# Konu temaları: uygulamada her seviyenin altında bu başlıklarla gruplanır (sıra: tema, sonra bu listedeki sıra)
THEMES=[
('Fiil zamanları',['to-be','present-simple','present-continuous','simple-vs-continuous','past-simple','irregular-verbs','spelling-rules','will-going-to','present-for-future','present-perfect','past-continuous','present-perfect-continuous','for-since-ago','pp-vs-past-simple','still-yet-already','used-to','time-clauses','past-perfect','past-perfect-continuous','future-continuous-perfect','future-in-the-past','be-to-future','would-uses']),
('Modal fiiller ve rica / teklif',['can-cant','can-could-able-to','must-have-to-should','requests-offers-permission','may-might','shall-ought-need','had-better-would-rather','modals-deduction','past-modals']),
('Koşul cümleleri ve dilek',['zero-conditional','first-conditional','second-conditional','unless-provided','in-time-in-case','third-conditional','wish-if-only','conditionals-advanced','subjunctive']),
('Soru yapıları ve kısa cevaplar',['question-words','subject-object-questions','indirect-questions','question-tags','short-answers','auxiliary-so-do-i','even-negative-questions']),
('İsimler ve belirleyiciler',['plural-nouns','articles','names-the','articles-advanced','this-that','possessives','noun-noun','countable-uncountable','quantifiers','all-every-whole','both-either-neither-all-each','indefinite-pronouns','there-is-are','there-vs-it','numbers-dates-time']),
('Zamirler',['pronouns','reflexive-each-other']),
('Sıfat ve zarf',['adjectives-adverbs','adjectives-ed-ing','adjective-order','comparatives-superlatives','comparison-advanced','so-such-too-enough','quite-rather','frequency-adverbs','adverb-position','gradable-adjectives','like-as','senses-linking-verbs','adjective-to-infinitive','compound-adjectives']),
('Edatlar',['prepositions-in-on-at','prepositions-place','prepositions-time-movement','adjective-prepositions','verb-prepositions','noun-prepositions','preposition-ing','exceptions-between']),
('Fiil kalıpları',['have-got','do-make-have-get','like-love-ing','gerund-infinitive','ing-to-meaning','verb-object-to-infinitive','make-let-perception','indirect-object','phrasal-separable','phrasal-types','causative','reporting-verbs']),
('Edilgen çatı ve dolaylı anlatım',['passive-voice','passive-advanced','reported-speech','passive-reporting']),
('Cümle kurma ve bağlaçlar',['imperatives','word-order','conjunctions-basic','cause-result','linkers-contrast-purpose','advanced-linkers','relative-clauses','relative-clauses-2','participle-clauses','subject-verb-agreement','it-structures','noun-that-clauses']),
('Vurgu ve ileri düzey',['emphasis','inversion','cleft-sentences','ellipsis-substitution','hedging-nominalisation','nuance-register','error-correction']),
('Kelime bilgisi',['prefixes-suffixes','word-formation']),
]
THEME_POS={}
for _i,(_n,_ids) in enumerate(THEMES):
    for _j,_id in enumerate(_ids):THEME_POS[_id]=(_i,_j,_n)
