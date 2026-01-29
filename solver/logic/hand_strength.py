# --- START hand_strength.py ---
import itertools

RANK_ORDER = "23456789TJQKA"
SUIT_SYMBOLS = {
    "C": "♣",
    "D": "♦",
    "H": "♥",
    "S": "♠"
}

def rank_value(card):
    return RANK_ORDER.index(card[0])


def is_flush(cards):
    suits = [c[1] for c in cards]
    return len(set(suits)) == 1


def is_straight(cards):
    ranks = sorted([rank_value(c) for c in cards])
    return ranks == list(range(ranks[0], ranks[0] + 5))


def classify_hand(cards):
    ranks = [c[0] for c in cards]
    suits = [c[1] for c in cards]
    rank_counts = {r: ranks.count(r) for r in ranks}

    is_flush_hand = len(set(suits)) == 1
    sorted_vals = sorted([rank_value(c) for c in cards])
    is_straight_hand = sorted_vals == list(range(sorted_vals[0], sorted_vals[0] + 5))

    if is_flush_hand and sorted_vals == [8, 9, 10, 11, 12]:
        return "Royal Flush"
    if is_flush_hand and is_straight_hand:
        return "Straight Flush"
    if 4 in rank_counts.values():
        return "Four of a Kind"
    if sorted(rank_counts.values()) == [2, 3]:
        return "Full House"
    if is_flush_hand:
        return "Flush"
    if is_straight_hand:
        return "Straight"
    if 3 in rank_counts.values():
        return "Three of a Kind"
    if list(rank_counts.values()).count(2) == 2:
        return "Two Pair"
    if 2 in rank_counts.values():
        return "Pair"
    return "High Card"


def best_five_from_seven(cards):
    best = None
    best_rank = None

    for combo in itertools.combinations(cards, 5):
        hand_type = classify_hand(combo)
        rank_index = [
            "High Card", "Pair", "Two Pair", "Three of a Kind",
            "Straight", "Flush", "Full House", "Four of a Kind",
            "Straight Flush", "Royal Flush"
        ].index(hand_type)

        if best is None or best_rank is None or rank_index > best_rank:
            best = combo
            best_rank = rank_index

    return list(best), classify_hand(best)


def simulate_future_outs(hand, board):
    used = set(hand + board)
    ranks = list(RANK_ORDER)
    suits = ["C", "D", "H", "S"]

    deck = [r + s for r in ranks for s in suits if (r + s) not in used]

    base_best, base_type = best_five_from_seven(hand + board)

    future = {"C": [], "D": [], "H": [], "S": []}

    for card in deck:
        new_board = board + [card]
        best5, new_type = best_five_from_seven(hand + new_board)

        if new_type != base_type:
            suit = card[1]
            suit_icon = SUIT_SYMBOLS[suit]
            future[suit].append((card, suit_icon, new_type))

    return future


def evaluate_best_possible_flop(hand_cards, board_cards):
    if len(board_cards) < 3:
        return None, "Board too small", {}

    flop = board_cards[:3]
    best5, best_type = best_five_from_seven(hand_cards + flop)
    future = simulate_future_outs(hand_cards, flop)

    return best5, best_type, future


def evaluate_best_possible_turn(hand_cards, board_cards):
    if len(board_cards) < 4:
        return None, "Board too small", {}

    turn = board_cards[:4]
    best5, best_type = best_five_from_seven(hand_cards + turn)
    future = simulate_future_outs(hand_cards, turn)

    return best5, best_type, future


def evaluate_best_possible_river(hand_cards, board_cards):
    if len(board_cards) < 5:
        return None, "Board too small", {}

    river = board_cards[:5]
    best5, best_type = best_five_from_seven(hand_cards + river)
    future = {}  # no future outs on river

    return best5, best_type, future


def evaluate_hand(hand_str, board_str):
    hand = hand_str.upper().replace(" ", "")
    board = board_str.upper().replace(" ", "")

    hand_cards = [hand[i:i+2] for i in range(0, len(hand), 2)]
    board_cards = [board[i:i+2] for i in range(0, len(board), 2)]

    best5, best_type = best_five_from_seven(hand_cards + board_cards)
    future = simulate_future_outs(hand_cards, board_cards)

    return {
        "best5": best5,
        "best_type": best_type,
        "future": future
    }

# --- END hand_strength.py ---
# --- START hand_strength.py ---
import itertools

RANKS = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    '10': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14,
}

SUITS = ['C', 'D', 'H', 'S']


def _normalize_card(card):
    c = card.upper().replace(" ", "")
    if not c:
        return None

    if len(c) == 3 and c.startswith("10"):
        rank = 'T'
        suit = c[2]
    elif len(c) == 2:
        rank = c[0]
        suit = c[1]
        if rank == '0':
            rank = 'T'
    else:
        return None

    if rank not in RANKS or suit not in SUITS:
        return None

    return rank + suit


