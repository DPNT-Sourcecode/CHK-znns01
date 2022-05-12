from abc import ABC
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product():
    sku: str
    price: int
    quantity: int
    discounts: list[Discount]
    subtotal: Decimal

    def applicable_discounts(self) -> list:
        applicable_discounts = []
        if not self.discounts:
            return applicable_discounts
        else:
            for discount in self.discounts:
                if discount.condition(self.price, self.quantity) is True:
                    applicable_discounts.append(discount)

        return applicable_discounts

    def apply_applicable_discounts(self, applicable_discounts: list):
        applied_discount_subtotal = []

        for discount in applicable_discounts:
            applied_discount_value = 0

            if isinstance(discount, BundlePriceDiscount):
                applied_discount_value = discount.rule(self.price, self.quantity)
            elif isinstance(discount, BundleGiftDiscount):
                applied_discount_value = discount.rule(self.quantity)

            applied_discount_subtotal.append(applied_discount_value)
            best_discounted_subtotal = min(applied_discount_subtotal)
            self.subtotal = best_discounted_subtotal


class Discount(ABC):
    @property
    def rule(self):
        pass

    @property
    def condition(self, product_price: int, product_quantity: int):
        pass


class BundlePriceDiscount(Discount):
    # X A Products for Y

    @property
    def rule(self, product_quantity: int, applied_price: int):
        pass

    @property
    def condition(self, product_price: int, product_quantity: int):
        pass


class BundleGiftDiscount(Discount):
    # X B Products get one C Product free
    bundled_product = Product

    @property
    def rule(self, product_quantity: int):
        bundled_product_price = self.bundled_product.price
        pass

    @property
    def condition(self, product_price: int, product_quantity: int):
        pass


# noinspection PyUnusedLocal
# skus = unicode string

def prices_offers_dict() -> dict:
    prices_offers = {
        "A": {"price": 50, "offer": ["3A for 130", "5A for 200"]},
        "B": {"price": 30, "offer": ["2B for 45"]},
        "C": {"price": 20},
        "D": {"price": 15},
        "E": {"price": 40, "offer": ["2E get one B free"]}
    }

    return prices_offers


def populate_product_checkout_dict(skus: str) -> dict:
    stripped_space_skus = skus.replace(" ", "")
    skus_list = list(stripped_space_skus)
    prices_offers = prices_offers_dict()
    product_checkout_dict = {}

    for sku in skus_list:
        if len(sku) > 1:
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
                    for item_offer in item_dict.get("offer"):
                        item_offer_list = item_offer.split()
                        item_offer_quantity = item_offer_list[0]
                        item_offer_quantity_number = item_offer_quantity[:-1]
                        item_offer_price = item_offer_list[-1]

                        if "offer" not in product_checkout_dict[sku].keys():
                            product_checkout_dict[sku]["offer"] = [{
                                "quantity": item_offer_quantity_number,
                                "price": item_offer_price
                            }]
                        else:
                            product_checkout_dict[sku]["offer"].append({
                                "quantity": item_offer_quantity_number,
                                "price": item_offer_price
                            })
            else:
                product_checkout_dict[sku]["quantity"] += 1 

    return product_checkout_dict


def calculate_product_offer_subtotal(product: dict) -> Decimal:
    product_offer_quantity = product.get("offer").get("quantity")
    product_offer_price = product.get("offer").get("price")

    offer_quantity_result = \
        Decimal(str(product.get("quantity"))) / Decimal(str(product_offer_quantity))
    truncated_offer_quantity_result = int(offer_quantity_result)

    if truncated_offer_quantity_result > 0:
        subtotal_offer_value = \
            Decimal(str(truncated_offer_quantity_result)) * Decimal(str(product_offer_price))

        remainder_offer_quantity_result = \
            Decimal(str(product.get("quantity"))) % Decimal(str(product_offer_quantity))
        subtotal_remainder_value = \
            Decimal(str(remainder_offer_quantity_result)) * Decimal(str(product.get("price")))
        subtotal_value = \
            Decimal(str(subtotal_offer_value)) + Decimal(str(subtotal_remainder_value))
    else:
        subtotal_value = \
            Decimal(str(product.get("quantity"))) * Decimal(str(product.get("price")))
    
    return subtotal_value


def checkout(skus: str) -> int:
    total_value = 0

    if len(skus) == 0:
        return total_value

    product_checkout_dict = populate_product_checkout_dict(skus)

    if product_checkout_dict == -1:
        return -1

    for _, product in product_checkout_dict.items():
        if "offer" in product.keys():
            subtotal_value = calculate_product_offer_subtotal(product)
            total_value += subtotal_value

        else:
            subtotal_value = \
                Decimal(str(product.get("quantity"))) * Decimal(str(product.get("price")))
            total_value += subtotal_value

    return int(total_value)


