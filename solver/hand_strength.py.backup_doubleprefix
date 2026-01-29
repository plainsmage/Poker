"""
hand_strength.py
Micro‑chunk rebuild
Chunk 1A
"""
# --- module logger initialization (inserted to avoid NameError) ---
import logging
_logger = logging.getLogger('solver.hand_strength')
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('[HS-DEBUG] %(message)s'))
    _logger.addHandler(_handler)
_logger.setLevel(logging.INFO)
def set_debug(enabled: bool):
    _logger.setLevel(logging.DEBUG if enabled else logging.INFO)
# --- end inserted logger init ---


from itertools import combinations

# Rank ordering
RANK_ORDER = "23456789TJQKA"
RANK_INDEX = {r: i for i, r in enumerate(RANK_ORDER)}

def _rank_value(card):
    """Return numeric rank index."""
    return RANK_INDEX[card[0]]

if _logger.isEnabledFor(logging.DEBUG):
    print("Loaded rank helpers")
def _classify_five(cards):
    """
    Classify exactly 5 cards.
    Returns:
        category, name, tiebreak, cards
    """
    print("[HS-DEBUG] Classifying:", cards)

    # Extract ranks and suits
    ranks = [_rank_value(c) for c in cards]
    suits = [c[1] for c in cards]

    # Sort ranks high to low
    ranks_sorted = sorted(ranks, reverse=True)

    # Flush check
    is_flush = (len(set(suits)) == 1)

    # Straight check
    r_sorted_low = sorted(ranks)
    is_wheel = (r_sorted_low == [0,1,2,3,12])
    if is_wheel:
        is_straight = True
        straight_high = 3
    else:
        diffs = []
        for i in range(4):
            diffs.append(r_sorted_low[i+1] - r_sorted_low[i])
        is_straight = all(d == 1 for d in diffs)
        straight_high = r_sorted_low[-1] if is_straight else None

    # Count ranks
    rank_counts = {}
    for r in ranks:
        rank_counts[r] = rank_counts.get(r, 0) + 1

    counts = sorted(rank_counts.values(), reverse=True)
    # Straight Flush
    if is_straight and is_flush:
        return 8, "Straight Flush", [straight_high], cards

    # Four of a Kind
    if counts == [4,1]:
        four_rank = None
        for r in rank_counts:
            if rank_counts[r] == 4:
                four_rank = r
        kicker = None
        for r in ranks_sorted:
            if r != four_rank:
                kicker = r
                break
        return 7, "Four of a Kind", [four_rank, kicker], cards

    # Full House
    if counts == [3,2]:
        three_rank = None
        pair_rank = None
        for r in rank_counts:
            if rank_counts[r] == 3:
                three_rank = r
            elif rank_counts[r] == 2:
                pair_rank = r
        return 6, "Full House", [three_rank, pair_rank], cards

    # Flush
    if is_flush:
        return 5, "Flush", ranks_sorted, cards

    # Straight
    if is_straight:
        return 4, "Straight", [straight_high], cards

    # Three of a Kind
    if counts == [3,1,1]:
        three_rank = None
        for r in rank_counts:
            if rank_counts[r] == 3:
                three_rank = r
        kickers = []
        for r in ranks_sorted:
            if r != three_rank:
                kickers.append(r)
        return 3, "Three of a Kind", [three_rank] + kickers, cards

    # Two Pair
    if counts == [2,2,1]:
        pairs = []
        kicker = None
        for r in rank_counts:
            if rank_counts[r] == 2:
                pairs.append(r)
        pairs = sorted(pairs, reverse=True)
        for r in ranks_sorted:
            if r not in pairs:
                kicker = r
                break
        return 2, "Two Pair", pairs + [kicker], cards

    # One Pair
    if counts == [2,1,1,1]:
        pair_rank = None
        for r in rank_counts:
            if rank_counts[r] == 2:
                pair_rank = r
        kickers = []
        for r in ranks_sorted:
            if r != pair_rank:
                kickers.append(r)
        return 1, "One Pair", [pair_rank] + kickers, cards

    # High Card
    return 0, "High Card", ranks_sorted, cards
def _best_five_from_seven(cards):
    """
    Choose best 5 from 7 cards.
    Returns:
        category, name, tiebreak, best_five
    """
    print("[HS-DEBUG] Evaluating best 5 from 7:", cards)

    best_cat = -1
    best_name = ""
    best_tb = []
    best_five = None

    # Generate all 21 combos
    for combo in combinations(cards, 5):
        cat, name, tb, _ = _classify_five(list(combo))

        if cat > best_cat:
            best_cat = cat
            best_name = name
            best_tb = tb
            best_five = list(combo)
            print("[HS-DEBUG] New best:", name, best_five)

        elif cat == best_cat and tb > best_tb:
            best_name = name
            best_tb = tb
            best_five = list(combo)
            print("[HS-DEBUG] Tiebreak improved:", name, best_five)

    return best_cat, best_name, best_tb, best_five
