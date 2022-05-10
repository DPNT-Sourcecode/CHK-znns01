

# noinspection PyUnusedLocal
# skus = unicode string

def prices_offers_dict() -> dict:
    prices_offers = {
        "A": {"price": 50, "offer": "3A for 130"},
        "B": {"price": 30, "offer": "2B for 45"},
        "C": {"price": 20},
        "D": {"price": 15},
    }

    return prices_offers

def checkout(skus: str) -> int:
    skus_list = skus.split(",")
    prices_offers = prices_offers_dict()
    total_value = 0

    for sku in skus_list:
        if len(sku) == 0 or len(sku) > 1:
            return -1
        elif prices_offers.get(sku) is None:
            return -1
        else:
            pass

    return total_value

