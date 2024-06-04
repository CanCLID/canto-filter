import unittest
from cantofilter.judge import LanguageType, judge

cantonese = ["你喺邊度", "乜你今日唔使返學咩", "今日好可能會嚟唔到", "我哋影張相留念"]
mandarin = ["你在哪裏", "你想插班的話", "家長也應做好家居防蚊措施", "教育不只是為了傳授知識"]
mixed = ["是咁的", "屋企停電的話", "但長遠來講，都係申請息口較低的貸款比較划算"]
neutral = ["去學校讀書", "做人最重要開心",
           "外交部駐香港特別行政區特派員公署副特派員", "全日制或大學生於晚市星期一至星期四一天前訂座"]


class TestJudgeFunction(unittest.TestCase):
    def test_cantonese(self):
        for s in cantonese:
            result = judge(s)
            self.assertEqual(result, LanguageType.CANTONESE)
            self.assertEqual(result, "cantonese")  # plain string also works here

    def test_mandarin(self):
        for s in mandarin:
            result = judge(s)
            self.assertEqual(result, LanguageType.MANDARIN)
            self.assertEqual(result, "mandarin")

    def test_mixed(self):
        for s in mixed:
            result = judge(s)
            self.assertEqual(result, LanguageType.MIXED)
            self.assertEqual(result, "mixed")

    def test_neutral(self):
        for s in neutral:
            result = judge(s)
            self.assertEqual(result, LanguageType.NEUTRAL)
            self.assertEqual(result, "neutral")


if __name__ == "__main__":
    unittest.main()
