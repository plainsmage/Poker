from django import template

register = template.Library()

SUIT_MAP = {
    "s": ("♠", "suit-s"),
    "h": ("♥", "suit-h"),
    "d": ("♦", "suit-d"),
    "c": ("♣", "suit-c"),
}

@register.filter
def cards(value):
    if not value:
        return ""
    parts = value.split()
    out = []
    for card in parts:
        if len(card) < 2:
            continue
        rank = card[0]
        suit = card[1].lower()
        if suit in SUIT_MAP:
            symbol, css = SUIT_MAP[suit]
            out.append(f'<span class="{css}">{rank}{symbol}</span>')
        else:
            out.append(card)
    return " ".join(out)
