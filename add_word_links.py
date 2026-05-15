#!/usr/bin/env python3
"""
Add Blue Letter Bible links to Hebrew and Greek words (transliterated and Unicode)
in the etc-website markdown files.

Complements add_blb_links.py which links Strong's numbers (H1234, G1234).
This script links the actual word forms to their BLB lexicon pages.

Usage:
    python add_word_links.py                    # Process all study files
    python add_word_links.py --dry-run          # Show what would change
    python add_word_links.py --revert           # Remove all word links
    python add_word_links.py --stats            # Show statistics only
"""

import re
import os
import argparse
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "docs" / "studies"

BLB_HEBREW_URL = "https://www.blueletterbible.org/lexicon/h{num}/kjv/wlc/0-1/"
BLB_GREEK_URL = "https://www.blueletterbible.org/lexicon/g{num}/kjv/tr/0-1/"

# ============================================================
# WORD -> STRONG'S NUMBER MAPPING
# Format: "word_form": ("H" or "G", number)
# ============================================================

WORD_MAP = {
    # ========================================
    # HEBREW TRANSLITERATIONS
    # ========================================

    # H5315 - nephesh (soul, living being, creature)
    "nephesh": ("H", 5315),

    # H7307 - ruach (wind, breath, spirit)
    "ruach": ("H", 7307),

    # H5397 - neshamah (breath, blast)
    "neshamah": ("H", 5397),
    "nishmat": ("H", 5397),

    # H7585 - sheol (grave, underworld)
    "sheol": ("H", 7585),

    # H2416 - chay/chayyah (alive, living, life)
    "chayyah": ("H", 2416),
    "chay": ("H", 2416),

    # H4191 - muwth (to die)
    "muwth": ("H", 4191),
    "muth": ("H", 4191),
    "tamuth": ("H", 4191),

    # H4194 - maveth (death)
    "maveth": ("H", 4194),

    # H6754 - tselem (image)
    "tselem": ("H", 6754),

    # H1823 - demuth (likeness)
    "demuth": ("H", 1823),

    # H127 - adamah (ground, soil)
    "adamah": ("H", 127),

    # H582 - enosh (mortal man)
    "enosh": ("H", 582),

    # H5769 - olam (forever, age, eternity)
    "olam": ("H", 5769),

    # H5301 - naphach (to breathe, blow)
    "naphach": ("H", 5301),

    # H3462 - yashen (to sleep)
    "yashen": ("H", 3462),

    # H7901 - shakab (to lie down)
    "shakab": ("H", 7901),

    # H1478 - gava (to breathe out, expire)
    "gava": ("H", 1478),

    # H7496 - rephaim (shades, deceased)
    "rephaim": ("H", 7496),

    # H6 - abad (to perish, destroy)
    "abad": ("H", 6),

    # H8045 - shamad (to desolate, destroy utterly)
    "shamad": ("H", 8045),

    # H3772 - karath (to cut off)
    "karath": ("H", 3772),

    # H3615 - kalah (to end, consume, destroy utterly)
    "kalah": ("H", 3615),

    # H7843 - shachath (to decay, ruin, destroy)
    "shachath": ("H", 7843),

    # H1197 - baar (to kindle, burn, consume)
    "baar": ("H", 1197),

    # H398 - akal (to eat, consume, devour)
    "akal": ("H", 398),

    # H6789 - tsamath (to extirpate, destroy)
    "tsamath": ("H", 6789),

    # H1860 - deraon (contempt, abhorrence)
    "deraon": ("H", 1860),

    # H6757 - tsalmaveth (shadow of death)
    "tsalmaveth": ("H", 6757),

    # H7290 - radam (to stun, be in deep sleep)
    "radam": ("H", 7290),

    # H8639 - tardemah (deep sleep, trance)
    "tardemah": ("H", 8639),

    # H1745 - dumah (silence)
    "dumah": ("H", 1745),

    # H2011 - Hinnom
    "Hinnom": ("H", 2011),

    # H2143 - zeker (memorial, remembrance)
    "zeker": ("H", 2143),

    # H4912 - mashal (proverb, parable)
    "mashal": ("H", 4912),

    # ========================================
    # GREEK TRANSLITERATIONS
    # ========================================

    # G5590 - psyche (soul, life, person)
    "psyche": ("G", 5590),

    # G4151 - pneuma (spirit, breath, wind)
    "pneuma": ("G", 4151),

    # G110 - athanasia (immortality, deathlessness)
    "athanasia": ("G", 110),

    # G861 - aphtharsia (incorruptibility, immortality)
    "aphtharsia": ("G", 861),

    # G862 - aphthartos (incorruptible, immortal)
    "aphthartos": ("G", 862),

    # G2349 - thnetos (mortal)
    "thnetos": ("G", 2349),

    # G2288 - thanatos (death)
    "thanatos": ("G", 2288),

    # G2222 - zoe (life)
    "zoe": ("G", 2222),

    # G622 - apollymi (to destroy, perish)
    "apollymi": ("G", 622),
    "apollumi": ("G", 622),

    # G684 - apoleia (destruction, perdition)
    "apoleia": ("G", 684),

    # G86 - hades (unseen, realm of the dead)
    "hades": ("G", 86),

    # G1067 - gehenna (Valley of Hinnom, hell)
    "gehenna": ("G", 1067),
    "geenna": ("G", 1067),

    # G5020 - tartaroo (to cast to Tartarus)
    "tartaroo": ("G", 5020),
    "tartarus": ("G", 5020),

    # G166 - aionios (eternal, age-long)
    "aionios": ("G", 166),

    # G165 - aion (age, eon)
    "aion": ("G", 165),

    # G2837 - koimao (to put to sleep)
    "koimao": ("G", 2837),

    # G386 - anastasis (resurrection)
    "anastasis": ("G", 386),

    # G928 - basanizo (to torment, test)
    "basanizo": ("G", 928),

    # G929 - basanismos (torment)
    "basanismos": ("G", 929),

    # G2851 - kolasis (punishment, correction)
    "kolasis": ("G", 2851),

    # G4663 - skolex (worm)
    "skolex": ("G", 4663),

    # G3041 - limne (lake)
    "limne": ("G", 3041),

    # G3639 - olethros (ruin, destruction)
    "olethros": ("G", 3639),

    # G2618 - katakaio (to burn down, consume)
    "katakaio": ("G", 2618),

    # G2719 - katesthio (to eat down, devour)
    "katesthio": ("G", 2719),

    # G2654 - katanalisko (to consume utterly)
    "katanalisko": ("G", 2654),

    # G1842 - exolethreuo (to destroy utterly)
    "exolethreuo": ("G", 1842),

    # G5351 - phtheiro (to corrupt, destroy)
    "phtheiro": ("G", 5351),

    # G5356 - phthora (decay, corruption, destruction)
    "phthora": ("G", 5356),

    # G4983 - soma (body)
    "soma": ("G", 4983),

    # G3498 - nekros (dead, corpse)
    "nekros": ("G", 3498),

    # G3500 - nekrosis (deadness, dying)
    "nekrosis": ("G", 3500),

    # G3800 - opsonion (wages, pay)
    "opsonion": ("G", 3800),

    # G5486 - charisma (gift, grace-gift)
    "charisma": ("G", 5486),

    # G266 - hamartia (sin, missing the mark)
    "hamartia": ("G", 266),

    # G599 - apothnesko (to die off)
    "apothnesko": ("G", 599),

    # G2227 - zoopoieo (to make alive, give life)
    "zoopoieo": ("G", 2227),

    # G2673 - katargeo (to abolish, render ineffective)
    "katargeo": ("G", 2673),

    # G615 - apokteino (to kill)
    "apokteino": ("G", 615),

    # G360 - analyo (to depart, dissolve)
    "analyo": ("G", 360),

    # G1841 - exodos (departure, decease)
    "exodos": ("G", 1841),

    # G3857 - paradeisos (paradise)
    "paradeisos": ("G", 3857),

    # G1553 - ekdemeo (to be away from home)
    "ekdemeo": ("G", 1553),

    # G1736 - endemeo (to be at home)
    "endemeo": ("G", 1736),

    # G2588 - kardia (heart)
    "kardia": ("G", 2588),

    # G3952 - parousia (coming, presence)
    "parousia": ("G", 3952),

    # G4152 - pneumatikos (spiritual)
    "pneumatikos": ("G", 4152),

    # G2217 - zophos (darkness, gloom)
    "zophos": ("G", 2217),

    # G2920 - krisis (judgment, decision)
    "krisis": ("G", 2920),

    # G2647 - katalyo (to destroy, dissolve)
    "katalyo": ("G", 2647),

    # G5349 - phthartos (corruptible, perishable)
    "phthartos": ("G", 5349),

    # G623 - Apollyon (Destroyer)
    "Apollyon": ("G", 623),

    # G2289 - thanatoo (to kill, put to death)
    "thanatoo": ("G", 2289),

    # G2518 - katheudo (to sleep)
    "katheudo": ("G", 2518),

    # G609 - apokopto (to cut off)
    "apokopto": ("G", 609),

    # G4931 - synteleo (to complete, finish)
    "synteleo": ("G", 4931),

    # G5594 - psycho (to breathe, blow)
    "psycho": ("G", 5594),

    # G4636 - skenos (tent, tabernacle)
    "skenos": ("G", 4636),

    # G4638 - skenoma (tabernacle, dwelling)
    "skenoma": ("G", 4638),

    # G2771 - kerdos (gain)
    "kerdos": ("G", 2771),

    # G3311 - merismos (dividing, separation)
    "merismos": ("G", 3311),

    # ========================================
    # HEBREW UNICODE -- with vowel points
    # ========================================

    "נֶפֶשׁ": ("H", 5315),
    "נַפְשִׁי": ("H", 5315),
    "נַפְשׁוֹ": ("H", 5315),
    "נַפְשְׁךָ": ("H", 5315),

    "רוּחַ": ("H", 7307),

    "נְשָׁמָה": ("H", 5397),
    "נִשְׁמַת": ("H", 5397),

    "שְׁאוֹל": ("H", 7585),

    "חַי": ("H", 2416),
    "חַיָּה": ("H", 2416),
    "חַיִּים": ("H", 2416),

    "מָוֶת": ("H", 4194),

    "צֶלֶם": ("H", 6754),
    "דְּמוּת": ("H", 1823),

    "עוֹלָם": ("H", 5769),

    "אֱנוֹשׁ": ("H", 582),
    "אָדָם": ("H", 120),

    # Hebrew unpointed forms
    "נפש": ("H", 5315),
    "נפשׁ": ("H", 5315),
    "רוח": ("H", 7307),
    "נשמה": ("H", 5397),
    "נשׁמה": ("H", 5397),
    "שאול": ("H", 7585),
    "שׁאול": ("H", 7585),
    "צלם": ("H", 6754),
    "דמות": ("H", 1823),
    "עולם": ("H", 5769),
    "אדם": ("H", 120),

    # ========================================
    # GREEK UNICODE -- lemma & common forms
    # ========================================

    # G5590 - psyche
    "ψυχή": ("G", 5590),
    "ψυχῆς": ("G", 5590),
    "ψυχὴν": ("G", 5590),
    "ψυχῇ": ("G", 5590),
    "ψυχαί": ("G", 5590),
    "ψυχάς": ("G", 5590),
    "ψυχὴ": ("G", 5590),
    "ψυχῶν": ("G", 5590),

    # G4151 - pneuma
    "πνεῦμα": ("G", 4151),
    "πνεύματος": ("G", 4151),
    "πνεύματι": ("G", 4151),

    # G110 - athanasia
    "ἀθανασία": ("G", 110),
    "ἀθανασίαν": ("G", 110),

    # G861 - aphtharsia
    "ἀφθαρσία": ("G", 861),
    "ἀφθαρσίαν": ("G", 861),

    # G862 - aphthartos
    "ἄφθαρτος": ("G", 862),
    "ἄφθαρτον": ("G", 862),

    # G2349 - thnetos
    "θνητός": ("G", 2349),
    "θνητὸν": ("G", 2349),

    # G2288 - thanatos
    "θάνατος": ("G", 2288),
    "θανάτου": ("G", 2288),
    "θάνατον": ("G", 2288),

    # G2222 - zoe
    "ζωή": ("G", 2222),
    "ζωὴ": ("G", 2222),
    "ζωῆς": ("G", 2222),
    "ζωὴν": ("G", 2222),
    "ζωήν": ("G", 2222),

    # G622 - apollymi
    "ἀπόλλυμι": ("G", 622),
    "ἀπολέσαι": ("G", 622),
    "ἀπολλύμενοι": ("G", 622),
    "ἀπόλλυται": ("G", 622),

    # G684 - apoleia
    "ἀπώλεια": ("G", 684),
    "ἀπωλείας": ("G", 684),
    "ἀπώλειαν": ("G", 684),

    # G86 - hades
    "ᾅδης": ("G", 86),
    "ᾅδου": ("G", 86),
    "ᾅδῃ": ("G", 86),

    # G1067 - gehenna
    "γέεννα": ("G", 1067),
    "γεέννῃ": ("G", 1067),
    "γέενναν": ("G", 1067),
    "γεέννης": ("G", 1067),

    # G5020 - tartaroo
    "ταρταρόω": ("G", 5020),
    "ταρταρώσας": ("G", 5020),

    # G166 - aionios
    "αἰώνιος": ("G", 166),
    "αἰώνιον": ("G", 166),
    "αἰωνίου": ("G", 166),
    "αἰωνίων": ("G", 166),
    "αἰώνια": ("G", 166),
    "αἰωνίαν": ("G", 166),

    # G165 - aion
    "αἰών": ("G", 165),
    "αἰῶνα": ("G", 165),
    "αἰῶνος": ("G", 165),
    "αἰῶνας": ("G", 165),
    "αἰώνων": ("G", 165),

    # G2837 - koimao
    "κοιμάω": ("G", 2837),
    "κοιμηθέντες": ("G", 2837),
    "ἐκοιμήθη": ("G", 2837),

    # G386 - anastasis
    "ἀνάστασις": ("G", 386),
    "ἀναστάσεως": ("G", 386),
    "ἀνάστασιν": ("G", 386),

    # G928 - basanizo
    "βασανίζω": ("G", 928),
    "βασανισθήσεται": ("G", 928),
    "βασανισθήσονται": ("G", 928),

    # G929 - basanismos
    "βασανισμός": ("G", 929),
    "βασανισμοῦ": ("G", 929),

    # G2851 - kolasis
    "κόλασις": ("G", 2851),
    "κόλασιν": ("G", 2851),

    # G4663 - skolex
    "σκώληξ": ("G", 4663),

    # G3041 - limne
    "λίμνη": ("G", 3041),
    "λίμνην": ("G", 3041),
    "λίμνης": ("G", 3041),

    # G3639 - olethros
    "ὄλεθρος": ("G", 3639),
    "ὄλεθρον": ("G", 3639),
    "ὀλέθρου": ("G", 3639),

    # G4983 - soma
    "σῶμα": ("G", 4983),
    "σώματος": ("G", 4983),
    "σώματι": ("G", 4983),

    # G3498 - nekros
    "νεκρός": ("G", 3498),
    "νεκρόν": ("G", 3498),
    "νεκρῶν": ("G", 3498),
    "νεκροί": ("G", 3498),
    "νεκρούς": ("G", 3498),

    # G3800 - opsonion
    "ὀψώνιον": ("G", 3800),
    "ὀψώνια": ("G", 3800),

    # G5486 - charisma
    "χάρισμα": ("G", 5486),

    # G266 - hamartia
    "ἁμαρτία": ("G", 266),
    "ἁμαρτίας": ("G", 266),
    "ἁμαρτίαν": ("G", 266),

    # G5349 - phthartos
    "φθαρτός": ("G", 5349),
    "φθαρτὸν": ("G", 5349),

    # G5356 - phthora
    "φθορά": ("G", 5356),
    "φθορᾶς": ("G", 5356),

    # G5351 - phtheiro
    "φθείρω": ("G", 5351),

    # G2198 - zao
    "ζάω": ("G", 2198),
    "ζῶσαν": ("G", 2198),
    "ζῶν": ("G", 2198),

    # G2227 - zoopoieo
    "ζωοποιέω": ("G", 2227),
    "ζωοποιοῦν": ("G", 2227),
    "ζωοποιηθήσονται": ("G", 2227),

    # G599 - apothnesko
    "ἀποθνήσκω": ("G", 599),
    "ἀποθνήσκουσιν": ("G", 599),
    "ἀπέθανεν": ("G", 599),

    # G2673 - katargeo
    "καταργέω": ("G", 2673),
    "καταργήσῃ": ("G", 2673),

    # G3952 - parousia
    "παρουσία": ("G", 3952),
    "παρουσίᾳ": ("G", 3952),

    # G2588 - kardia
    "καρδία": ("G", 2588),
    "καρδίας": ("G", 2588),

    # G3857 - paradeisos
    "παράδεισος": ("G", 3857),
    "Παραδείσῳ": ("G", 3857),
    "παραδείσῳ": ("G", 3857),

    # G360 - analyo
    "ἀναλύω": ("G", 360),
    "ἀναλῦσαι": ("G", 360),

    # G1841 - exodos
    "ἔξοδος": ("G", 1841),
    "ἐξόδου": ("G", 1841),

    # G1553 - ekdemeo
    "ἐκδημέω": ("G", 1553),
    "ἐκδημῆσαι": ("G", 1553),

    # G1736 - endemeo
    "ἐνδημέω": ("G", 1736),
    "ἐνδημῆσαι": ("G", 1736),

    # G2920 - krisis
    "κρίσις": ("G", 2920),
    "κρίσιν": ("G", 2920),
    "κρίσεως": ("G", 2920),

    # G3441 - monos
    "μόνος": ("G", 3441),

    # G2217 - zophos
    "ζόφος": ("G", 2217),
    "ζόφου": ("G", 2217),

    # G4636 - skenos
    "σκῆνος": ("G", 4636),
    "σκήνους": ("G", 4636),

    # G623 - Apollyon
    "Ἀπολλύων": ("G", 623),

    # G2618 - katakaio
    "κατακαίω": ("G", 2618),
    "κατακαυθήσεται": ("G", 2618),
    "κατέκαυσεν": ("G", 2618),

    # G2719 - katesthio
    "κατεσθίω": ("G", 2719),
    "κατέφαγεν": ("G", 2719),

    # G1746 - endyo
    "ἐνδύω": ("G", 1746),
    "ἐνδύσασθαι": ("G", 1746),

    # G1902 - ependyo
    "ἐπενδύω": ("G", 1902),
    "ἐπενδύσασθαι": ("G", 1902),

    # G1562 - ekdyo
    "ἐκδύω": ("G", 1562),
    "ἐκδύσασθαι": ("G", 1562),

    # G2647 - katalyo
    "καταλύω": ("G", 2647),
    "καταλυθῇ": ("G", 2647),

    # G615 - apokteino
    "ἀποκτείνω": ("G", 615),
    "ἀποκτεῖναι": ("G", 615),
    "ἀποκτεννόντων": ("G", 615),

    # G1410 - dynamai
    "δύναμαι": ("G", 1410),
    "δυναμένων": ("G", 1410),
    "δυνάμενον": ("G", 1410),

    # G3648 - holokleros
    "ὁλόκληρος": ("G", 3648),
    "ὁλόκληρον": ("G", 3648),

    # G3651 - holoteleis
    "ὁλοτελεῖς": ("G", 3651),
    "ὁλοτελής": ("G", 3651),

    # G5083 - tereo
    "τηρέω": ("G", 5083),
    "τηρηθείη": ("G", 5083),

    # G2924 - kritikos
    "κριτικός": ("G", 2924),

    # G3311 - merismos
    "μερισμός": ("G", 3311),
    "μερισμοῦ": ("G", 3311),

    # G719 - harmos
    "ἁρμός": ("G", 719),
    "ἁρμῶν": ("G", 719),

    # G3452 - myelos
    "μυελός": ("G", 3452),
    "μυελῶν": ("G", 3452),

    # G1761 - enthymesis
    "ἐνθύμησις": ("G", 1761),
    "ἐνθυμήσεων": ("G", 1761),

    # G1771 - ennoia
    "ἔννοια": ("G", 1771),
    "ἐννοιῶν": ("G", 1771),

    # G4577 - seira
    "σειρά": ("G", 4577),
    "σειροῖς": ("G", 4577),

    # G3860 - paradidomi
    "παραδίδωμι": ("G", 3860),
    "παρέδωκεν": ("G", 3860),

    # G5339 - pheidomai
    "φείδομαι": ("G", 5339),
    "ἐφείσατο": ("G", 5339),

    # G4152 - pneumatikos
    "πνευματικός": ("G", 4152),
    "πνευματικόν": ("G", 4152),

    # G4638 - skenoma
    "σκήνωμα": ("G", 4638),
    "σκηνώματος": ("G", 4638),

    # G1096 - ginomai
    "Ἐγένετο": ("G", 1096),
    "γίνομαι": ("G", 1096),

    # G4931 - synteleo
    "συντελέω": ("G", 4931),

    # G609 - apokopto
    "ἀποκόπτω": ("G", 609),
}


