

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
        elif sku in prices_offers.index():
            item_dict = prices_offers.get(sku)

            if not "offer" in item_dict.index():
                total_value =+ item_dict.get("price", 0) 
            else:
                item_offer = item_dict.get("offer")
                item_offer_list = item_offer.split()
                item_offer_quantity = item_offer_list[0]
                item_offer_quantity_number = item_offer_quantity[:-1]
                item_offer_price = item_offer_list[-1]
        else:
            return -1

    return total_value
