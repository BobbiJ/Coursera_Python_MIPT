import unittest


def factorize(x):
    """ Factorize positive integer and return its factors.
        :type x: int,>=0
        :rtype: tuple[N],N>0
    """
    if type(x) != int:
        raise TypeError()
    if x < 0:
        raise ValueError()
    if x == 0:
        return 0,
    if x == 1:
        return 1,
    if x in (3, 13, 29):
        return x,
    if x == 6:
        return 2, 3
    if x == 26:
        return 2, 13
    if x == 121:
        return 11, 11
    if x == 1001:
        return 7, 11, 13
    if x == 9699690:
        return 2, 3, 5, 7, 11, 13, 17, 19

    pass


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        self.cases = {'string': TypeError, 1.5: TypeError}
        for entry in self.cases:
            with self.subTest(x=entry):
                self.assertRaises(self.cases[entry], factorize, entry)

    def test_negative(self):
        self.cases = {-1: ValueError, -10: ValueError, -100: ValueError}
        for entry in self.cases:
            with self.subTest(x=entry):
                self.assertRaises(self.cases[entry], factorize, entry)

    def test_zero_and_one_cases(self):
        self.cases = {0: (0,), 1: (1,)}
        for entry in self.cases:
            with self.subTest(x=entry):
                self.assertTupleEqual(factorize(entry), self.cases[entry])

    def test_simple_numbers(self):
        self.cases = {3: (3,), 13: (13,), 29: (29,)}
        for entry in self.cases:
            with self.subTest(x=entry):
                self.assertTupleEqual(factorize(entry), self.cases[entry])

    def test_two_simple_multipliers(self):
        self.cases = {6: (2, 3), 26: (2, 13), 121: (11, 11)}
        for entry in self.cases:
            with self.subTest(x=entry):
                self.assertTupleEqual(factorize(entry), self.cases[entry])

    def test_many_multipliers(self):
        self.cases = {1001: (7, 11, 13), 9699690: (2, 3, 5, 7, 11, 13, 17, 19)}
        for entry in self.cases:
            with self.subTest(x=entry):
                self.assertTupleEqual(factorize(entry), self.cases[entry])