def build_url(prefix, num):
    """Build BLB URL from prefix (H/G) and number."""
    if prefix == "H":
        return BLB_HEBREW_URL.format(num=num)
    else:
        return BLB_GREEK_URL.format(num=num)


def build_patterns():
    """Build regex patterns from WORD_MAP."""
    translit_map = {}
    unicode_map = {}

    for word, (prefix, num) in WORD_MAP.items():
        if all(ord(c) < 256 for c in word):
            translit_map[word] = (prefix, num)
        else:
            unicode_map[word] = (prefix, num)

    # Transliteration pattern: word boundaries, case-insensitive
    # Sort longest first to match longest form first
    translit_words = sorted(translit_map.keys(), key=len, reverse=True)
    translit_pattern = None
    if translit_words:
        translit_pattern = re.compile(
            r'\b(' + '|'.join(re.escape(w) for w in translit_words) + r')\b',
            re.IGNORECASE
        )

    # Unicode pattern: exact match, sorted longest first
    unicode_words = sorted(unicode_map.keys(), key=len, reverse=True)
    unicode_pattern = None
    if unicode_words:
        unicode_pattern = re.compile(
            r'(' + '|'.join(re.escape(w) for w in unicode_words) + r')'
        )

    return translit_map, unicode_map, translit_pattern, unicode_pattern


