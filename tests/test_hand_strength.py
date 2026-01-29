import pytest
from solver.hand_strength import evaluate_hand, compute_best_possible_hand

def test_wheel_straight():
    # A-2-3-4-5 wheel straight
    hole = ["5h", "4d"]
    board = ["3c", "2s", "Ah"]
    res = evaluate_hand(hole, board, verbose=False)
    assert res["hand_name"] == "Straight"
    # best_five must include the wheel ranks
    ranks = "".join(res["best_five"])
    assert any(card[0] == "5" for card in res["best_five"])
    assert any(card[0] == "4" for card in res["best_five"])
    assert any(card[0] == "3" for card in res["best_five"])
    assert any(card[0] == "2" for card in res["best_five"])
    assert any(card[0] == "A" for card in res["best_five"])

def test_flush_tiebreak():
    # Five hearts present, Ace-high flush expected
    hole = ["Kh", "2h"]
    board = ["Ah", "Qh", "Jh", "3d", "4s"]
    res = evaluate_hand(hole, board, verbose=False)
    assert res["hand_name"] == "Flush"
    # Ensure top hearts are present (Ace and King)
    assert any(card == "Ah" for card in res["best_five"])
    assert any(card == "Kh" for card in res["best_five"])

def test_six_card_input_four_of_a_kind():
    # 6 total cards (2 hole + 4 board) with four aces present
    hole = ["As", "Ad"]
    board = ["Ah", "Ac", "Kd", "2c"]
    res = evaluate_hand(hole, board, verbose=False)
    assert res["hand_name"] == "Four of a Kind"
    # best_five should include all four aces
    assert sum(1 for c in res["best_five"] if c[0] == "A") == 4

def test_compute_best_possible_hand_finds_straight_flush():
    # Known scenario where a straight flush completion exists
    hole = ["7h", "8h"]
    board = ["9h", "Th", "2c", "3d"]  # turn present, one card to complete
    nuts = compute_best_possible_hand(hole, board, verbose=False)
    assert isinstance(nuts, dict)
    # The nuts search should find a Straight Flush (category 8)
    assert nuts["best_category"] == 8
    assert "Straight Flush" in nuts["best_name"]

if __name__ == "__main__":
    pytest.main(["-q", "tests/test_hand_strength.py"])
