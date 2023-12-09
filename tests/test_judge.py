import unittest
from cantofilter.judge import judge

cantonese = ["你喺邊度"]
mandarin = ["你在哪裏"]
mixed = ["是咁的"]
neutral = ["去學校讀書"]


class TestJudgeFunction(unittest.TestCase):
    def test_cantonese(self):
        for s in cantonese:
            self.assertEqual(judge(s), "cantonese")

    def test_mandarin(self):
        for s in mandarin:
            self.assertEqual(judge(s), "mandarin")

    def test_mixed(self):
        for s in mixed:
            self.assertEqual(judge(s), "mixed")

    def test_neutral(self):
        for s in neutral:
            self.assertEqual(judge(s), "neutral")


if __name__ == "__main__":
    unittest.main()
