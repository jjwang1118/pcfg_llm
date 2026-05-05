# Tag Definitions (RAG Format)

Each section describes one tag used in password segmentation and analysis. Each entry is self-contained and includes category, language (if applicable), definition, positive examples (password context), and counter-examples.

---

## ENGLISH_NOUN

**Category:** Linguistic POS Tag  
**Language:** English  

English nouns constitute the largest and most frequent word class, characterized by their ability to inflect for number, combine with determiners, and function primarily as subjects or objects. They denote anything from physical objects to abstract concepts.

**正例 (Examples):**
- "dragon" in password "dragon123" → ENGLISH_NOUN (common password base word)
- "sunshine" in "sunshine2020" → ENGLISH_NOUN (abstract noun as password root)
- "love" in "love2024" → ENGLISH_NOUN (noun form used as password segment)
- "angel" in "angel@123" → ENGLISH_NOUN

**反例 (Counter-examples):**
- "love" in "iloveyou" → ENGLISH_VERB (verb usage in phrasal password context)
- "running" in "running2024" → may be ENGLISH_NOUN (nominalized) or ENGLISH_VERB depending on model decision; default to ENGLISH_NOUN if base form is noun-like
- "she", "they" → ENGLISH_PRON (pronouns are a separate class)

---

## ENGLISH_VERB

**Category:** Linguistic POS Tag  
**Language:** English  

An English verb is a word that describes an action (run), occurrence (happen), or state of being (exist, feel).

**正例 (Examples):**
- "love" in "iloveyou" → ENGLISH_VERB (verb in concatenated password phrase)
- "hate" in "ihate123" → ENGLISH_VERB
- "run" in "run4ever" → ENGLISH_VERB
- "live" in "liveforever2024" → ENGLISH_VERB

**反例 (Counter-examples):**
- "love" in "love2024" → ENGLISH_NOUN (used as a noun base, not a verb phrase)
- "runner" in "runner123" → ENGLISH_NOUN (agent noun derived from verb)
- "quickly" → ENGLISH_ADV (modifies verbs but is itself an adverb)

---

## ENGLISH_PRON

**Category:** Linguistic POS Tag  
**Language:** English  

A pronoun is a word or phrase that substitutes for a noun or noun phrase. Pronouns are traditionally classified as a part of speech, with subtypes including personal, possessive, reflexive, reciprocal, demonstrative, relative, interrogative, and indefinite pronouns. Their meaning often depends on an antecedent via anaphora (e.g., "he" referring back to "that poor man").

**正例 (Examples):**
- "i" in "iloveyou" → ENGLISH_PRON (personal pronoun as password segment)
- "my" in "mypassword123" → ENGLISH_PRON (possessive pronoun)
- "me" in "loveme2024" → ENGLISH_PRON
- "you" in "iloveyou" → ENGLISH_PRON

**反例 (Counter-examples):**
- "my" when part of a name like "MySpace" → WKNE (brand name takes priority)
- "it" in "itsme123" → ENGLISH_PRON, but "it" alone in password may also be ENGLISH_X if role is ambiguous
- "man" → ENGLISH_NOUN (not a pronoun)

---

## ENGLISH_ADJ

**Category:** Linguistic POS Tag  
**Language:** English  

English adjectives are an open word class that semantically denote properties such as size, colour, mood, quality, and age. They head adjective phrases and typically function as modifiers in noun phrases or complements in verb phrases. Most adjectives inflect for grade (big → bigger → biggest) or use more/most for comparison, and are modifiable by very.

**正例 (Examples):**
- "cute" in "cutegirl2020" → ENGLISH_ADJ (adjective used as password prefix)
- "cool" in "coolboy123" → ENGLISH_ADJ
- "sexy" in "sexy2024" → ENGLISH_ADJ
- "sweet" in "sweet@home" → ENGLISH_ADJ

**反例 (Counter-examples):**
- "super" in "superman" → may be PRE (derivational prefix) rather than ENGLISH_ADJ depending on segmentation
- "quickly" → ENGLISH_ADV (ends in -ly, modifies verbs)
- "beauty" in "beauty2024" → ENGLISH_NOUN (nominalized form; the adjective would be "beautiful")

---

## ENGLISH_ADV

**Category:** Linguistic POS Tag  
**Language:** English  

An English adverb is a word that modifies verbs, adjectives, other adverbs, or entire sentences, expressing manner, time, place, frequency, degree, or speaker stance (e.g., unfortunately). Often formed by adding -ly to adjectives (e.g., quick → quickly), many also stand alone (e.g., well, fast, very).

**正例 (Examples):**
- "forever" in "loveforever" → ENGLISH_ADV (time adverb as password segment)
- "always" in "always123" → ENGLISH_ADV
- "never" in "never2give" → ENGLISH_ADV
- "forever" in "forever21" → ENGLISH_ADV

**反例 (Counter-examples):**
- "fast" in "fastcar2024" → ENGLISH_ADJ (modifying a noun, functions as adjective here)
- "well" in "well123" → ambiguous; default to ENGLISH_ADV unless clearly a noun
- "good" in "goodboy" → ENGLISH_ADJ (predicative/attributive adjective, not adverb)

---

## ENGLISH_ADP

**Category:** Linguistic POS Tag  
**Language:** English  

