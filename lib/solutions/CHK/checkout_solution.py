from abc import ABC
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Receipt():
    products_dict: dict
    total: int

    def build_products_list(self, skus: str):
        stripped_space_skus = skus.replace(" ", "")
        skus_list = list(stripped_space_skus)
        prices_offers = prices_offers_dict()

        for sku in skus_list:
            if len(sku) > 1:
                raise Exception("Unexpected individual sku length. It has to be of length 1.") 
            elif sku not in prices_offers.keys():
                raise Exception("Unexpected sku value. We do not have products with the given sku value.") 
            else:
                item_dict = prices_offers.get(sku)

                if sku not in product_checkout_dict.keys():
                    product_checkout_dict[sku] = Product(
                        sku=sku,
                        price=item_dict.get("price"),
                        quantity= 1
                    )

                    if "offer" in item_dict.keys():
                        for item_offer in item_dict.get("offer"):
                            item_offer_list = item_offer.split()
                            item_offer_quantity = item_offer_list[0]
                            item_offer_quantity_number = item_offer_quantity[:-1]

                            stripped_item_offer = item_offer.strip(" ")

                            if stripped_item_offer[-3] == "one" and stripped_item_offer[-1] == "free":   
                                product_offered_sku = stripped_item_offer[-2]

                                product_checkout_dict[sku].discounts.append(BundleGiftDiscount(
                                    bundled_product_sku=product_offered_sku,
                                    quantity=item_offer_quantity_number
                                ))
                            else:
                                item_offer_price = item_offer_list[-1]

                                product_checkout_dict[sku].discount.append(BundlePriceDiscount(
                                    quantity=item_offer_quantity_number,
                                    price=item_offer_price
                                ))
                else:
                    product_checkout_dict[sku].quantity += 1 

    def calculate_total(self):
        total_value = 0

        for _, product in self.products_dict.items():
            product.calculate_subtotal(self.products_dict)
            total_value += product.subtotal

        self.total = total_value


@dataclass
class Product():
    sku: str
    price: int
    quantity: int
    discounts: list
    subtotal: Decimal

    def applicable_discounts(self, products_dict) -> list:
        applicable_discounts = []
        if not self.discounts:
            return applicable_discounts
        else:
            for discount in self.discounts:
                if discount.condition(self.quantity) is True:
                    applicable_discounts.append(discount)

        return applicable_discounts

    def apply_applicable_discounts(self, applicable_discounts: list, products_dict):
        applied_discount_subtotal = []

        for discount in applicable_discounts:
            applied_discount_value = 0

            if isinstance(discount, BundlePriceDiscount):
                applied_discount_value = discount.rule(self.quantity, self.price)
            elif isinstance(discount, BundleGiftDiscount):
                applied_discount_value = discount.rule(self.quantity, self.price, products_dict)

            applied_discount_subtotal.append(applied_discount_value)
            best_discounted_subtotal = min(applied_discount_subtotal)
        
        return best_discounted_subtotal

    def calculate_subtotal(self, products_dict):
        available_discounts = self.applicable_discounts(products_dict)
        subtotal_value = 0

        if len(available_discounts) > 0:
            self.subtotal = self.apply_applicable_discounts(available_discounts, products_dict)
        else:
            self.subtotal = self.price * self.quantity


class Discount(ABC):
    def rule(self):
        pass

    def condition(self, product_quantity: int):
        pass


class BundlePriceDiscount(Discount):
    # X A Products for Y
    quantity: int
    price: int

    def rule(self, product_quantity: int, product_price: int) -> Decimal:
        offer_quantity_result = \
            Decimal(str(product_quantity)) / Decimal(str(self.quantity))
        truncated_offer_quantity_result = int(offer_quantity_result)

        if truncated_offer_quantity_result > 0:
            subtotal_offer_value = \
                Decimal(str(truncated_offer_quantity_result)) * Decimal(str(self.price))

            remainder_offer_quantity_result = \
                Decimal(str(product_quantity)) % Decimal(str(self.quantity))
            subtotal_remainder_value = \
                Decimal(str(remainder_offer_quantity_result)) * Decimal(str(product_price))
            subtotal_value = \
                Decimal(str(subtotal_offer_value)) + Decimal(str(subtotal_remainder_value))
        else:
            subtotal_value = \
                Decimal(str(product_quantity)) * Decimal(str(product_price))
        
        return subtotal_value

    def condition(self, product_quantity: int) -> bool:
        return product_quantity >= self.quantity


class BundleGiftDiscount(Discount):
    # X B Products get one C Product free
    quantity: int
    bundled_product_sku: str

    def rule(self, product_quantity: int, product_price, products_dict: dict) -> Decimal:
        bundled_product_price = self.products_dict[bundled_product_sku].price
        applied_discount = 0

        if self.bundled_product_sku in products_dict.keys():
            offer_quantity_result = Decimal(str(product_quantity)) / Decimal(str(self.quantity))
            truncated_offer_quantity_result = int(offer_quantity_result)

            if truncated_offer_quantity_result >= product_quantity: 
                applied_discount =\
                    Decimal(str(-truncated_offer_quantity_result)) * Decimal(str(bundled_product_price))
            else:
                applied_discount = \
                    Decimal(str(-truncated_offer_quantity_result)) * Decimal(str(bundled_product_price))

        discounted_price = \
            Decimal(str(product_quantity)) * Decimal(str(product_price)) - Decimal(str(applied_discount))

        return discounted_price

    def condition(self, product_quantity: int) -> bool:
        return product_quantity >= self.quantity


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


def checkout(skus: str) -> int:
    if len(skus) == 0:
        return 0

    receipt = Receipt()

    try:
        receipt.build_products_list(skus)
    except Exception:
        return -1

    receipt.calculate_total()

    return int(receipt.total)
