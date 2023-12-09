import unittest
from cantofilter.judge import judge

cantonese = ["你喺邊度","乜你今日唔使返學咩","今日好可能會嚟唔到", "我哋影張相留念"]
mandarin = ["你在哪裏","你想插班的話"]
mixed = ["是咁的","屋企停電的話"]
neutral = ["去學校讀書","做人最重要開心"]


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
