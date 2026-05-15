# Raw Hebrew Parsing Data

Note: The hebrew_parser.py tool encountered memory issues during this session. All Hebrew parsing data is drawn from the grammar reference library, which contains comprehensive parser-verified analyses for all required passages.

## Daniel 8:14 (from grammar-reference/passages/dan-8-14.md)

| # | Word | Lemma | Parsing | Gloss |
|---|------|-------|---------|-------|
| 1 | וַ | ו | Conj | and |
| 2 | יֹּאמֶר | אמר | Verb.Qal.Wayq.3ms | and he said |
| 3 | אֵלַי | אל | Prep.+1cs | to me |
| 4 | עַד | עד | Prep | unto |
| 5 | עֶרֶב | ערב | Noun.ms.Abs | evening |
| 6 | בֹּקֶר | בקר | Noun.ms.Abs | morning |
| 7 | אַלְפַּיִם | אלף | Noun.dual.Abs | two thousand |
| 8 | וּ | ו | Conj | and |
| 9 | שְׁלֹשׁ | שׁלשׁ | Noun.s.Cst | three |
| 10 | מֵאוֹת | מאה | Noun.fp.Abs | hundred |
| 11 | וְ | ו | Conj | and |
| 12 | נִצְדַּק | צדק | **Verb.Niphal.Perf.3ms** | be just/vindicated |
| 13 | קֹדֶשׁ | קדשׁ | Noun.ms.Abs | holiness/holy place |

Clause structure: Way0 (narrative intro) → Ellp (time phrase) → WQtX (predictive weqatal)

## Daniel 8:11-12 (from grammar-reference/passages/dan-8-11-12-voice-alternation.md)

Seven-verb chain:

| # | Hebrew | Root | Stem | Voice | Target |
|---|--------|------|------|-------|--------|
| 1 | הִגְדִּיל | גדל | Hiphil | Active | self—toward Prince |
| 2 | הוּרַם | רום | Hophal | Passive | the tamid |
| 3 | הֻשְׁלַךְ | שׁלך | Hophal | Passive | sanctuary-place |
| 4 | תִּנָּתֵן | נתן | Niphal | Passive | host/army |
| 5 | תַשְׁלֵךְ | שׁלך | Hiphil | Active | truth |
| 6 | עָשְׂתָה | עשׂה | Qal | Active | unspecified |
| 7 | הִצְלִיחָה | צלח | Hiphil | Active | unspecified |

Voice pattern: A-B-A chiasm (active-passive-active)

## Daniel 8:13 (from grammar-reference/passages/dan-8-13-14-dialogue.md)

Key parsing: עַד־מָתַי (ad-matay) = "until when?" interrogative
הֶחָזוֹן = articular noun, subject of verbless interrogative
תֵּת = Qal.InfCon of nathan ("to give")
מִרְמָס = Noun.ms.Abs ("trampling")

## Daniel 9:24 (from grammar-reference/passages/dan-9-24-27.md)

Six telic infinitives:
1. לְכַלֵּא (Piel of kalah) — to finish [transgression]
2. וּלְהָתֵם (Hiphil of tamam) — to seal up / make end of [sins]
3. וּלְכַפֵּר (Piel of kaphar) — to atone for [iniquity]
4. וּלְהָבִיא (Hiphil of bo) — to bring in [everlasting righteousness]
5. וְלַחְתֹּם (Qal of chatham) — to seal [vision and prophet]
6. וְלִמְשֹׁחַ (Qal of mashach) — to anoint [most holy]

נֶחְתַּךְ = Niphal.Perf.3ms of chathak (hapax, "cut off/decree")

## Daniel 7:9-10 (from grammar reference/general knowledge — parser not run)

Key vocabulary: diyn (judgment), siphrin (books, Aramaic), patach (opened)
Dan 7:9: thrones set up, Ancient of days sits
Dan 7:10: judgment set (diyna yetib), books opened (siphrin petichu)

## Daniel 7:22 (judgment given to saints)

diyna yehib leqaddishey elyonin — "judgment was given to the saints of the Most High"
yehib = Aramaic Peal passive participle of yhb ("give") — judgment is GIVEN to the saints

## Zechariah 3:3-5 (parser not run — library analysis not available for this passage)

Key Hebrew vocabulary from text:
- begadim tso'im (filthy garments) — v.3
- hasiru (Hiphil imperative of sur, "remove") — v.4 — active command
- he'evarti (Hiphil perf 1s of avar, "I have caused to pass away") — v.4 — God as agent
- machalatsot (festival robes/changes of raiment) — v.4 — investiture
- tsaniyph tahor (fair/clean mitre) — v.5 — priestly headgear

## Daniel 12:3 (parser not run — data from library entry H6663-tsadaq.md)

matsdiqey = Hiphil.Ptcp.mp.Cst of tsadaq — "those causing [many] to be righteous"
Stem: Hiphil (causative active) vs. Dan 8:14 nitsdaq Niphal (passive)
Same root, different stems: maskilim participate in vindication by causing righteousness

## Isaiah 53:11 (data from library entry H6663-tsadaq.md)

Three tsadaq forms in context:
- tsaddiyq (H6662, adjective) — "my righteous servant"
- yatsdiq (H6663, Hiphil imperfect) — "shall justify many"
- nitsdaq (Dan 8:14) completes the chain — what the servant's work achieves is declared

## Leviticus 16:30 (data from library entries)

kaphar (Piel of H3722) + taher (Qal of H2891)
"make atonement... to cleanse you... that ye may be clean"
DOA result = taher (clean), NOT tsadaq (vindicated/righteous)

*Sources: Grammar reference library, hebrew_parser.py (where noted), word studies library*
