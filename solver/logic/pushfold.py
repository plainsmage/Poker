# Real push/fold engine driven by lookup tables.
# Fill PUSH_RANGES with your actual charts.

# Example structure:
# PUSH_RANGES[stack_band][position] = set of combos like "AK", "AQ", "TT", etc.

PUSH_RANGES = {
    "0-6": {
        "UTG": {"AA", "KK", "QQ", "JJ", "TT", "AK", "AQ"},
        "MP":  {"AA", "KK", "QQ", "JJ", "TT", "AK", "AQ", "AJ"},
        "CO":  {"AA", "KK", "QQ", "JJ", "TT", "99", "AK", "AQ", "AJ", "AT", "KQ"},
        "BTN": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "AK", "AQ", "AJ", "AT", "KQ", "KJ", "QJ"},
        "SB":  {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "AK", "AQ", "AJ", "AT", "KQ", "KJ", "QJ"},
        "BB":  {"AA", "KK", "QQ", "JJ", "TT", "AK", "AQ"},  # vs unopened pot, adjust as needed
    },
    "7-12": {
        "UTG": {"AA", "KK", "QQ", "JJ", "TT", "AK", "AQ"},
        "MP":  {"AA", "KK", "QQ", "JJ", "TT", "AK", "AQ", "AJ"},
        "CO":  {"AA", "KK", "QQ", "JJ", "TT", "99", "AK", "AQ", "AJ", "AT", "KQ"},
        "BTN": {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "AK", "AQ", "AJ", "AT", "KQ", "KJ", "QJ"},
        "SB":  {"AA", "KK", "QQ", "JJ", "TT", "99", "88", "AK", "AQ", "AJ", "AT", "KQ", "KJ", "QJ"},
        "BB":  {"AA", "KK", "QQ", "JJ", "TT", "AK", "AQ"},
    },
}


def pushfold_decision(position, hand, stack):
    """
    Uses real push/fold ranges from PUSH_RANGES.
    """

    combo = normalize_combo(hand)
    band = stack_band(stack)

    # If we don't have a band or position defined, fall back to a generic message
    if band not in PUSH_RANGES or position not in PUSH_RANGES[band]:
        return f"No range defined for {position} at {stack}BB (band {band})."

    allowed = PUSH_RANGES[band][position]

    if combo in allowed:
        return f"Jam ({combo} is in the {band}BB shove range for {position})."

    return f"Fold ({combo} is NOT in the {band}BB shove range for {position})."


def normalize_combo(hand):
    """
    Convert 'As Kh' -> 'AK', '7d 7c' -> '77'.
    Suits are ignored for push/fold charts.
    """
    c1, c2 = hand.split()
    r1, r2 = c1[0], c2[0]
    # Sort ranks so AK and KA both become AK
    ranks = sorted([r1, r2], reverse=True)
    return "".join(ranks)


def stack_band(stack):
    """
    Map exact stack size to a band key used in PUSH_RANGES.
    Adjust thresholds to match your charts.
    """
    if stack <= 6:
        return "0-6"
    if 7 <= stack <= 12:
        return "7-12"
    return "13+"