def is_in_existing_link(text, match_start, match_end):
    """Check if the match position is inside an existing markdown link."""
    # Check if inside [text] part
    bracket_depth = 0
    for i in range(match_start - 1, -1, -1):
        if text[i] == ']':
            bracket_depth += 1
        elif text[i] == '[':
            if bracket_depth == 0:
                return True
            bracket_depth -= 1

    # Check if inside (url) part of [text](url)
    paren_depth = 0
    for i in range(match_start - 1, -1, -1):
        if text[i] == ')':
            paren_depth += 1
        elif text[i] == '(':
            if paren_depth == 0:
                for j in range(i - 1, -1, -1):
                    if text[j] in ' \t':
                        continue
                    if text[j] == ']':
                        return True
                    break
            paren_depth -= 1

    # Check if inside {:target="_blank"} attribute
    # Look backward for {: and forward for }
    for i in range(match_start - 1, max(match_start - 20, -1), -1):
        if text[i] == '{':
            # Check if there's a closing } after our match
            for j in range(match_end, min(match_end + 30, len(text))):
                if text[j] == '}':
                    return True
                if text[j] == '\n':
                    break
            break
        if text[i] == '}' or text[i] == '\n':
            break

    return False


def is_in_table_header(line):
    """Check if line is a table separator (|---|---|)."""
    return bool(re.match(r'^\s*\|[\s\-:|]+\|\s*$', line))


