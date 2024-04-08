import unittest
from cantofilter.judge import judge

cantonese = ["你喺邊度", "乜你今日唔使返學咩", "今日好可能會嚟唔到", "我哋影張相留念"]
mandarin = ["你在哪裏", "你想插班的話", "家長也應做好家居防蚊措施", "教育不只是為了傳授知識"]
mixed = ["是咁的", "屋企停電的話", "但長遠來講，都係申請息口較低的貸款比較划算"]
neutral = ["去學校讀書", "做人最重要開心",
           "外交部駐香港特別行政區特派員公署副特派員", "全日制或大學生於晚市星期一至星期四一天前訂座"]


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
