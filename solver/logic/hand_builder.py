def build_hand(cleaned):
    c1 = cleaned["hand_rank_1"] + cleaned["hand_suit_1"]
    c2 = cleaned["hand_rank_2"] + cleaned["hand_suit_2"]
    return f"{c1} {c2}"

