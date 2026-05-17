# 🛡️ RUBRIC WATCHDOG V2.1 (SOUL & TRADITION)
# Валидатор рубрик для концепции V2.0

VALID_RUBRICS = {
    "AC": [
        "#TIME_WHEEL", "#STAR_MAP", "#SACRED_PERSON", "#SYMBOL_CODE",
        "#RITUAL_KEY", "#HISTORY_MYSTERY", "#ART_SOUL", "#NIGHT_OMEN",
        "#ALCHEMY_OF_SYNC", "#ARCHITECT_MEMORY", "#MIND_JUBILEE", "#STATE_GENESIS", "#NIGHT_REFLECTION" # Legacy
    ],
    "NB": [
        "#PLACE_OF_POWER", "#CRAFT_MAGIC", "#FOLK_LEGEND", "#TRADITION_KEEPER",
        "#COSTUME_CODE", "#NATURE_RHYTHM", "#STREET_VIBE", "#VISUAL_ESCAPE",
        "#MARKET_DAY", "#CRAFT_TRADITION", "#VOICE_OF_STREET", "#FOLK_STORY_NIGHT", "#VOGUE_VISUAL" # Legacy
    ],
    "SW": [
        "#SIGNATURE_CAKE", "#VINTAGE_BAKE", "#SEASON_TASTE", "#SPICE_MAGIC",
        "#CHOCOLATE_RITUAL", "#COZY_DRINK", "#GASTRO_HISTORY", "#SWEET_DREAM",
        "#FLAVOR_PAIRING", "#HEDONIST_RITUAL", "#PASTRY_TECHNIQUE" # Legacy
    ],
    "YV": [
        "#NEWS", "#LIVE_NEWS", "#ANALYSIS", "#PREDICTION", "#SPOTLIGHT",
        "#WEEK_AHEAD", "#CHART_RESULTS", "#CHART_ANNOUNCE", "#STAGE_DIVING",
        "#POLL", "#REVIEW", "#HYPEMETER", "#RESULTS", "#CHART_UPDATE"
    ]
}

def check_rubric(channel, content):
    for rubric in VALID_RUBRICS.get(channel, []):
        if rubric in content:
            return True
    return False
