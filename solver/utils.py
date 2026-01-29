def normalize_cards(cards):
    out = []
    for c in cards:
        c = c.strip()
        if len(c) != 2:
            continue
        rank = c[0].upper()
        suit = c[1].lower()
        out.append(rank + suit)
    return out

