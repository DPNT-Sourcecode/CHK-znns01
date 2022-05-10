

# noinspection PyUnusedLocal
# skus = unicode string

def prices_offers_list() -> list(dict):
    prices_offers = [
        {"item": "A", "price": 50, "offer": "3A for 130"},
        {"item": "B", "price": 30, "offer": "2B for 45"},
        {"item": "C", "price": 20},
        {"item": "D", "price": 15},
    ]

    return prices_offers

def checkout(skus: str) -> int:
    raise NotImplementedError()