def _normalize_cards(cards):
    out = []
    for c in cards:
        nc = _normalize_card(c)
        print("NORMALIZE:", repr(c), "->", repr(nc))
        if nc:
            out.append(nc)
    print("FINAL NORMALIZED LIST:", out)
    return out
def _card_rank(card):
    return RANKS[card[0]]


def _hand_rank_5(cards5):
    ranks = sorted((_card_rank(c) for c in cards5), reverse=True)
    suits = [c[1] for c in cards5]

    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1

    count_rank = sorted(((cnt, r) for r, cnt in counts.items()), reverse=True)

    is_flush = len(set(suits)) == 1

    unique_ranks = sorted(set(ranks), reverse=True)
    is_straight = False
    high_straight = None

    if len(unique_ranks) >= 5:
        for i in range(len(unique_ranks) - 4 + 1):
            window = unique_ranks[i:i+5]
            if window[0] - window[4] == 4:
                is_straight = True
                high_straight = window[0]
                break

        if not is_straight and set([14, 5, 4, 3, 2]).issubset(set(unique_ranks)):
            is_straight = True
            high_straight = 5

    if is_flush and is_straight:
        flush_suit = suits[0]
        flush_cards = [c for c in cards5 if c[1] == flush_suit]
        flush_ranks = sorted((_card_rank(c) for c in flush_cards), reverse=True)
        unique_flush_ranks = sorted(set(flush_ranks), reverse=True)

        sf = False
        sf_high = None

        if len(unique_flush_ranks) >= 5:
            for i in range(len(unique_flush_ranks) - 4 + 1):
                window = unique_flush_ranks[i:i+5]
                if window[0] - window[4] == 4:
                    sf = True
                    sf_high = window[0]
                    break
            if not sf and set([14, 5, 4, 3, 2]).issubset(set(unique_flush_ranks)):
                sf = True
                sf_high = 5

        if sf:
            return (8, sf_high, sorted(ranks, reverse=True))

    if count_rank[0][0] == 4:
        four = count_rank[0][1]
        kicker = max(r for r in ranks if r != four)
        return (7, four, kicker)

    if count_rank[0][0] == 3 and count_rank[1][0] >= 2:
        three = count_rank[0][1]
        pair = count_rank[1][1]
        return (6, three, pair)

    if is_flush:
        return (5, ranks)

    if is_straight:
        return (4, high_straight)

    if count_rank[0][0] == 3:
        three = count_rank[0][1]
        kickers = sorted((r for r in ranks if r != three), reverse=True)
        return (3, three, kickers)

    if count_rank[0][0] == 2 and count_rank[1][0] == 2:
        high_pair = max(count_rank[0][1], count_rank[1][1])
        low_pair = min(count_rank[0][1], count_rank[1][1])
        kicker = max(r for r in ranks if r != high_pair and r != low_pair)
        return (2, high_pair, low_pair, kicker)

    if count_rank[0][0] == 2:
        pair = count_rank[0][1]
        kickers = sorted((r for r in ranks if r != pair), reverse=True)
        return (1, pair, kickers)

    return (0, ranks)
def _hand_type_from_rank(rank_tuple):
    category = rank_tuple[0]
    return [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush",
    ][category]


def _best_5_from_7(cards):
    best_rank = None
    best_hand = None

    for combo in itertools.combinations(cards, 5):
        r = _hand_rank_5(list(combo))
        if best_rank is None or r > best_rank:
            best_rank = r
            best_hand = list(combo)

    if best_hand is None:
        return None, None

    best_type = _hand_type_from_rank(best_rank)
    return best_hand, best_type


def _future_stub(street, hand_cards, board_cards):
    return {
        "street": street,
        "message": "Future simulation placeholder – evaluator is working.",
        "hand": hand_cards,
        "board": board_cards,
    }


def evaluate_best_possible_flop(hand_cards, board_cards):
    h = _normalize_cards(hand_cards)
    b = _normalize_cards(board_cards)
    if len(h) != 2 or len(b) != 3:
        return None, None, {}
    combined = h + b
    best5, best_type = _best_5_from_7(combined)
    return best5, best_type, _future_stub("flop", h, b)


def evaluate_best_possible_turn(hand_cards, board_cards):
    h = _normalize_cards(hand_cards)
    b = _normalize_cards(board_cards)
    if len(h) != 2 or len(b) != 4:
        return None, None, {}
    combined = h + b
    best5, best_type = _best_5_from_7(combined)
    return best5, best_type, _future_stub("turn", h, b)


def evaluate_best_possible_river(hand_cards, board_cards):
    h = _normalize_cards(hand_cards)
    b = _normalize_cards(board_cards)
    if len(h) != 2 or len(b) < 5:
        return None, None, {}
    combined = h + b[:5]
    best5, best_type = _best_5_from_7(combined)
    return best5, best_type, _future_stub("river", h, b[:5])
# --- END hand_strength.py ---
