from itertools import combinations

RANKS = "23456789TJQKA"
RANK_VALUE = {r: i for i, r in enumerate(RANKS, start=2)}

HAND_ORDER = {
    "High Card": 0,
    "One Pair": 1,
    "Two Pair": 2,
    "Three of a Kind": 3,
    "Straight": 4,
    "Flush": 5,
    "Full House": 6,
    "Four of a Kind": 7,
    "Straight Flush": 8,
}


def classify_5(cards):
    # cards: ["Ah","Kd","Qs","Jc","Tc"]
    ranks = [c[0].upper() for c in cards]
    suits = [c[1].lower() for c in cards]

    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    counts = sorted(rank_counts.values(), reverse=True)
    unique_vals = sorted({RANK_VALUE[r] for r in ranks}, reverse=True)

    is_flush = len(set(suits)) == 1

    # Straight detection (including wheel A2345)
    sorted_vals = sorted({RANK_VALUE[r] for r in ranks})
    is_straight = False
    if len(sorted_vals) == 5 and sorted_vals[-1] - sorted_vals[0] == 4:
        is_straight = True
    # Wheel: A2345 (treat as 5-high straight)
    if set(ranks) == set("A2345"):
        is_straight = True
        sorted_vals = [5, 4, 3, 2, 1]

    if is_straight and is_flush:
        label = "Straight Flush"
    elif counts == [4, 1]:
        label = "Four of a Kind"
    elif counts == [3, 2]:
        label = "Full House"
    elif is_flush:
        label = "Flush"
    elif is_straight:
        label = "Straight"
    elif counts == [3, 1, 1]:
        label = "Three of a Kind"
    elif counts == [2, 2, 1]:
        label = "Two Pair"
    elif counts == [2, 1, 1, 1]:
        label = "One Pair"
    else:
        label = "High Card"

    cat_score = HAND_ORDER[label]
    kicker_score = sorted_vals[::-1]
    return label, (cat_score, kicker_score)


def best_5_of_n(cards):
    best_label = None
    best_score = None

    for combo in combinations(cards, 5):
        label, score = classify_5(list(combo))
        if best_score is None or score > best_score:
            best_score = score
            best_label = label

    return best_label


def evaluate_hand(all_cards):
    """
    all_cards: list like ["Ah","Kd","Qs","Jc","Tc"]
    Supports 5 to 7 cards total.
    """
    n = len(all_cards)
    if n < 5 or n > 7:
        return "Hand evaluation currently supports 5 to 7 cards total (hand + board)."

    if n == 5:
        label, _ = classify_5(all_cards)
        return f"Hand Type: {label}"

    label = best_5_of_n(all_cards)
    return f"Hand Type: {label}"