An adposition is a closed-class word that links a noun phrase to its syntactic head, expressing spatial, temporal, or semantic relationships. It serves as a cover term for prepositions (preceding the complement, e.g., in the box), postpositions, and circumpositions. Adpositions show no inflectional variation.

**正例 (Examples):**
- "under" in "under123" → ENGLISH_ADP (preposition as password segment)
- "over" in "over9000" → ENGLISH_ADP
- "in" in "inlove2024" → ENGLISH_ADP
- "at" in "at123home" → ENGLISH_ADP

**反例 (Counter-examples):**
- "up" in "whatsupp" → ENGLISH_PRT (particle in phrasal verb, not a preposition)
- "before" if followed by a clause structure → ENGLISH_CONJ (subordinating conjunction)
- "inside" used as an adjective modifier → ENGLISH_ADJ

---

## ENGLISH_CONJ

**Category:** Linguistic POS Tag  
**Language:** English  

An English conjunction is a closed-class, uninflected word that connects words, phrases, or clauses. The three main types are: coordinating conjunctions (FANBOYS: for, and, nor, but, or, yet, so) which join elements of equal grammatical rank; correlative conjunctions (both...and, either...or) which work in pairs; and subordinating conjunctions (because, although, while, since).

**正例 (Examples):**
- "and" in "youandme123" → ENGLISH_CONJ (coordinating conjunction in concatenated password)
- "or" in "noworever" → ENGLISH_CONJ
- "but" in "notbad2024" → ENGLISH_CONJ (though "not" here is ENGLISH_PRT)
- "n" in "rocknroll" → ENGLISH_CONJ (informal shortening of "and")

**反例 (Counter-examples):**
- "for" in "for2024" → ambiguous; default to ENGLISH_ADP if acting as preposition
- "so" in "so123" → ENGLISH_ADV if acting as degree modifier; ENGLISH_CONJ if connective
- "however" → ENGLISH_ADV (conjunctive adverb, not a true conjunction)

---

## ENGLISH_DET

**Category:** Linguistic POS Tag  
**Language:** English  

An English determiner is a closed-class word that precedes a noun or noun phrase to specify its reference, definiteness, quantity, or ownership. Subtypes include articles (a, the), demonstratives (this, that), possessives (my, your), quantifiers (some, many, few), distributives (each, every), and interrogative determiners (which, what). Unlike adjectives, determiners are not gradable and typically cannot appear as predicates.

**正例 (Examples):**
- "the" in "thebest123" → ENGLISH_DET (definite article as password segment)
- "my" in "mylife2024" → ENGLISH_DET (possessive determiner)
- "no" in "nopain2024" → ENGLISH_DET (determiner meaning "zero")
- "every" in "everyday123" → ENGLISH_DET

**反例 (Counter-examples):**
- "my" in "myspace" → WKNE (brand name; entity tag takes priority)
- "this" when standing alone → ENGLISH_PRON (demonstrative pronoun)
- "many" → ENGLISH_DET but rarely appears as standalone password segment; usually part of a phrase

---

## ENGLISH_PRT

**Category:** Linguistic POS Tag  
**Language:** English  

An English particle is a function word that must be associated with another word or phrase to impart meaning and does not fit neatly into other parts of speech. Common types include adverb particles in phrasal verbs (give up, turn on), the infinitive marker to, and the negative particle not. Particles are uninflected and have no standalone lexical definition.

**正例 (Examples):**
- "up" in "whatsupp" → ENGLISH_PRT (phrasal verb particle segment)
- "not" in "donot123" → ENGLISH_PRT (negative particle)
- "out" in "workout2024" → ENGLISH_PRT (particle in compound)
- "to" in "to4ever" → ENGLISH_PRT (informal spelling of infinitive marker in password)

**反例 (Counter-examples):**
- "up" in "upload" → PRE (prefix in compound word, not a standalone particle)
- "out" in "outdoor" → PRE (prefix, not a particle)
- "to" used as a number substitute in leet (e.g., "2") → NUMBER or LEET

---

## ENGLISH_NUM

**Category:** Linguistic POS Tag  
**Language:** English  

An English numeral is a word or phrase that expresses a precise numerical quantity. Cardinal numerals (one, two, twelve) indicate count and can replace articles before nouns. Ordinal numerals (first, second) indicate sequence. Numerals may function as determiners, nouns, or pronouns depending on context, and are distinct from quantifiers like many or several, which indicate only approximate quantity.

**正例 (Examples):**
- "one" in "numberone" → ENGLISH_NUM (cardinal numeral as password word)
- "first" in "firstlove" → ENGLISH_NUM (ordinal numeral)
- "two" in "twohearts2024" → ENGLISH_NUM
- "million" in "onemillion" → ENGLISH_NUM

**反例 (Counter-examples):**
- "1" in "love1" → NUMBER (digit form, not a written numeral)
- "once" in "once123" → ENGLISH_ADV (temporal adverb, not a numeral)
- "many" → ENGLISH_DET (quantifier, indicates approximate quantity, not a numeral)

---

## ENGLISH_X

**Category:** Linguistic POS Tag  
**Language:** English  

A catch-all tag for English tokens that do not fit any other defined English POS category.

**正例 (Examples):**
- "asdfg" treated as a word segment but not classifiable → ENGLISH_X
- Partial or truncated English words with no recognizable POS role → ENGLISH_X
- Emoticons embedded in password strings → ENGLISH_X