def evaluate_hand(hand_cards, board_cards):
    """
    Evaluate hero's current hand.
    Handles:
        <5 cards  -> not enough
        5 cards   -> classify directly
        6 cards   -> best 5 of 6
        7 cards   -> best 5 of 7
    """
    all_cards = hand_cards + board_cards
    n = len(all_cards)

    print("[HS-DEBUG] evaluate_hand: total cards =", n)
    print("[HS-DEBUG] Hand:", hand_cards)
    print("[HS-DEBUG] Board:", board_cards)

    # Not enough cards
    if n < 5:
        print("[HS-DEBUG] Not enough cards to evaluate")
        return {
            "hand_cards": hand_cards,
            "board_cards": board_cards,
            "all_cards": all_cards,
            "best_five": [],
            "category": -1,
            "hand_type": "Not enough cards",
            "hand_name": "Not enough cards",
            "tiebreak": [],
        }

    # Exactly 5 cards
    if n == 5:
        cat, name, tb, best_five = _classify_five(all_cards)
        print("[HS-DEBUG] 5-card result:", name, best_five)
        return {
            "hand_cards": hand_cards,
            "board_cards": board_cards,
            "all_cards": all_cards,
            "best_five": best_five,
            "category": cat,
            "hand_type": name,
            "hand_name": name,
            "tiebreak": tb,
        }

    # 6 or 7 cards
    if n in (6, 7):
        cat, name, tb, best_five = _best_five_from_seven(all_cards[:7])
        print("[HS-DEBUG] Best from", n, "cards:", name, best_five)
        print("[HS-DEBUG] Best from", n, "cards:", name, best_five)
        return {
            "hand_cards": hand_cards,
            "board_cards": board_cards,
            "all_cards": all_cards,
            "best_five": best_five,
            "category": cat,
            "hand_type": name,
            "hand_name": name,
            "tiebreak": tb,
        }

    # Fallback (should not happen)
    print("[HS-DEBUG] Unexpected card count")
    return {
        "hand_cards": hand_cards,
        "board_cards": board_cards,
        "all_cards": all_cards,
        "best_five": [],
        "category": -1,
        "hand_type": "Error",
        "hand_name": "Error",
        "tiebreak": [],
    }

def compute_best_possible_hand(hole, board):
    """
    Compute the best possible 5-card hand (nuts) given
    hero hole cards and current board (0-5 cards).
    Returns a dict with the best category, name, tiebreak,
    and the best five-card combination found.
    """
    print("[HS-DEBUG] compute_best_possible_hand: hole", hole, "board", board)

    # Build full deck
    deck = []
    for r in RANK_ORDER:
        for s in "cdhs":
            deck.append(r + s)

    # Remove known cards
    known = set(hole + board)
    deck = [c for c in deck if c not in known]

    # Number of board cards
    b = len(board)
    if b > 5:
        print("[HS-DEBUG] Too many board cards")
        return None
    # How many cards to add to reach 5
    to_add = 5 - b

    # If board already complete, just evaluate current
    if to_add == 0:
        cat, name, tb, best_five = _best_five_from_seven(hole + board)
        return {
            "best_category": cat,
            "best_name": name,
            "best_tiebreak": tb,
            "best_five": best_five,
            "completion": [],
        }

    # Iterate all possible completions
    from itertools import combinations as combs
    best_overall = {
        "best_category": -1,
        "best_name": None,
        "best_tiebreak": [],
        "best_five": None,
        "completion": None,
    }

    for extra in combs(deck, to_add):
        full_board = board + list(extra)
        result = evaluate_hand(hole, full_board)
        cat = result["category"]
        tb = result["tiebreak"]

        if cat > best_overall["best_category"]:
            best_overall["best_category"] = cat
            best_overall["best_name"] = result["hand_name"]
            best_overall["best_tiebreak"] = tb
            best_overall["best_five"] = result["best_five"]
            best_overall["completion"] = list(extra)
            print("[HS-DEBUG] New nuts via", extra, "->", result["hand_name"])

        elif cat == best_overall["best_category"] and tb > best_overall["best_tiebreak"]:
            best_overall["best_name"] = result["hand_name"]
            best_overall["best_tiebreak"] = tb
            best_overall["best_five"] = result["best_five"]
            best_overall["completion"] = list(extra)
            print("[HS-DEBUG] Tiebreak nuts improved via", extra)

    return best_overall
# Exports
__all__ = [
    "evaluate_hand",
    "compute_best_possible_hand",
    "_classify_five",
    "_best_five_from_seven",
]

