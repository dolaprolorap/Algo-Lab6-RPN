import unittest
from rpn import StackCalc

class Test_TestParser(unittest.TestCase):
    def arrEqual(self, arr1: list, arr2: list) -> bool:
        if len(arr1) != len(arr2): return False
        for i in range(len(arr1)):
            if arr1[i] != arr2[i]:
                return False
        return True

    def test_testParser1(self):
        sc = StackCalc()
        sc.parse_str_to_tokens("1 2 + 3")
        excepted_arr = [
            1.0, 2.0, "+", 3.0
        ]
        self.assertTrue(self.arrEqual(sc.tokens, excepted_arr))

    def test_testParser2(self):
        sc = StackCalc()
        sc.parse_str_to_tokens("  1  2 - ( ) + 3")
        excepted_arr = [
            1.0, 2.0, "-", "(", ")", "+", 3.0
        ]
        self.assertTrue(self.arrEqual(sc.tokens, excepted_arr))
    
    def test_testParser3(self):
        sc = StackCalc()
        sc.parse_str_to_tokens("  123  21428 -123 ( 444.0942 ) + 3.9000+")
        excepted_arr = [
            123.0, 21428.0, "-", 123.0, "(", 444.0942, ")", "+", 3.9, "+"
        ]
        self.assertTrue(self.arrEqual(sc.tokens, excepted_arr))

    def test_testParser4(self):
        sc = StackCalc()
        sc.parse_str_to_tokens("+sin(123.09)costg !sin")
        excepted_arr = [
            "+", "sin", "(", 123.09, ")", "cos", "tg", "!", "sin"
        ]
        self.assertTrue(self.arrEqual(sc.tokens, excepted_arr))

class Test_StackCalcRPN(unittest.TestCase):
    def test_testCals1(self):
        sc = StackCalc()
        self.assertEqual(sc.calc("1 2 +"), 3.0)

    def test_testCals2(self):
        sc = StackCalc()
        self.assertEqual(sc.calc("  1  2   + 3 - "), 0.0)

    def test_testCals3(self):
        sc = StackCalc()
        self.assertEqual(sc.calc("  1    8.5 + 3 - "), 6.5)

    def test_testCals4(self):
        sc = StackCalc()
        self.assertEqual(sc.calc(" 3 ! "), 6)

    def test_testCals5(self):
        sc = StackCalc()
        self.assertEqual(sc.calc(" 0 sin cos"), 1)

if __name__ == '__main__':
    unittest.main()