**反例 (Counter-examples):**
- Any token identifiable as NOUN, VERB, ADJ, ADV, ADP, CONJ, DET, PRT, or NUM → use the specific tag
- "qwerty" → KB (keyboard pattern, not ENGLISH_X)
- "123" → SR or NUMBER

---

## GERMAN_NOUN

**Category:** Linguistic POS Tag  
**Language:** German  

A German noun (Nomen/Substantiv) is a word that names a person, place, thing, or idea. Every German noun carries one of three grammatical genders (masculine der, feminine die, neuter das), is always capitalized in writing, and declines across four cases (Nominativ, Akkusativ, Dativ, Genitiv) and two numbers (singular/plural). Plural forms are irregular and must be learned individually; compound nouns inherit the gender of the final component.

**正例 (Examples):**
- "hund" in "meinHund99" → GERMAN_NOUN (dog; German noun as password base)
- "liebe" in "liebe2024" → GERMAN_NOUN (love; noun form)
- "sonne" in "sonne123" → GERMAN_NOUN (sun)
- "passwort" in "passwort1" → GERMAN_NOUN (word meaning "password")

**反例 (Counter-examples):**
- "schnell" in "schnell123" → GERMAN_ADV (adverb meaning fast, not a noun)
- "schön" → GERMAN_ADJ (adjective meaning beautiful)
- "laufen" → GERMAN_VERB (verb infinitive meaning to run)

---

## GERMAN_ADJ

**Category:** Linguistic POS Tag  
**Language:** German  

A German adjective (Adjektiv) is a word that modifies a noun, expressing properties such as size, colour, or quality. When used attributively (before a noun), it must agree with the noun in gender, number, and case, following one of three declension patterns: weak (after definite articles), mixed (after indefinite articles/possessives), or strong (no preceding article). When used predicatively (after sein, bleiben, werden) or adverbially, it remains uninflected.

**正例 (Examples):**
- "schön" in "schön123" → GERMAN_ADJ (beautiful; adjective as password segment)
- "klein" in "kleinekatze" → GERMAN_ADJ (small)
- "süß" in "süß2024" → GERMAN_ADJ (sweet/cute)
- "stark" in "stark99" → GERMAN_ADJ (strong)

**反例 (Counter-examples):**
- "schnell" in "schnell99" → GERMAN_ADV (adverb, even when used as password root)
- "Schönheit" in "Schönheit1" → GERMAN_NOUN (nominalized form "beauty", capitalized)
- "sehr" → GERMAN_ADV (degree adverb meaning "very")

---

## GERMAN_ADV

**Category:** Linguistic POS Tag  
**Language:** German  

A German adverb (Adverb) is an uninflected word that modifies verbs, adjectives, or other adverbs, providing information about place (hier, dort), time (gestern, jetzt), manner (schnell, gern), or cause (deshalb, trotzdem). Unlike adjectives, adverbs never take case endings. A key German feature is the -erweise suffix for sentence-level adverbs expressing the speaker's stance (e.g., glücklicherweise = "fortunately").

**正例 (Examples):**
- "immer" in "immer123" → GERMAN_ADV (always; time adverb as password segment)
- "hier" in "hierbin1" → GERMAN_ADV (here; place adverb)
- "schnell" in "schnell99" → GERMAN_ADV (fast; manner adverb)
- "nie" in "nie2024" → GERMAN_ADV (never)

