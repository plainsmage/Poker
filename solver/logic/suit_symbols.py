from django.utils.safestring import mark_safe

def convert_suits(card_string):
    suit_map = {
        "s": ("\u2660", "suit-spade"),
        "h": ("\u2665", "suit-heart"),
        "d": ("\u2666", "suit-diamond"),
        "c": ("\u2663", "suit-club"),
    }

    cards = card_string.split()
    out = []

    for c in cards:
        rank = c[0]
        suit = c[1]
        symbol, css_class = suit_map[suit]
        out.append(f"{rank}<span class='{css_class}'>{symbol}</span>")

    return mark_safe(" ".join(out))

