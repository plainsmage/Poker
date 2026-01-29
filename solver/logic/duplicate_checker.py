def check_for_duplicates(hand, board):
    """
    Returns None if no duplicates.
    Returns an error string if duplicates exist.
    """

    # Split hand: "As Kh" -> ["As", "Kh"]
    hand_cards = hand.split()

    # Split board: "(no board)" or "Qs 7d 2c"
    if board == "(no board)":
        board_cards = []
    else:
        board_cards = board.split()

    all_cards = hand_cards + board_cards

    # If any card appears more than once, it's a duplicate
    seen = set()
    for card in all_cards:
        if card in seen:
            return f"Duplicate card detected: {card}"
        seen.add(card)

    return None

