from .hand_evaluator import evaluate_hand


def parse_cards(text):
    # Remove spaces and normalize 10 -> T
    cleaned = text.replace(" ", "")
    cleaned = cleaned.replace("10", "T").replace("t", "T")
    cards = []
    for i in range(0, len(cleaned), 2):
        chunk = cleaned[i:i+2]
        if len(chunk) == 2:
            cards.append(chunk)
    return cards


def run_solver(payload):
    hand_text = payload.get("hand", "")
    board_text = payload.get("board", "")

    hand_cards = parse_cards(hand_text)
    board_cards = parse_cards(board_text)
    all_cards = hand_cards + board_cards

    eval_result = evaluate_hand(all_cards)

    return {
        "cards": all_cards,
        "evaluation": eval_result,
    }
