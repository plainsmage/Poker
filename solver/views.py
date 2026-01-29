from .hand_strength import compute_best_possible_hand
from django.shortcuts import render
from .hand_strength import evaluate_hand, compute_future_improvements


def home(request):
    if request.method == "POST":
        raw_hand = request.POST.get("hand", "")
        raw_board = request.POST.get("board", "")

        # Split user input into card tokens
        hand_cards = raw_hand.split()
        board_cards = raw_board.split()

        # Require at least 2 hand cards and 3 board cards
        if len(hand_cards) < 2 or len(board_cards) < 3:
            return render(request, "solver/home.html", {
                "hand": raw_hand,
                "board": raw_board,
                "result": None,
            })

        # Evaluate the current hand
        result = evaluate_hand(hand_cards, board_cards)
        print("DEBUG RESULT:", result)

        # Add future improvement info (placeholder)
        all_cards = hand_cards + board_cards
        result["best_possible"] = compute_best_possible_hand(all_cards)

        result["future"] = compute_future_improvements(hand_cards, board_cards)

        return render(request, "solver/home.html", {
            "hand": raw_hand,
            "board": raw_board,
            "result": result,
        })

    # GET request
    return render(request, "solver/home.html", {
        "hand": "",
        "board": "",
        "result": None,
    })
