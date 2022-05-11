from decimal import Decimal

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
    product_checkout_dict = {}

    for sku in skus_list:
        if len(sku) == 0 or len(sku) > 1:
            return -1
        elif sku not in prices_offers.keys():
            return -1
        else:
            item_dict = prices_offers.get(sku)

            if sku not in product_checkout_dict.keys():
                product_checkout_dict[sku] = {
                    "quantity": 1,
                    "price": item_dict.get("price"),
                }

                if "offer" in item_dict.keys():
                    item_offer = item_dict.get("offer")
                    item_offer_list = item_offer.split()
                    item_offer_quantity = item_offer_list[0]
                    item_offer_quantity_number = item_offer_quantity[:-1]
                    item_offer_price = item_offer_list[-1]

                    product_checkout_dict[sku]["offer"] = {
                        "quantity": item_offer_quantity_number,
                        "price": item_offer_price
                    }
            else:
                product_checkout_dict[sku]["quantity"] += 1 

    for _, product in product_checkout_dict.items():
        if "offer" in product.keys():
            product_offer_quantity = product.get("offer").get("quantity")
            product_offer_price = product.get("offer").get("price")

            offer_quantity_result = \
                Decimal(f"{product.get('quantity')}") / Decimal(f"{product_offer_quantity}")
            truncated_offer_quantity_result = int(offer_quantity_result)

            if truncated_offer_quantity_result > 0:
                subtotal_offer_value = \
                    Decimal(f"{truncated_offer_quantity_result}") * Decimal(f"{product_offer_price}")

                remainder_offer_quantity_result = \
                    Decimal(f"{product.get('quantity')}") % Decimal(f"{product_offer_quantity}")
                subtotal_remainder_value = \
                    Decimal(f"{remainder_offer_quantity_result}") * Decimal((f"{product.get('price')}}")
                subtotal_value = subtotal_offer_value + subtotal_remainder_value
            else:
                subtotal_value = \
                    Decimal(f"{product.get('quantity')}") * Decimal(f"{product.get('price')}")

            total_value += subtotal_value

        else:
            subtotal_value = \
                Decimal(f"product.get('quantity')") * Decimal(f"{product.get('price')}")
            total_value += subtotal_value

    return total_value


