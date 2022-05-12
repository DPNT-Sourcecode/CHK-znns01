from solutions.CHK import checkout_solution


class TestCkeckout():
    def test_checkout_invalid(self):
        assert checkout_solution.checkout("") == -1

    def test_checkout_valid_without_offer(self):
        assert checkout_solution.checkout("C, D") == 35

    def test_checkout_valid_with_offer(self):
        assert checkout_solution.checkout("A, B, A, B, A") == 175