# Simple test harness
if __name__ == "__main__":
    # Quick smoke tests
    hole = ["As", "Kd"]
    board = ["Ah", "Ad", "Ac"]
    print("[HS-DEBUG] Smoke test: hole", hole, "board", board)
    res = evaluate_hand(hole, board)
    print("[HS-DEBUG] evaluate_hand result:", res)

    # Nuts calc example: turn (4 board cards)
    hole2 = ["7h", "8h"]
    board2 = ["9h", "Th", "2c", "3d"]
    nuts = compute_best_possible_hand(hole2, board2)
    print("[HS-DEBUG] compute_best_possible_hand result:", nuts)
import sys
import io
import contextlib

# Keep originals so we can override safely
_orig_evaluate_hand = evaluate_hand
_orig_compute_best_possible_hand = compute_best_possible_hand

@contextlib.contextmanager
def _suppress_stdout(suppress):
    if not suppress:
        yield
        return
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = old_stdout

def evaluate_hand(hand_cards, board_cards, verbose=False):
    """
    Wrapper around original evaluate_hand that can silence debug prints.
    If verbose is False, stdout from the original function is suppressed.
    """
    with _suppress_stdout(not verbose):
        return _orig_evaluate_hand(hand_cards, board_cards)

def compute_best_possible_hand(hole, board, verbose=False):
    """
    Reimplementation of nuts search that supports verbose flag
    and early exit when the absolute best (category 8) is found.
    """
    print("[HS-DEBUG] compute_best_possible_hand: hole", hole, "board", board) if verbose else None

    # Build full deck
    deck = []
    for r in RANK_ORDER:
        for s in "cdhs":
            deck.append(r + s)

    # Remove known cards
    known = set(hole + board)
    deck = [c for c in deck if c not in known]

    b = len(board)
    if b > 5:
        if verbose:
            print("[HS-DEBUG] Too many board cards")
        return None

    to_add = 5 - b
    if to_add == 0:
        # Evaluate current complete board using suppressed prints as requested
        res = evaluate_hand(hole, board, verbose=verbose)
        return {
            "best_category": res["category"],
            "best_name": res["hand_name"],
            "best_tiebreak": res["tiebreak"],
            "best_five": res["best_five"],
            "completion": [],
        }

    from itertools import combinations as combs
    best_overall = {
        "best_category": -1,
        "best_name": None,
        "best_tiebreak": [],
        "best_five": None,
        "completion": None,
    }

    for extra in combs(deck, to_add):
        full_board = board + list(extra)
        # Use the wrapper evaluate_hand which respects verbose
        result = evaluate_hand(hole, full_board, verbose=verbose)
        cat = result["category"]
        tb = result["tiebreak"]

        if cat > best_overall["best_category"]:
            best_overall["best_category"] = cat
            best_overall["best_name"] = result["hand_name"]
            best_overall["best_tiebreak"] = tb
            best_overall["best_five"] = result["best_five"]
            best_overall["completion"] = list(extra)
            if verbose:
                print("[HS-DEBUG] New nuts via", extra, "->", result["hand_name"])

        elif cat == best_overall["best_category"] and tb > best_overall["best_tiebreak"]:
            best_overall["best_name"] = result["hand_name"]
            best_overall["best_tiebreak"] = tb
            best_overall["best_five"] = result["best_five"]
            best_overall["completion"] = list(extra)
            if verbose:
                print("[HS-DEBUG] Tiebreak nuts improved via", extra)

        # Early exit: Straight Flush is the absolute best
        if best_overall["best_category"] == 8:
            if verbose:
                print("[HS-DEBUG] Early exit: found Straight Flush nuts")
            break

    return best_overall
# --- Quiet wrapper for _best_five_from_seven to avoid duplicate prints ---
# Keep original reference
_orig__best_five_from_seven = _best_five_from_seven

def _best_five_from_seven(cards, verbose=False):
    """
    Wrapper around original _best_five_from_seven that suppresses
    stdout when verbose is False. This prevents duplicate debug lines
    when higher-level functions also print the same events.
    """
    with _suppress_stdout(not verbose):
        return _orig__best_five_from_seven(cards)
# --- end wrapper ---
# --- Logging setup and module-level print override ---
import logging
import builtins

_logger = logging.getLogger("solver.hand_strength")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(_handler)
# Default to INFO so normal runs are quiet; enable debug with set_debug(True)
_logger.setLevel(logging.INFO)

def set_debug(enabled: bool):
    """
    Enable or disable debug logging for this module.
    Call set_debug(True) to see debug traces; set_debug(False) to silence them.
    """
    _logger.setLevel(logging.DEBUG if enabled else logging.INFO)

def _module_print(*args, **kwargs):
    """
    Module-scoped replacement for print that routes to the logger at DEBUG level.
    Keeps behavior simple: joins args with spaces and logs them.
    """
    try:
        msg = " ".join(str(a) for a in args)
    except Exception:
        # Fallback to repr if something is not stringable
        msg = " ".join(repr(a) for a in args)
    _logger.debug(msg)

# Replace the module-level print name so existing print(...) calls in this file
# will be routed to the logger. This does not modify builtins.print globally.
globals()["print"] = _module_print
# --- end logging setup ---
