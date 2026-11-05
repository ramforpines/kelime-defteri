// PET yazma / konuşma değerlendirmesi (Supabase Edge Function: pet-eval)
// Gerekli gizli anahtar (Edge Functions → Secrets): ANTHROPIC_API_KEY
// İsteğe bağlı: PET_MODEL (varsayılan aşağıda)
// Kota ve yetki: kullanıcının kendi oturumuyla pet_eval_take / pet_eval_save (supabase-pet-eval.sql) çağrılır.

const SB_URL = Deno.env.get("SUPABASE_URL") ?? "https://cqlcrwolgxrrrcyyluin.supabase.co";
const SB_PUB = "sb_publishable_UXoJCOF_Su6EjPdrIcpYVA_dYntzppl"; // uygulamadaki herkese açık anahtar
const AI_KEY = Deno.env.get("ANTHROPIC_API_KEY") ?? "";
const MODEL = Deno.env.get("PET_MODEL") ?? "claude-haiku-5-5";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const out = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json" } });

async function rpc(name: string, args: unknown, auth: string) {
  const r = await fetch(`${SB_URL}/rest/v1/rpc/${name}`, {
    method: "POST",
    headers: { apikey: SB_PUB, Authorization: auth, "Content-Type": "application/json" },
    body: JSON.stringify(args),
  });
  const t = await r.text();
  if (!r.ok) throw new Error(t || String(r.status));
  return t ? JSON.parse(t) : null;
}

const clip = (s: unknown, n: number) => String(s ?? "").slice(0, n);

