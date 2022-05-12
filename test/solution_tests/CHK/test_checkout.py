from solutions.CHK import checkout_solution


class TestCkeckout():
    def test_checkout_invalid(self):
        assert checkout_solution.checkout("") == 0

    def test_checkout_valid_without_offer(self):
        assert checkout_solution.checkout("CD") == 35

    def test_checkout_valid_with_offers(self):
        assert checkout_solution.checkout("ABABA") == 175

    def test_checkout_valid_with_multiple_occurence_offers(self):
        assert checkout_solution.checkout("ABABABB") == 220

    def test_checkout_valid_with_multiple_occurence_offers_and_remainder(self):
        assert checkout_solution.checkout("ABABABBA") == 270