**反例 (Counter-examples):**
- "schnelle" in "schnelleAuto" → GERMAN_ADJ (inflected adjective, not adverb)
- "immer" capitalized at start → still GERMAN_ADV (capitalization at sentence start doesn't change POS in password context)
- "Morgen" in "Morgen123" → GERMAN_NOUN (morning/tomorrow as noun, not adverb form)

---

## GERMAN_PRON

**Category:** Linguistic POS Tag  
**Language:** German  

A German pronoun (Pronomen) is a word that substitutes for a noun or noun phrase. It inflects for case (Nominativ, Akkusativ, Dativ, Genitiv), gender, number, and person. Major subtypes include personal pronouns (ich, du, er/sie/es), possessive pronouns (mein, dein), reflexive pronouns (mich/sich), demonstrative pronouns (dieser, jener), and relative pronouns (der, welcher). The formal second-person pronoun Sie is always capitalized.

**正例 (Examples):**
- "ich" in "ich2024" → GERMAN_PRON (I; personal pronoun as password segment)
- "mein" in "meinleben1" → GERMAN_PRON (my/mine; possessive pronoun)
- "du" in "du123" → GERMAN_PRON (you; personal pronoun)
- "wir" in "wir2024" → GERMAN_PRON (we)

**反例 (Counter-examples):**
- "mein" before a noun in "meinHund" → GERMAN_DET (possessive as determiner)
- "Man" (one/people) → distinct from GERMAN_NOUN "Mann" (man); check spelling carefully
- "ich" in leet form "1ch" → LEET (leet substitution takes priority)

---

## GERMAN_VERB

**Category:** Linguistic POS Tag  
**Language:** German  

A German verb (Verb) is a word expressing an action or state of being, conjugated to reflect person (1st/2nd/3rd), number (singular/plural), tense (Präsens, Präteritum, Perfekt, Plusquamperfekt, Futur I/II), mood (Indikativ, Imperativ, Konjunktiv I/II), and voice (active/passive). In main clauses, the conjugated verb always occupies the second position; in subordinate clauses, it moves to the final position.

**正例 (Examples):**
- "liebe" in "ichliebe123" → GERMAN_VERB (I love; verb form in password phrase)
- "laufen" in "laufen2024" → GERMAN_VERB (to run; infinitive)
- "lebe" in "ichlebe1" → GERMAN_VERB (I live; verb form)
- "machen" in "machen99" → GERMAN_VERB (to make/do)

**反例 (Counter-examples):**
- "liebe" in "liebe2024" → GERMAN_NOUN (love as noun, not verb phrase)
- "laufend" in "laufend123" → GERMAN_ADJ (present participle used as adjective)
- "Laufen" capitalized alone → GERMAN_NOUN (nominalized infinitive)

---

## FRENCH_NOUN

**Category:** Linguistic POS Tag  
**Language:** French  

A French noun (nom) is a word naming a person, place, thing, or idea. Every French noun has a grammatical gender — either masculine (le/un) or feminine (la/une) — and inflects for number (singular/plural, typically by adding -s in writing). There is no neuter gender. Gender is often arbitrary and must be memorized. Unlike German, French nouns are not capitalized unless they are proper nouns.

**正例 (Examples):**
- "amour" in "amour2024" → FRENCH_NOUN (love; noun as password base)
- "soleil" in "soleil123" → FRENCH_NOUN (sun)
- "coeur" in "moncoeur1" → FRENCH_NOUN (heart)
- "vie" in "mavie2024" → FRENCH_NOUN (life)

**反例 (Counter-examples):**
- "belle" in "belle123" → FRENCH_ADJ (beautiful; adjective form)
- "aimer" in "aimer2024" → FRENCH_VERB (to love; verb infinitive)
- "rapidement" → FRENCH_ADV (adverb ending in -ment)

---

## FRENCH_ADJ

**Category:** Linguistic POS Tag  
**Language:** French  

A French adjective (adjectif) is a word that modifies a noun and must agree with it in gender (masculine/feminine) and number (singular/plural), following up to four distinct forms (e.g., petit / petite / petits / petites). Most adjectives are placed after the noun, but a core group of common adjectives — typically describing beauty, age, goodness, or size (BAGS) — precede the noun.

**正例 (Examples):**
- "belle" in "belle2024" → FRENCH_ADJ (beautiful, feminine form)
- "petit" in "petitange" → FRENCH_ADJ (small/little + angel compound)
- "grand" in "grandamour" → FRENCH_ADJ (great/big in password phrase)
- "beau" in "beau123" → FRENCH_ADJ (beautiful, masculine form)

**反例 (Counter-examples):**
- "beauté" in "beauté123" → FRENCH_NOUN (beauty; nominalized form of adjective)
- "rapidement" → FRENCH_ADV (adverb, invariable, never agrees)
- "le", "la" → FRENCH_DET (articles, not adjectives)

---

## FRENCH_ADV

**Category:** Linguistic POS Tag  
**Language:** French  

A French adverb (adverbe) is an invariable word that modifies a verb, adjective, prepositional phrase, or another adverb. It does not agree in gender or number. Most French adverbs are derived from adjectives by adding -ment to the feminine form (e.g., lente → lentement). Types include place (ici, là), time (maintenant, hier), manner (bien, vite), quantity (très, assez), and negation (ne...jamais).

**正例 (Examples):**
- "toujours" in "toujours123" → FRENCH_ADV (always; time adverb as password segment)
- "jamais" in "jamais2024" → FRENCH_ADV (never)
- "bien" in "bien99" → FRENCH_ADV (well)
- "vite" in "vite123" → FRENCH_ADV (fast)

**反例 (Counter-examples):**
- "rapide" in "rapide2024" → FRENCH_ADJ (fast as adjective; adverb would be "rapidement")
- "bien" in "lebien" → FRENCH_NOUN (nominalized: "the good")
- "toujours" in leet form "t0uj0urs" → LEET (leet substitution takes priority)

---

## FRENCH_PRON

**Category:** Linguistic POS Tag  
**Language:** French  

A French pronoun (pronom) is a word that substitutes for a noun phrase to avoid repetition. French pronouns inflect for person, number, gender, and case (subject, direct object, indirect object, stressed/disjunctive). Key subtypes include personal subject pronouns (je, tu, il/elle, nous, vous, ils/elles), object clitics (me, te, lui, y, en), reflexive pronouns (se), possessive pronouns (le mien), demonstrative pronouns (celui, celle), and relative pronouns (qui, que, dont, où).

**正例 (Examples):**
- "je" in "jesuis2024" → FRENCH_PRON (I; personal subject pronoun in password)
- "tu" in "tu123" → FRENCH_PRON (you)
- "mon" in "moncoeur1" → FRENCH_PRON (my/mine; possessive pronoun)
- "moi" in "moi2024" → FRENCH_PRON (me; stressed/disjunctive pronoun)

**反例 (Counter-examples):**
- "mon" before a noun in "moncoeur" → FRENCH_DET (possessive as determiner before noun)
- "je" in leet "j3" → LEET (leet substitution takes priority)
- "nous" as part of a brand name → WKNE if recognized (entity tag takes priority)

---

## FRENCH_VERB

**Category:** Linguistic POS Tag  
**Language:** French  

A French verb (verbe) is a word expressing action or state, conjugated to reflect mood (indicatif, subjonctif, conditionnel, impératif), tense (past, present, future), person (1st/2nd/3rd), and number (singular/plural). French has three regular verb groups (-er, -ir, -re) plus numerous irregular verbs. Compound tenses are formed with auxiliary avoir or être plus a past participle.

**正例 (Examples):**
- "aimer" in "aimer2024" → FRENCH_VERB (to love; infinitive as password base)
- "aime" in "jetaime123" → FRENCH_VERB (love; conjugated form in password phrase)
- "vivre" in "vivre99" → FRENCH_VERB (to live; infinitive)
- "suis" in "jesuisla" → FRENCH_VERB (am; conjugated être)

**反例 (Counter-examples):**
- "amour" in "amour2024" → FRENCH_NOUN (love as noun, not verb)
- "aimant" in "aimant123" → FRENCH_ADJ (loving; present participle as adjective)
- "rapidement" → FRENCH_ADV (modifies verbs but is itself an adverb)

---

## X

**Category:** Linguistic POS Tag  
**Language:** Other / Language-agnostic  

A catch-all tag for tokens that do not belong to any defined language-specific POS category and cannot be classified under any other tag in the schema.

**正例 (Examples):**
- A password segment in an unrecognized language or script → X
- Truncated or corrupted word fragments with no identifiable POS → X
- Mixed-language tokens that span multiple language systems ambiguously → X

**反例 (Counter-examples):**
- Any token identifiable as ENGLISH_*, GERMAN_*, or FRENCH_* → use the specific POS tag
- "!@#$" → SPEC (has its own tag)
- "123" → SR or NUMBER (has its own tag)

---

## MALE_NAME

**Category:** Proper Noun & Entity  

A token or span identifying a masculine personal name — given names, full names, or common name variants typically associated with male individuals (e.g., James, 大衛, Mohammed). This tag covers first names, full names, and culturally recognized male name patterns. It excludes titles, honorifics, and gender-neutral names unless context confirms male gender.

**正例 (Examples):**
- "james" in "james1990" → MALE_NAME (male given name as password root)
- "david" in "david123" → MALE_NAME
- "大衛" in "大衛2024" → MALE_NAME (Chinese transliteration of David)
- "mohammed" in "mohammed99" → MALE_NAME

**反例 (Counter-examples):**
- "alex" in "alex2024" → ambiguous gender, avoid MALE_NAME unless confirmed
- "jordan" → gender-neutral, requires context to assign MALE_NAME
- "james" as a brand (e.g., LeBron James as WKNE context) → entity tag may take priority

---

## FEMALE_NAME

**Category:** Proper Noun & Entity  

A token or span identifying a feminine personal name — given names, full names, or common name variants typically associated with female individuals (e.g., Emma, 小芳, Fatima). Analogous to MALE_NAME, it covers first names and full names where female gender is established by cultural convention or context.

**正例 (Examples):**
- "emma" in "emma2000" → FEMALE_NAME (female given name as password root)
- "小芳" in "小芳123" → FEMALE_NAME (common Chinese female name)
- "fatima" in "fatima99" → FEMALE_NAME
- "mary" in "mary2024" → FEMALE_NAME

**反例 (Counter-examples):**
- "victoria" in "victoria2024" → ambiguous; could be LOCATION (Victoria Harbour) or FEMALE_NAME — use context
- "alex", "taylor" → gender-neutral without confirmation
- "emma" as a brand name → check if WKNE applies first

---

## CN_NAME_ABBR

**Category:** Proper Noun & Entity  

A span representing an abbreviated form of a Chinese proper noun — typically a shortened version of an institution, organization, person name, or brand that is recognizable without the full form (e.g., 台大 → 國立臺灣大學, 健保 → 全民健康保險, 北大 → 北京大學). These abbreviations are culturally established and differ from acronyms in that they are phonologically derived from the source name rather than initialism-based.

**正例 (Examples):**
- "台大" in "台大2024" → CN_NAME_ABBR (short for 國立臺灣大學, used as password segment)
- "健保" in "健保123" → CN_NAME_ABBR (short for 全民健康保險)
- "北大" in "北大99" → CN_NAME_ABBR (short for 北京大學)
- "勞保" in "勞保2024" → CN_NAME_ABBR

**反例 (Counter-examples):**
- "台灣" in "台灣2024" → LOCATION (full proper noun, not an abbreviation)
- "NTU" → not CN_NAME_ABBR (initialism-based acronym, not phonological)
- "台北" → LOCATION (full city name)

---

## WKNE

**Category:** Proper Noun & Entity  

A named entity that is globally or regionally well-known and can be identified without additional context — typically large organizations, flagship brands, landmark institutions, or universally recognized proper nouns (e.g., Apple, Google, 聯合國, McDonald's, 台積電). Distinguished from UBE by the entity's high public recognizability and unambiguous referent.

**正例 (Examples):**
- "apple" in "apple2024" → WKNE (Apple Inc. brand used as password base)
- "google" in "google123" → WKNE
- "nike" in "nike2024!" → WKNE (globally recognized brand)
- "tsmc" in "tsmc99" → WKNE (台積電 abbreviation)

**反例 (Counter-examples):**
- "apple" in "applepie123" → ENGLISH_NOUN (apple as food, not brand — context-dependent)
- "小明髮廊" → UBE (local business, not a known entity)
- "台北市" → LOCATION (geographic entity, not an organization)

---

## UBE

**Category:** Proper Noun & Entity  

A span that appears to refer to a business, brand, or commercial entity but cannot be verified against known databases or corpora — typically small businesses, local shops, informal brands, newly founded companies, or entities with insufficient public information (e.g., 小明髮廊, XYZ 工程行). Used when the text contains strong signals of a commercial entity (e.g., 行, 店, 公司, Co., Ltd.) but the specific entity is not identifiable as a WKNE.

**正例 (Examples):**
- "小明髮廊" in "小明髮廊2024" → UBE (local shop as password base)
- "xyz工程行" in "xyz工程行99" → UBE
- "阿鴻小吃" in "阿鴻小吃123" → UBE
- "wangbakery" in "wangbakery1" → UBE (small local brand)

**反例 (Counter-examples):**
- "apple" → WKNE (globally recognized brand)
- "7eleven" in "7eleven123" → WKNE (internationally recognized franchise)
- "公司" alone → not UBE (common noun, not a named entity)

---

## LOCATION

**Category:** Proper Noun & Entity  

A span identifying a geographical or spatial entity — including countries, cities, regions, addresses, landmarks, and named geographical features (e.g., Taiwan, 台北市, Eiffel Tower, 淡水河). May include both physical locations and geopolitical entities (GPE). Covers named places (Paris), administrative regions (Île-de-France), and natural features (Amazon River) as a unified class.

**正例 (Examples):**
- "taipei" in "taipei2024" → LOCATION (city used as password base)
- "taiwan" in "taiwan123" → LOCATION
- "paris" in "paris2024!" → LOCATION
- "台北" in "台北99" → LOCATION

**反例 (Counter-examples):**
- "apple" → WKNE (brand name, not a location)
- "home" in "home2024" → ENGLISH_NOUN (common noun, not a named geographic entity)
- "north" → ENGLISH_NOUN/ADV (directional word, not a named location)

---

## YEAR

**Category:** Date & Number  

A 4-digit token representing a calendar year, typically in the range of a plausible historical or future year. Covers standalone year references in numeric form. Does not include 2-digit abbreviated years (e.g., '99) or year ranges unless the full 4-digit form is present.

**Pattern:** `\d{4}` where the value falls within 1000–2999

**正例 (Examples):**
- "2024" in "dragon2024" → YEAR (year suffix in password)
- "1998" in "born1998" → YEAR (birth year as password segment)
- "2000" in "y2k2000" → YEAR

**反例 (Counter-examples):**
- "99" in "dragon99" → NUMBER (2-digit, not a YEAR)
- "20241231" → DATE_8DIGIT (full 8-digit date, not standalone year)
- "1234" in a PIN-like context → NUMBER (value outside typical year range or lacks year semantics)

---

## DATE_6DIGIT

**Category:** Date & Number  

A 6-digit string encoding a compact date, most commonly in YYYYMM or YYMMDD format. Used in formal documents, invoices, IDs, and records where a shortened date representation is standard.

**Pattern:** `\d{6}`  
**Common formats:**
- YYYYMM → 202401 = January 2024
- YYMMDD → 240101 = January 1st, 2024

**正例 (Examples):**
- "199803" in "john199803" → DATE_6DIGIT (birth year-month as password segment)
- "991231" in "991231abc" → DATE_6DIGIT (YYMMDD format)
- "202401" in "key202401" → DATE_6DIGIT

**反例 (Counter-examples):**
- "2024" → YEAR (4-digit, not 6)
- "20240101" → DATE_8DIGIT (8-digit, not 6)
- "123456" with no date context → SR or NUMBER

---

## DATE_8DIGIT

**Category:** Date & Number  

An 8-digit string encoding a full date, most commonly in YYYYMMDD format. Widely used in government documents, databases, and Chinese administrative systems as the standard machine-readable date format.

**Pattern:** `\d{8}`  
**Common format:** YYYYMMDD → 20240101 = January 1st, 2024

**正例 (Examples):**
- "19980315" in "john19980315" → DATE_8DIGIT (full birthdate as password segment)
- "20001231" in "20001231abc" → DATE_8DIGIT
- "19991231" in "key19991231" → DATE_8DIGIT

**反例 (Counter-examples):**
- "2024" → YEAR (only 4 digits)
- "202401" → DATE_6DIGIT (only 6 digits)
- "12345678" → NUMBER (value outside valid YYYYMMDD date range)

---

## MONTH

**Category:** Date & Number  

A token or span representing a calendar month, either as a numeral, a written-out name, or a culture-specific expression. Covers standalone month references without a full date context. Must carry clear month semantics (e.g., accompanied by 月 or used as a month name) to distinguish from generic NUMBER.

**Pattern variants:**
- Numeric with suffix: 1月, 12月, 三月
- Full name (EN): January … December
- Abbreviated (EN): Jan, Feb, Mar …

**正例 (Examples):**
- "3月" in "生日3月" → MONTH (birth month as password segment)
- "december" in "december2024" → MONTH (full English month name)
- "jan" in "jan1998" → MONTH (abbreviated month)
- "十二月" in "十二月123" → MONTH

**反例 (Counter-examples):**
- "3" alone in "dragon3" → NUMBER (bare digit without month context)
- "march" as a surname in "march2024" → MALE_NAME or FEMALE_NAME depending on context
- "may" in "may2024" → ambiguous between MONTH and FEMALE_NAME; use context

---

## CN_MOBILE

**Category:** Date & Number  

An 11-digit string representing a mainland China mobile phone number, beginning with 1 followed by a carrier-assigned second digit. Follows the format standardized by the Ministry of Industry and Information Technology (MIIT).

**Pattern:** `1[3-9]\d{9}`

**正例 (Examples):**
- "13812345678" in password "13812345678" → CN_MOBILE (phone number used directly as password)
- "17600001234" → CN_MOBILE
- "19912345678" → CN_MOBILE

**反例 (Counter-examples):**
- "0912345678" → NUMBER (Taiwan mobile format, 10-digit, not CN)
- "13812345" → NUMBER (only 8 digits, too short for CN_MOBILE)
- "10012345678" → NUMBER (second digit 0 is not a valid CN carrier prefix)

---

## NUMBER

**Category:** Date & Number  

A catch-all tag for numeric tokens or spans that do not match more specific tags (YEAR, DATE_6DIGIT, DATE_8DIGIT, CN_MOBILE). Covers integers, decimals, percentages, quantities, ordinals, and written-out numbers across languages.

**Subtypes covered:**
- Cardinal integers: 42, 1,000,000
- Decimals: 3.14, 0.5
- Percentages: 85%, 百分之五
- Written-out: 三十二, twenty, deux
- Ordinals: 第三, 3rd, 第1名

**正例 (Examples):**
- "99" in "dragon99" → NUMBER (2-digit suffix, no date semantics)
- "520" in "love520" → NUMBER (Chinese internet slang for "I love you", non-date digit string)
- "007" in "james007" → NUMBER (leading zero, not a year)
- "42" in "answer42" → NUMBER

**反例 (Counter-examples):**
- "2024" in "dragon2024" → YEAR (4-digit in year range with year semantics)
- "13812345678" → CN_MOBILE (matches CN mobile pattern)
- "123456" with sequential pattern → SR (sequential repeat takes priority)

---

## EMAIL

**Category:** String Pattern & Structure  

A string matching the standard email address format: a local part, @ symbol, and domain. May appear standalone or embedded within text.

**Pattern:** `[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}`

**正例 (Examples):**
- "user@example.com" used as a password → EMAIL
- "john.doe@gmail.com" in credential dataset → EMAIL
- "alice_123@mail.co.uk" → EMAIL

**反例 (Counter-examples):**
- "user@localhost" → not EMAIL (no valid TLD)
- "@username" → not EMAIL (social handle, no domain structure)
- "google.com" → DN (domain without @ and local part)

---

## DN

**Category:** String Pattern & Structure  

A string representing a fully qualified domain name (FQDN) or hostname, consisting of labels separated by dots, ending in a valid top-level domain (TLD).

**Pattern:** `[\w-]+(\.[\w-]+)+\.[a-zA-Z]{2,}`

**正例 (Examples):**
- "google.com" used as password segment → DN
- "mail.example.org" → DN
- "api.service.io" → DN

**反例 (Counter-examples):**
- "user@google.com" → EMAIL (contains @ symbol)
- "google" alone → WKNE (brand name without domain structure)
- "192.168.1.1" → NUMBER or SPEC (IP address, not a domain name)

---

## KB

**Category:** String Pattern & Structure  

A string formed by consecutive or adjacent keys on a standard keyboard layout (QWERTY/QWERTZ/AZERTY), typically used as weak passwords or shortcuts. Includes horizontal, vertical, and diagonal key sequences.

**Pattern logic:** Adjacent key traversal on keyboard grid

**正例 (Examples):**
- "qwerty" → KB (top row, left-to-right traversal)
- "asdf" → KB (home row segment)
- "1q2w3e" → KB (alternating number/letter columns)
- "zxcvbn" → KB (bottom row traversal)

**反例 (Counter-examples):**
- "abcde" → SR (sequential alphabetical order, not keyboard-adjacent)
- "password" → ENGLISH_NOUN (real word, not a keyboard pattern)
- "123456" → SR (numeric sequential, not keyboard-adjacent)

---

## SR

**Category:** String Pattern & Structure  

A string composed of monotonically increasing or decreasing characters — numeric, alphabetic, or mixed — forming a predictable sequence. Common in weak passwords and placeholder inputs.

**Subtypes:**
- Numeric ascending: 12345, 123456789
- Numeric descending: 987654
- Alpha ascending: abcde, abcdefg
- Repeating: aaaa, 1111, zzzz

**正例 (Examples):**
- "123456" → SR (most common weak password, numeric ascending)
- "abcdef" → SR (alpha ascending)
- "9876" → SR (numeric descending)
- "1111" → SR (repeating digit)

**反例 (Counter-examples):**
- "qwerty" → KB (keyboard-adjacent pattern, not monotonically sequential)
- "2024" in year context → YEAR (year semantics take priority)
- "1a2b3c" → not SR (mixed non-monotonic; may be KB or NUMBER)

---

## PRE

**Category:** String Pattern & Structure  

A string segment identified as a meaningful prefix — a morpheme, word, or pattern that appears at the beginning of a token and carries derivational or structural significance.

**正例 (Examples):**
- "Super" in "Super123!" → PRE (word prefix in password structure)
- "my" in "mycat2024" → PRE (possessive word prefix — when not tagged as ENGLISH_PRON)
- "un" in "unlock99" → PRE (negation morpheme prefix)
- "re" in "restart2024" → PRE (repetition morpheme prefix)

**反例 (Counter-examples):**
- "super" as standalone password → ENGLISH_ADJ (complete word, not a prefix)
- "123" at end of "Super123" → SUF (suffix segment, not prefix)
- "up" in "upload" → context-dependent; could be PRE if clearly a prefix morpheme

---

## SUF

**Category:** String Pattern & Structure  

A string segment identified as a meaningful suffix — a morpheme, word, or pattern that appears at the end of a token, often indicating inflection, derivation, or padding.

**正例 (Examples):**
- "123" in "dragon123" → SUF (numeric padding suffix, most common password suffix)
- "!" in "Password!" → SUF (special character padding suffix)
- "2024" in "myname2024" → SUF (year as padding suffix — when not tagged as YEAR)
- "@123" in "Password@123" → SUF (mixed padding suffix)

**反例 (Counter-examples):**
- "2024" as standalone password → YEAR (not a suffix when appearing independently)
- "dragon" at start of "dragon123" → PRE or ENGLISH_NOUN (prefix/root, not suffix)
- "123456" as full password → SR (sequential pattern, not a suffix of another segment)

---

## PY

**Category:** String Pattern & Structure  

A string matching Mandarin Chinese romanization (Pinyin) — a sequence of valid Pinyin syllables with or without tone marks, used to represent Chinese words phonetically in ASCII.

**Pattern logic:** Valid Pinyin initials + finals (e.g., zh, ch, sh + vowel combinations)

**正例 (Examples):**
- "beijing" in "beijing2008" → PY (Pinyin of 北京, common password base)
- "wode" in "wode123" → PY (Pinyin of 我的)
- "xiaoming" in "xiaoming99" → PY (Pinyin of a common Chinese name 小明)
- "aini" in "aini2024" → PY (Pinyin of 愛你, "I love you")

**反例 (Counter-examples):**
- "bj" in "bj2024" → CONSONANTS (consonant-only abbreviation, not a full Pinyin syllable)
- "china" → ENGLISH_NOUN or LOCATION (English word, not Pinyin)
- "beijing" if tagged as a location → LOCATION takes priority over PY in entity context

---

## CONSONANTS

**Category:** String Pattern & Structure  

A string composed exclusively of consonant characters with no vowels, typically indicating an abbreviation, acronym, keyboard pattern, or non-phonetic token.

**Consonants (EN):** b c d f g h j k l m n p q r s t v w x y z

**正例 (Examples):**
- "bj" in "bj2024" → CONSONANTS (abbreviation of 北京 Beijing using initials)
- "pwd" in "pwd123" → CONSONANTS (abbreviation of password)
- "mgr" in "mgr2024" → CONSONANTS (abbreviation of manager)
- "zh" in "zh123" → CONSONANTS (Pinyin consonant-only abbreviation)

**反例 (Counter-examples):**
- "qwerty" → KB (keyboard-adjacent pattern — key adjacency takes priority over consonant-only check)
- "pwd" if recognized as a well-known abbreviation in a brand context → WKNE may apply
- "bcdf" as purely random consonants with no abbreviation semantics → may fall back to CONSONANTS or X

---

## SPEC

**Category:** String Pattern & Structure  

A string or token composed of non-alphanumeric symbols, including punctuation, currency signs, mathematical operators, and Unicode special characters.

**Character set:** `! @ # $ % ^ & * ( ) _ + - = [ ] { } | ; ' : " , . / < > ? \` ~`

**正例 (Examples):**
- "!" in "dragon2024!" → SPEC (single special character padding)
- "!@#$" in "!@#$abc" → SPEC (common special character sequence in password)
- "***" in "***pass" → SPEC
- "_" in "my_password" → SPEC (underscore as separator)

**反例 (Counter-examples):**
- "3.14" → NUMBER (decimal number; dot is part of numeric format)
- "@" in "user@example.com" → part of EMAIL (not isolated SPEC)
- "p@ssw0rd" → LEET (leet substitution pattern, not pure special characters)

---

## LEET

**Category:** String Pattern & Structure  

A string using leet substitutions — systematic replacement of standard letters with visually similar numbers or symbols, derived from "elite" hacker culture.

**Common substitutions:** a → 4 or @, e → 3, i → 1 or !, o → 0, s → 5 or $, t → 7, l → 1

**正例 (Examples):**
- "p@ssw0rd" → LEET (a→@, o→0; leet version of "password")
- "h3ll0" → LEET (e→3, o→0; leet version of "hello")
- "dr@g0n" → LEET (a→@, o→0; leet version of "dragon")
- "4dm1n" → LEET (a→4, i→1; leet version of "admin")

**反例 (Counter-examples):**
- "dragon" → ENGLISH_NOUN (no leet substitution applied)
- "!@#$" → SPEC (pure special characters with no underlying letter pattern)
- "1234" → SR or NUMBER (sequential digits, not leet substitution of letters)
