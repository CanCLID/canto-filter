import argparse
import re
from typing import List, Tuple

canto_unique = re.compile(r'[嘅嗰啲咗佢喺咁噉冇啩哋畀嚟諗乜嘢閪撚𨳍瞓]|屋企|邊度|而家|依家|琴日|尋日')
mando_unique = re.compile(r'[這哪您們唄]|那[個些裏裡邊天樣麼么兒]')
mando_feature = re.compile(r'[那是的他她吧了沒不在麼么些]')
mando_loan = re.compile(r'亞利桑那|剎那|巴塞羅那|薩那|沙那|哈瓦那|印第安那|那不勒斯|支那|是日|是次|是非|利是|唯命是從|頭頭是道|似是而非|\\\
        自以為是|俯拾皆是|撩是鬥非|莫衷一是|是但|是旦|大吉利是|目的|紅的|綠的|藍的|的士|波羅的海|的確|眾矢之的|些微|些少|些小|些許|\\\
        淹沒|沉沒|沒收|湮沒|埋沒|沒落|了結|未了|了無|不了了之|了斷|了當|了然|了哥|不過|不滿|不如|不妨|\\\
        不俗|不宜|不僅|不必|不利|不當|不死|不果|不一|迫不及待|不足|意想不到|不忠|不同|不絕|不斷|不良|不外乎|\\\
        不妙|他信|他人|他加祿|他國|他山之石|他日|他殺|他鄉|其他|利他|排他|無他|維他|馬耳他|在場|酒吧|貼吧|\\\
        網吧|水吧|吧台')


def is_loan(fs: str, loan_spans: List[Tuple]) -> bool:
    # 判斷一個官話特徵係唔係借詞。如果佢嘅位置喺某個借詞區間，就係借詞
    for ls in loan_spans:
        if fs[0] >= ls[0] and fs[1] <= ls[1]:
            return True
    return False


def is_all_loan(s: str) -> bool:
    # 判斷一句話入面所有官話特徵係唔係都係借詞
    mando_features = mando_feature.finditer(s)
    mando_loans = mando_loan.finditer(s)
    feature_spans = [m.span() for m in mando_features]
    loan_spans = [m.span() for m in mando_loans]

    # 如果所有官話特徵都喺借詞區間，噉就全部都係借詞
    for fs in feature_spans:
        if not is_loan(fs, loan_spans):
            return False
    return True


def judge(s: str) -> str:
    has_canto_unique = bool(re.search(canto_unique, s))
    has_mando_unique = bool(re.search(mando_unique, s))
    has_mando_feature = bool(re.search(mando_feature, s))

    if has_canto_unique:
        # 含有粵語成分
        if not (has_mando_unique or has_mando_feature):
            # 冇官話成分，純粵語
            return "cantonese"
        elif has_mando_unique:
            # 含有官話成分，有官話專屬詞，所以係官話溝粵語
            return "mixed"
        else:
            # 含有官話成分，冇官話專屬詞，有可能官話借詞，亦都算粵語
            if is_all_loan(s):
                return "cantonese"
            else:
                return "mixed"
    elif has_mando_unique:
        # 冇粵語成分
        return "mandarin"
    elif has_mando_feature:
        # 有官話特徵但係要判斷係唔係全部都係借詞
        if is_all_loan(s):
            # 全部都係借詞，唔算官話
            return "neutral"
        else:
            # 有特徵唔係借詞，所以算官話
            return "mandarin"
    else:
        # 冇任何特徵，既可以當粵語亦可以當官話
        return "neutral"


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='')
    argparser.add_argument('--input', type=str, default='input.txt')
    args = argparser.parse_args()

    lines = open(args.input, encoding="utf-8").readlines()
    output = open('output.tsv', 'w', encoding="utf-8")

    for line in lines:
        output.write('{}\t{}\n'.format(judge(line.strip()), line.strip()))

    output.close()