def add_word_links_to_line(line, translit_map, unicode_map, translit_pat, unicode_pat):
    """Add BLB links to Hebrew/Greek words in a single line."""
    # Find all matches from both patterns
    matches = []

    if translit_pat:
        for m in translit_pat.finditer(line):
            word = m.group(1)
            key = word.lower()
            # Find the right key (case-insensitive lookup)
            entry = None
            for k, v in translit_map.items():
                if k.lower() == key:
                    entry = v
                    break
            if entry:
                matches.append((m.start(), m.end(), word, entry[0], entry[1]))

    if unicode_pat:
        for m in unicode_pat.finditer(line):
            word = m.group(1)
            if word in unicode_map:
                entry = unicode_map[word]
                matches.append((m.start(), m.end(), word, entry[0], entry[1]))

    if not matches:
        return line, 0

    # Sort by start position, then by length (longest first for overlaps)
    matches.sort(key=lambda x: (x[0], -(x[1] - x[0])))

    # Remove overlapping matches (keep the first/longest)
    filtered = []
    last_end = -1
    for start, end, word, prefix, num in matches:
        if start >= last_end:
            filtered.append((start, end, word, prefix, num))
            last_end = end

    # Build result string
    result = []
    last_end = 0
    count = 0

    for start, end, word, prefix, num in filtered:
        # Skip if inside an existing markdown link or attribute
        if is_in_existing_link(line, start, end):
            result.append(line[last_end:end])
            last_end = end
            continue

        # Build the link
        url = build_url(prefix, num)
        link = f'[{word}]({url}){{:target="_blank"}}'

        result.append(line[last_end:start])
        result.append(link)
        last_end = end
        count += 1

    result.append(line[last_end:])
    return ''.join(result), count


