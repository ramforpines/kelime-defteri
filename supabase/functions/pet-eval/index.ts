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

const EXAMS: Record<string, string> = { A2: "A2 Key (KET)", B1: "B1 Preliminary (PET)", B2: "B2 First (FCE)", C1: "C1 Advanced (CAE)" };
const NEXT: Record<string, string> = { A2: "B1", B1: "B2", B2: "C1", C1: "C2" };
const PREV: Record<string, string> = { A2: "A1", B1: "A2", B2: "B1", C1: "B2" };

function topicList(b: any) {
  return (Array.isArray(b.topics) ? b.topics : []).slice(0, 80)
    .map((t: any) => `${clip(t.id, 40)}: ${clip(t.t, 60)}`).join("\n");
}
function common(b: any, lv: string) {
  return `Accuracy rules:
- Only list errors you are certain are wrong in standard English. Do NOT mark correct alternatives, British/American spelling variants, informal but acceptable style, or contractions as errors.
- "orig" must be copied exactly from the student's text. Do not invent errors to fill the list; an empty list is fine.
- Score against ${lv} level, not native level: a ${lv} candidate who communicates clearly with some errors can still get 3-4.
Feedback language: Turkish (explanations, summary, tips). Quote the student's words and corrections in English.
For each error give the grammar topic id from this list if one fits, otherwise null:
${topicList(b)}
Return ONLY a JSON object, no markdown.`;
}
function wPrompt(b: any, t: any, lv: string) {
  const ex = EXAMS[lv] ?? EXAMS.B1;
  return {
    system: `You are an experienced Cambridge ${ex} writing examiner. Assess the student's answer with the Cambridge writing assessment scales, each 0-5, interpreted for the ${lv} level of this exam:
Content: 5 = all content is relevant and the reader is fully informed; 3 = minor irrelevances or omissions, reader on the whole informed; 1 = irrelevances or misinterpretation, reader minimally informed; 0 = totally irrelevant.
Communicative Achievement: 5 = uses the conventions of the task effectively to hold the reader's attention and communicate ideas; 3 = conventions used in generally appropriate ways; 1 = communicates simple ideas in simple ways.
Organisation: 5 = well organised and coherent, using a variety of linking words and cohesive devices; 3 = connected and coherent, using basic linking words and a limited number of cohesive devices; 1 = connected using basic, high-frequency linking words.
Language: 5 = range of vocabulary and grammatical forms appropriate for ${lv}, used with a good degree of control, errors do not impede communication; 3 = vocabulary and grammar reasonably appropriate, errors noticeable but meaning clear; 1 = basic vocabulary and simple forms, errors may impede meaning at times.
Scores 4 and 2 are between the described bands. Be fair, consistent and accurate. ${common(b, lv)}`,
    user: `TASK (Part ${clip(t.part, 2)}${t.genre ? " " + clip(t.genre, 20) : ""}, target ${clip(t.min, 4)}-${clip(t.max, 4)} words):
${clip(t.task, 1500)}

CONTENT POINTS THE ANSWER MUST COVER:
${clip(t.points, 600)}

STUDENT ANSWER (${clip(t.words, 6)} words):
"""${clip(t.text, 3500)}"""

JSON schema:
{"scores":{"content":0-5,"communicative":0-5,"organisation":0-5,"language":0-5},"level":"${PREV[lv] ?? "A2"}"|"${lv}"|"${NEXT[lv] ?? "C2"}","summary":"2-3 Turkish sentences","strengths":["Turkish, max 3"],"errors":[{"orig":"exact wrong phrase from the answer","fix":"corrected phrase","why":"short Turkish explanation","topic":"topic id or null"}],"improved":"the student's answer rewritten at strong ${lv} level, keeping their ideas","tips":["Turkish, max 3, concrete"]}
List at most 8 of the most important errors.`,
  };
}
const sSystem = (b: any, lv: string) => `You are an experienced Cambridge ${EXAMS[lv] ?? EXAMS.B1} speaking examiner. You receive automatic speech-recognition transcripts of a student's spoken answers. Transcripts may contain recognition mistakes, have no reliable punctuation and you cannot hear pronunciation: do not penalise punctuation, capitalisation or likely recognition errors, and do not score pronunciation. Score Grammar and Vocabulary, and Discourse Management (length, organisation, linking, relevance), each 0-5, interpreted for the ${lv} level. ${common(b, lv)}`;

