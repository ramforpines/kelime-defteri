"""Kaynaklarda (Oxford 3000/5000, CEFR-J, Octanove) bulunmayan tek kelimelerin elle gözden geçirilmiş seviyeleri.
Ölçüt: kelimenin günlük kullanım sıklığı, kavramsal zorluğu ve B1/B2 sınav metinlerinde görülme olasılığı."""
def G(lv,s):return {w:lv for w in s.split()}
MAN={}
# --- A1/A2: temel ---
MAN.update(G('A1','children'))
MAN.update(G('A2','eighteenth eleventh nineteenth bravo hooray gasoline hen'))
# --- B1: gündelik, somut ---
MAN.update(G('B1','''chore bumpy joyful gesundheit stress-free finals get-together mic welcoming fizzy
skinny tweet bullying hoodie motel staircase lizard chalk ebook scanner flyer brunch router cart sip wallpaper hallway technician intern gosh ugh yuck phew
kindergarten tractor toddler puddle bungalow beige binoculars porridge sporty cutlery mittens mitten heatwave introvert extrovert guesthouse painkiller decaf gigabyte washable multitask
workmate oversleep seasick satnav jetlag wholemeal streetlight sunburnt jogger cordless contactless lentil wheelbarrow honeybee beekeeper sleeveless pensioner drizzle scorching gust touchscreen
overcast smog celeb kayak Fahrenheit baggy faucet refill crunchy shrub snowfall hectic trekking fussy unsubscribe rinse voucher autograph caretaker flip-flop grumpy stroll almond moth pollen
rooftop blizzard avalanche workload patio darts oatmeal hotline eco-friendly gladly cosmetics beware erase outdated spectators unfinished handmade disposable hassle graffiti edible furry
slippery unused courtyard alarmed alarming coughing knitting striped sideways neatly tunes tutorial lightweight font all-inclusive preview subscribe check-out open-air tax-free sugar-free
world-famous nine-to-five dog-tired self-catering wiki self-esteem time-consuming billboard scam automobile rented horizontal burnt cracked packaging tidily serviette nightclothes untidily mislay
mislaid unkindly touchable tallness dirtiness unfriendliness fizzy'''))
# --- B2 ---
MAN.update(G('B2','''android rip-off self-portrait silicon depot glossy leafy snapshot janitor rodent toad insults disrespectful intimidating wrecked plentiful funnel flashy effortlessly jokingly hopelessly
unintentionally seasonally shameless giver playhouse conversational romantically wobbly snug puffy ugliness invisibility pessimism flatten outwards displeased grower streetcar twig twister stutter
sieve revolting inactivity symbolize fertiliser microchip befriend bookkeeper catchphrase expertly flawlessly hurrah insecticide irregularly midpoint nibble shears unofficially unreasonably sensibly
bluish oar biodegradable eatery energetically greenery mismatched overused pail restock savoury scaly carnivore biofuel amphibian muffler peacemaker reachable spud storehouse wintry disassemble
bookworm clumsily gusty hobbyist inaccurately keepsake letdown lodger parasol productively purifier siesta strainer underpass uninjured unsatisfying wordy healthily herbivore simile glasshouse
loyally monolingual overpay thankfulness silkworm inexpensively magnifier unequally unpleasantly explainable abbreviate inefficiently peacefulness polythene punctually woodworker crèche unromantic
imperial metropolitan marsh aerial photographic heavens radioactive yeast pod geometric jockey pointer yarn flattering puff sneaky thorn maize
in-house must-have start-up better-off run-down first-hand break-in hands-on state-of-the-art decided first-rate dead-end down-to-earth short-lived high-rise park-and-ride stuck-up super-rich
ground-breaking lay-by entry-level two-faced off-peak black-tie cutting-edge cape knight emerging finest infinite pat vintage like-minded inn overview streak page-turner smart-casual pile-up war-torn
gauge cord crushed liking liquor narrow-minded ranch randomly rushed static cylinder white-collar blue-collar amber e-cigarette ruby pharmaceutical overwhelmed abusive automated confidential
excluded feminine hooked mindset one-sided sober unified unstable handbook fist networking petroleum livestock visibility rigid prototype biased detached digit inconsistent inferior innocence
invalid refined structured subjective disturbed foil neglected poisoning splendid textile armour fatty twilight migrant renewal veterinary insulin skeptical comprehend devastated challenger coating
contaminated detector incapable instability intentional manually masculine monarch peek poetic premature protector rot routinely schooling shove storyline stunned takeover unarmed unlawful crust
hose caffeine millennium obese linguistic responsive briefing auburn chilling chic deluxe retro scoop analytical famine scarce furnace repetitive drastic drastically citrus comforting disguised
disrespect distressed fading falsely fearful fertile incompetent morals pillar podium restless secrecy theoretically thriving typhoon insecurity nun adulthood multinational razor-sharp emerald
gluten-free tailor-made simulator horsepower dosage groundbreaking shuffle dart arrogance bitterness bland clarification concise cunning cyclone digestive disconnected forgiving fungus garments
imperfect incidentally inefficient insignificant intensely misuse respectfully self-centred snatch soothing stimulating swiftly troubling vaguely wellbeing overdue wrestle mural backbone fingerprint
usable appendix glitch invaluable overrated fast-paced law-abiding rethink sitcom nausea auditor recap symmetry extravagant iceberg landfill multicultural commuter migrate relocate adolescence dusk
etiquette excessively hesitant lodging mildly outspoken overflow plainly reassuring scrape senseless sturdy umpire unavoidable unjust soften revisit caterpillar misguided far-fetched heartfelt
gripping illiterate acronym fluorescent manageable chubby goggles evergreen sapphire mammal decimal equator migraine stationery considerate cautiously cramped disgraceful heartless seasoning
secretive securely syllabus unethical unexplained ungrateful unsuccessfully itchy monsoon eerie speechless turquoise sculptor prepaid carbohydrate reptile slum pesticide flammable envious courteous
detergent gracefully painless plump thaw uneducated unqualified congested paparazzi pastel webinar archery handcuffs sprinter suede brisk phobia antisocial chairperson exhale illogical informally
pastime spotless unproductive unwind unwelcome superstitious overpriced hammock dermatologist alibi chalet slimy apologetic blockage impatience overcrowding tearful unskilled yolk mouthful wrinkled
pushy multilingual overpass boardroom childlike chatty rehearse thrifty runny subtraction beehive scruffy argumentative pliers veranda helpline sizzle downpour layoff sleet indigestion tweezers
dominoes tongs procrastinate overpopulation cyberbullying corkscrew halve sweltering brainy cufflinks upmarket banknote muggy retrain draughts grater soundproof untruthful unspoilt unfriend
showery shopaholic resit bedsit ovenproof unfasten canoeist airsickness typeface chiropractor cardiologist frock fresher biopic phishing renovate compost trespass nauseous celebratory crutches
renewables polygon photosynthesis vertebrate emigrate granted'''))
# --- C1 (C2'den indirilen) ---
MAN.update(G('C1','''has-been forward-looking off-colour self-harm power-hungry cure-all tongue-tied spike escort savage deceased quantum maritime hardy cardiac biting crushing drainage extraction parody
invasive baseline awakening brook ensemble insanity chronicle crimson flop readiness relocation resentment venom consul procession cleanse cosmos deity durability fauna imbalance implant
incompatible longing medicinal swine epilepsy marrow ceremonial compressor broth livelihood novice pouch gland saliva newness watchful mishap layering tasteful tireless unforgiving regrettable
bacterium mallet merciless fragility deceitful impure instructive passively successively trickery veer vengeful whirl jolt sedative ailment retract melatonin monochrome deciduous oceanography
disprove downplay illiteracy immeasurable parched siphon spiteful wail combative confiscate opinionated randomness flinch bureaucrat correspondingly amenity blameless defenceless indecision
industrious insufficiently justifiably recklessness scuffle unremarkable unscientific untamed skimpy inaudible overhang affluence excavate collapsible demotion disagreeable drape dystopia impurity
insincere invertebrate jovial placard sorrowful trinket triumphantly disown impassable unchanging bramble contaminant encircle forgetfulness impulsively inadequately irregularity irrelevance
irresponsibility outhouse selflessness shrunken stockholder unnaturally uproot weariness mnemonic bedridden poacher ageism enrage immobility indiscreet preachy unavoidably undervalue uninvolved
unreliability unchangeable typecast cinders decelerate demote dissenter favouritism steadiness unachievable understate unemotional unemployable uselessness warmonger unpredictably pollinator
soundbite deregulate inadvisable joblessness nearness endorphin courteously doubter fruitlessly mechanisation thoughtlessly cremate umpteen undemanding miscast dawdle anticlimax cohabit forefather
ineffectively outrank sadden shantytown triviality compostable guesstimate hotheaded deepness promptness sightless unawareness unpick poky teetotal doubtfully gloomily moreish meanly icily rehouse
breathalyser uncleanliness insincerely'''))

# --- kalıplar: C1'de duran sık phrasal verb'ler ---
PV={}
PV.update(G('B1','learn about|comment on|disagree with'.replace(' ','_').replace('|',' ')))
PV.update(G('B2',"""back down|fall for|fall through|go along with|kick off|reach out|set back|settle for|step down|step in|stick up for|tell apart|track down|trade in|weigh up|break even|burn out|catch on|cut in|die down|draw up|jot down|lay out|live up to|long for|narrow down|nod off|opt for|pick on|play down|rip off|run down|set aside|spell out|step up|stir up|tone down|win over|wind up|write off|back out|bank on|bounce back|branch out|chip in|ease off|stand up to|team up|blend in|doze off|storm out|shop around|spice up|crop up|slim down|cash in on|cave in|flag down|gang up|calm down|fill out|get down to|dawn on|rush into|carry over|come up against|come down to|boil down to|pass down|bring on|fight off|flare up|filter out|break through|call on|come through|drag on|fall back on|hold off|iron out|make for|see through|turn against|wear down""".replace(' ','_').replace('|',' ')))
PV={k.replace('_',' '):v for k,v in PV.items()}