function prompt(b: any) {
  const topics = (Array.isArray(b.topics) ? b.topics : []).slice(0, 80)
    .map((t: any) => `${clip(t.id, 40)}: ${clip(t.t, 60)}`).join("\n");
  const common = `Accuracy rules:
- Only list errors you are certain are wrong in standard English. Do NOT mark correct alternatives, British/American spelling variants, informal but acceptable style, or contractions as errors.
- "orig" must be copied exactly from the student's text. Do not invent errors to fill the list; an empty list is fine.
- Score against B1 level, not native level: a B1 candidate who communicates clearly with some errors can still get 3-4.
Feedback language: Turkish (explanations, summary, tips). Quote the student's words and corrections in English.
For each error give the grammar topic id from this list if one fits, otherwise null:
${topics}
Return ONLY a JSON object, no markdown.`;
  if (b.kind === "w") {
    return {
      system: `You are an experienced Cambridge B1 Preliminary (PET) writing examiner. Assess the student's answer with the PET writing assessment scales, each 0-5:
Content: 5 = all content is relevant and the reader is fully informed; 3 = minor irrelevances or omissions, reader on the whole informed; 1 = irrelevances or misinterpretation, reader minimally informed; 0 = totally irrelevant.
Communicative Achievement: 5 = uses the conventions of the task to hold the reader's attention and communicate straightforward ideas; 3 = conventions used in generally appropriate ways; 1 = produces text that communicates simple ideas in simple ways.
Organisation: 5 = text is generally well organised and coherent, using a variety of linking words and cohesive devices; 3 = connected and coherent, using basic linking words and a limited number of cohesive devices; 1 = connected using basic, high-frequency linking words.
Language: 5 = range of everyday vocabulary used appropriately, range of simple and some complex grammatical forms with a good degree of control, errors do not impede communication; 3 = basic vocabulary used reasonably appropriately, simple grammatical forms with a good degree of control, errors noticeable but meaning can still be determined; 1 = basic vocabulary and simple grammatical forms, errors may impede meaning at times.
Scores 4 and 2 are between the described bands. Be fair, consistent and accurate for a B1 exam. ${common}`,
      user: `TASK (${b.part === 1 ? "Part 1 email" : "Part 2 " + clip(b.genre, 20)}):
${clip(b.task, 1500)}

CONTENT POINTS THE ANSWER MUST COVER:
${clip(b.points, 600)}

STUDENT ANSWER (${clip(b.words, 6)} words):
"""${clip(b.text, 3000)}"""

JSON schema:
{"scores":{"content":0-5,"communicative":0-5,"organisation":0-5,"language":0-5},"level":"A2"|"B1"|"B2","summary":"2-3 Turkish sentences","strengths":["Turkish, max 3"],"errors":[{"orig":"exact wrong phrase from the answer","fix":"corrected phrase","why":"short Turkish explanation","topic":"topic id or null"}],"improved":"the student's answer rewritten at strong B1 level, keeping their ideas","tips":["Turkish, max 3, concrete"]}
List at most 8 of the most important errors.`,
    };
  }
  return {
    system: `You are an experienced Cambridge B1 Preliminary (PET) speaking examiner. You receive an automatic speech-recognition transcript of a student's spoken answer. The transcript may contain recognition mistakes, has no reliable punctuation and you cannot hear pronunciation: do not penalise punctuation, capitalisation or likely recognition errors, and do not score pronunciation. Score Grammar and Vocabulary, and Discourse Management (length, organisation, linking, relevance), each 0-5 on the PET scale. ${common}`,
    user: `SPEAKING TASK (Part ${clip(b.part, 2)}):
${clip(b.task, 800)}

Time allowed: ${clip(b.limit, 4)} s. Student spoke for ${clip(b.dur, 4)} s.
TRANSCRIPT:
"""${clip(b.text, 2500)}"""

JSON schema:
{"scores":{"grammar_vocab":0-5,"discourse":0-5},"level":"A2"|"B1"|"B2","summary":"2-3 Turkish sentences","strengths":["Turkish, max 3"],"errors":[{"orig":"phrase from transcript","fix":"better phrase","why":"short Turkish explanation","topic":"topic id or null"}],"improved":"a natural B1-level answer built on the student's ideas","tips":["Turkish, max 3, concrete"]}
List at most 6 errors. If the transcript is empty or unrelated, say so in the summary and give 0 scores.`,
  };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return out({ error: "method" }, 405);
  const auth = req.headers.get("Authorization") ?? "";
  if (!auth.startsWith("Bearer ")) return out({ error: "auth" }, 401);
  if (!AI_KEY) return out({ error: "setup" }, 500);
  let b: any;
  try { b = await req.json(); } catch { return out({ error: "bad" }, 400); }
  if (b.kind !== "w" && b.kind !== "s") return out({ error: "bad" }, 400);
  if (String(b.text ?? "").trim().split(/\s+/).length < 5) return out({ error: "short" }, 400);

  let take: any;
  try { take = await rpc("pet_eval_take", { p_kind: b.kind, p_task: clip(b.id, 40) }, auth); }
  catch (e) {
    const m = String((e as Error).message);
    return out({ error: /limit/.test(m) ? "limit" : /not allowed|JWT|jwt/.test(m) ? "auth" : "db" }, /limit/.test(m) ? 429 : 403);
  }

  try {
    const p = prompt(b);
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": AI_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({ model: MODEL, max_tokens: 2000, temperature: 0, system: p.system, messages: [{ role: "user", content: p.user }] }),
    });
    if (!r.ok) throw new Error("ai " + r.status + " " + (await r.text()).slice(0, 300));
    const j = await r.json();
    const txt = (j.content ?? []).map((c: any) => c.text ?? "").join("");
    const s = txt.indexOf("{"), e = txt.lastIndexOf("}");
    const res = JSON.parse(txt.slice(s, e + 1));
    const ids = new Set((Array.isArray(b.topics) ? b.topics : []).map((t: any) => t.id));
    (res.errors ?? []).forEach((x: any) => { if (x.topic && !ids.has(x.topic)) x.topic = null; });
    await rpc("pet_eval_save", { p_id: take.id, p_out: res }, auth).catch(() => {});
    return out({ ok: true, left: take.left, res });
  } catch (e) {
    console.error(e);
    await rpc("pet_eval_save", { p_id: take.id, p_out: null }, auth).catch(() => {}); // hak geri verilir
    return out({ error: "ai" }, 502);
  }
});