function prompt(b: any) {
  const lv = EXAMS[b.lv] ? b.lv : "B1";
  if (b.kind === "w") {
    return wPrompt(b, { part: b.part, genre: b.genre, task: b.task, points: b.points, text: b.text, words: b.words, min: b.min ?? 80, max: b.max ?? 130 }, lv);
  }
  return {
    system: sSystem(b, lv),
    user: `SPEAKING TASK (Part ${clip(b.part, 2)}):
${clip(b.task, 800)}

Time allowed: ${clip(b.limit, 4)} s. Student spoke for ${clip(b.dur, 4)} s.
TRANSCRIPT:
"""${clip(b.text, 2500)}"""

JSON schema:
{"scores":{"grammar_vocab":0-5,"discourse":0-5},"level":"${PREV[lv]}"|"${lv}"|"${NEXT[lv]}","summary":"2-3 Turkish sentences","strengths":["Turkish, max 3"],"errors":[{"orig":"phrase from transcript","fix":"better phrase","why":"short Turkish explanation","topic":"topic id or null"}],"improved":"a natural ${lv}-level answer built on the student's ideas","tips":["Turkish, max 3, concrete"]}
List at most 6 errors. If the transcript is empty or unrelated, say so in the summary and give 0 scores.`,
  };
}
function sExamPrompt(b: any) {
  const lv = EXAMS[b.lv] ? b.lv : "B1";
  const items = (Array.isArray(b.s) ? b.s : []).slice(0, 20).map((x: any, i: number) =>
    `#${i + 1} (Part ${clip(x.part, 2)}, ${clip(x.limit, 4)} s allowed, spoke ${clip(x.dur, 4)} s)\nQ: ${clip(x.task, 400)}\nA: """${clip(x.text, 1200)}"""`).join("\n\n");
  return {
    system: sSystem(b, lv),
    user: `These are all the answers from one speaking test. Assess the whole performance.

${items}

JSON schema:
{"scores":{"grammar_vocab":0-5,"discourse":0-5},"level":"${PREV[lv]}"|"${lv}"|"${NEXT[lv]}","summary":"2-3 Turkish sentences","strengths":["Turkish, max 3"],"errors":[{"orig":"phrase from a transcript","fix":"better phrase","why":"short Turkish explanation","topic":"topic id or null"}],"improved":"a strong ${lv}-level model answer to the question where the student was weakest, starting with the question number","tips":["Turkish, max 3, concrete"]}
List at most 8 errors. Unanswered or empty answers lower the discourse score.`,
  };
}

async function ask(p: { system: string; user: string }, ids: Set<string>) {
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": AI_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify({ model: MODEL, max_tokens: 2500, temperature: 0, system: p.system, messages: [{ role: "user", content: p.user }] }),
  });
  if (!r.ok) throw new Error("ai " + r.status + " " + (await r.text()).slice(0, 300));
  const j = await r.json();
  const txt = (j.content ?? []).map((c: any) => c.text ?? "").join("");
  const s = txt.indexOf("{"), e = txt.lastIndexOf("}");
  const res = JSON.parse(txt.slice(s, e + 1));
  (res.errors ?? []).forEach((x: any) => { if (x.topic && !ids.has(x.topic)) x.topic = null; });
  return res;
}
const words = (t: unknown) => String(t ?? "").trim().split(/\s+/).filter(Boolean).length;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  if (req.method !== "POST") return out({ error: "method" }, 405);
  const auth = req.headers.get("Authorization") ?? "";
  if (!auth.startsWith("Bearer ")) return out({ error: "auth" }, 401);
  if (!AI_KEY) return out({ error: "setup" }, 500);
  let b: any;
  try { b = await req.json(); } catch { return out({ error: "bad" }, 400); }
  if (b.kind !== "w" && b.kind !== "s" && b.kind !== "x") return out({ error: "bad" }, 400);
  if (b.kind !== "x" && words(b.text) < 5) return out({ error: "short" }, 400);
  if (b.kind === "x") {
    const ws = (Array.isArray(b.w) ? b.w : []).filter((t: any) => words(t.text) >= 5).slice(0, 3);
    const ss = (Array.isArray(b.s) ? b.s : []).filter((t: any) => words(t.text) >= 1);
    if (!ws.length && !ss.length) return out({ error: "short" }, 400);
  }

  let take: any;
  try { take = await rpc("pet_eval_take", { p_kind: b.kind, p_task: clip(b.id, 40) }, auth); }
  catch (e) {
    const m = String((e as Error).message);
    return out({ error: /limit/.test(m) ? "limit" : /not allowed|JWT|jwt/.test(m) ? "auth" : "db" }, /limit/.test(m) ? 429 : 403);
  }

  try {
    const ids = new Set<string>((Array.isArray(b.topics) ? b.topics : []).map((t: any) => t.id));
    let res: any;
    if (b.kind === "x") {
      const lv = EXAMS[b.lv] ? b.lv : "B1";
      const wl = Array.isArray(b.w) ? b.w : [];
      const ss = (Array.isArray(b.s) ? b.s : []).filter((t: any) => words(t.text) >= 1);
      const [w, s] = await Promise.all([
        Promise.all(wl.map((t: any) => words(t.text) >= 5 ? ask(wPrompt(b, t, lv), ids) : Promise.resolve(null))),
        ss.length ? ask(sExamPrompt(b), ids) : Promise.resolve(null),
      ]);
      res = { w, s };
    } else {
      res = await ask(prompt(b), ids);
    }
    await rpc("pet_eval_save", { p_id: take.id, p_out: res }, auth).catch(() => {});
    return out({ ok: true, left: take.left, res });
  } catch (e) {
    console.error(e);
    await rpc("pet_eval_save", { p_id: take.id, p_out: null }, auth).catch(() => {}); // hak geri verilir
    return out({ error: "ai" }, 502);
  }
});