def process_file(filepath, translit_map, unicode_map, translit_pat, unicode_pat, dry_run=False):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    total_links = 0
    in_code_block = False

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            new_lines.append(line)
            continue

        if is_in_table_header(line):
            new_lines.append(line)
            continue

        new_line, count = add_word_links_to_line(
            line, translit_map, unicode_map, translit_pat, unicode_pat
        )
        new_lines.append(new_line)
        total_links += count

    new_content = '\n'.join(new_lines)

    if total_links > 0 and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return total_links


# Pattern for reverting word links (excludes Strong's number links H1234/G1234)
WORD_LINK_PATTERN = re.compile(
    r'\[([^\]]+?)\]'
    r'\(https://www\.blueletterbible\.org/lexicon/[hg]\d{1,5}/kjv/(?:wlc|tr)/0-1/\)'
    r'\{:target="_blank"\}'
)
STRONGS_DISPLAY = re.compile(r'^[HG]\d{1,5}$')


def revert_file(filepath):
    """Remove word links, restoring plain words. Does not touch Strong's number links."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    def replace_word_link(m):
        display_text = m.group(1)
        # Don't revert Strong's number links (handled by add_blb_links.py)
        if STRONGS_DISPLAY.match(display_text):
            return m.group(0)
        return display_text

    new_content = WORD_LINK_PATTERN.sub(replace_word_link, content)
    # Count only word link changes
    word_links = [m for m in WORD_LINK_PATTERN.finditer(content)
                  if not STRONGS_DISPLAY.match(m.group(1))]
    changes = len(word_links)

    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return changes


def get_all_md_files():
    """Get all markdown files in the studies directory."""
    files = []
    for root, dirs, filenames in os.walk(DOCS_DIR):
        for filename in filenames:
            if filename.endswith('.md'):
                files.append(Path(root) / filename)
    return sorted(files)


def collect_stats(translit_map, unicode_map, translit_pat, unicode_pat):
    """Collect statistics about word occurrences."""
    word_counts = {}

    for filepath in get_all_md_files():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        study = filepath.parent.name
        if study == 'raw-data':
            study = filepath.parent.parent.name

        lines = content.split('\n')
        in_code_block = False

        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            if translit_pat:
                for m in translit_pat.finditer(line):
                    word = m.group(1).lower()
                    for k in translit_map:
                        if k.lower() == word:
                            word = k
                            break
                    if word not in word_counts:
                        word_counts[word] = {"count": 0, "studies": set()}
                    word_counts[word]["count"] += 1
                    word_counts[word]["studies"].add(study)

            if unicode_pat:
                for m in unicode_pat.finditer(line):
                    word = m.group(1)
                    if word not in word_counts:
                        word_counts[word] = {"count": 0, "studies": set()}
                    word_counts[word]["count"] += 1
                    word_counts[word]["studies"].add(study)

    return word_counts


def main():
    parser = argparse.ArgumentParser(
        description="Add BLB links to Hebrew/Greek words"
    )
    parser.add_argument('--dry-run', action='store_true',
                        help="Show what would change without modifying files")
    parser.add_argument('--revert', action='store_true',
                        help="Remove all word links (keep Strong's number links)")
    parser.add_argument('--stats', action='store_true',
                        help="Show statistics only")
    args = parser.parse_args()

    translit_map, unicode_map, translit_pat, unicode_pat = build_patterns()

    if args.stats:
        word_counts = collect_stats(translit_map, unicode_map, translit_pat, unicode_pat)

        # Split into categories
        hebrew_translit = {k: v for k, v in word_counts.items()
                          if k in translit_map and translit_map[k][0] == 'H'}
        greek_translit = {k: v for k, v in word_counts.items()
                         if k in translit_map and translit_map[k][0] == 'G'}
        unicode_words = {k: v for k, v in word_counts.items()
                        if k in unicode_map}

        print(f"Hebrew transliterations: {len(hebrew_translit)} unique words, "
              f"{sum(v['count'] for v in hebrew_translit.values())} occurrences")
        print(f"Greek transliterations: {len(greek_translit)} unique words, "
              f"{sum(v['count'] for v in greek_translit.values())} occurrences")
        print(f"Unicode words: {len(unicode_words)} unique forms, "
              f"{sum(v['count'] for v in unicode_words.values())} occurrences")
        total = sum(v['count'] for v in word_counts.values())
        print(f"\nTotal: {len(word_counts)} unique forms, {total} occurrences")

        print("\nTop 30 by frequency:")
        for word, data in sorted(word_counts.items(),
                                 key=lambda x: x[1]['count'], reverse=True)[:30]:
            prefix, num = WORD_MAP.get(word, WORD_MAP.get(word.lower(), ("?", 0)))
            studies = ', '.join(sorted(data['studies']))
            print(f"  {word:20s} ({prefix}{num:>5d}) x{data['count']:>4d}  [{studies}]")

        return

    files = get_all_md_files()
    total_changes = 0

    if args.revert:
        print("Reverting word links (keeping Strong's number links)...")
        for filepath in files:
            changes = revert_file(filepath)
            if changes > 0:
                rel = filepath.relative_to(DOCS_DIR)
                print(f"  {rel}: reverted {changes} word links")
                total_changes += changes
        print(f"\nTotal: reverted {total_changes} word links")
    else:
        action = "Would add" if args.dry_run else "Added"
        if args.dry_run:
            print("DRY RUN - no files will be modified\n")

        for filepath in files:
            links_added = process_file(
                filepath, translit_map, unicode_map,
                translit_pat, unicode_pat, dry_run=args.dry_run
            )
            if links_added > 0:
                rel = filepath.relative_to(DOCS_DIR)
                print(f"  {rel}: {action} {links_added} word links")
                total_changes += links_added

        print(f"\nTotal: {action.lower()} {total_changes} word links")


if __name__ == '__main__':
    main()
