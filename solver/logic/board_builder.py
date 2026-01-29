def build_board(cleaned):
    cards = []
    for i in range(1, 6):
        rank = cleaned.get(f"board_rank_{i}")
        suit = cleaned.get(f"board_suit_{i}")
        if rank and suit:
            cards.append(rank + suit)
    if not cards:
        return "(no board)"
    return " ".join(cards)

