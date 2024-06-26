"""
Core logic:
1. Extract the Cantonese unique words, Mandarin unique words, Mandarin feature words 
    and Mandarin loan words in the input.
2. Judge whether all Mandarin feature words of the input are Mandarin loan words, 
    getting `is_all_loan`.
3. Output the classification result based on the containment of Cantonese/Mandarin 
    unique/feature words.
"""
from enum import StrEnum, auto
import re
from typing import Set, Tuple

CANTO_UNIQUE = re.compile(
    r'[嘅嗰啲咗佢喺咁噉冇啩哋畀嚟諗惗乜嘢閪撚𨳍𨳊瞓睇㗎餸𨋢摷喎嚿噃嚡嘥嗮啱揾搵喐逳噏𢳂岋糴揈捹撳㩒𥄫攰癐冚孻冧𡃁嚫跣𨃩瀡氹嬲掟孭黐唞㪗埞忟𢛴]|' +
    r'唔[係得會好識使洗駛通知到去走掂該錯差]|點[樣會做得解]|[琴尋噚聽第]日|[而依]家|家[下陣]|[真就實梗又話都但淨剩只定一]係|邊[度個位科]|' +
    r'[嚇凍攝整揩逢淥浸激][親嚫]|[橫搞傾諗得唔]掂|仲[有係話要得好衰唔]|返[學工去歸]|執[好生實返輸]|' +
    r'屋企|收皮|慳錢|傾[偈計]|幫襯|求其|是[但旦]|[濕溼]碎|零舍|肉[赤緊酸]|核突|同埋|勁[秋抽]')
MANDO_UNIQUE = re.compile(r'[這哪您們唄咱啥甭她]|還[是好有]')
# “在不把” 因為太多融入粵語所以唔喺判別標準內
# Too many Cantonese loan words have 在不把, so not included in the judgment criteria
MANDO_FEATURE = re.compile(r'[那是的他它看吧沒麼么些了卻説說吃弄也]|而已')
MANDO_LOAN = re.compile(r'亞利桑那|剎那|巴塞羅那|薩那|沙那|哈瓦那|印第安那|那不勒斯|支那|' +
                        r'是[否日次非但旦]|[利於]是|唯命是從|頭頭是道|似是而非|自以為是|俯拾皆是|撩是鬥非|莫衷一是|唯才是用|' +
                        r'[目綠藍紅中飛]的|的[士確式色]|波羅的海|眾矢之的|的而且確|大眼的度|' +
                        r'些[微少許小]|' +
                        r'[淹沉浸覆湮埋沒出]沒|沒[落頂收]|神出鬼沒|' +
                        r'了[結無斷當然哥結得解事之]|[未明]了|不得了|大不了|' +
                        r'他[信人國日殺鄉]|[其利無排維結]他|馬耳他|他加祿|他山之石|' +
                        r'其[它]|' +
                        r'[收查窺觀]看|看[守住好護]|刮目相看|' +
                        r'[酒網水貼]吧|吧[務台臺枱檯]|' +
                        r'[退忘阻]卻|卻步|' +
                        r'[遊游小傳解學假淺眾衆訴論][説說]|[說説][話服明]|自圓其[説說]|長話短[說説]|不由分[說説]|' +
                        r'吃[虧苦力]|' +
                        r'弄[堂]|[賣擺嘲]弄|' +
                        r'可[怒惱]也|如也|也門|之乎者也|天助我也')


class LanguageType(StrEnum):
    '''
    總共有四個分類：粵語、官話、官話溝粵語、中性
    There are four categories: Cantonese, Mandarin, mixed-Mandarin-Cantonese, and neutral
    '''
    CANTONESE = auto()
    MANDARIN = auto()
    MIXED = auto()
    NEUTRAL = auto()


def is_within_loan_span(feature_span: Tuple[int, int], loan_spans: Set[Tuple[int, int]]) -> bool:
    '''
    判斷一個官話特徵係唔係借詞。如果佢嘅位置喺某個借詞區間，就係借詞
    Judge whether a Mandarin feature is a loan word. If its position is within any loan spans, it is a loan.

    Args:
        feature_span (Tuple[int, int]): 官話特徵嘅位置  Mandarin feature position
        loan_spans (Set[Tuple[int, int]]): 借詞嘅位置  Loan word positions
    Returns:
        bool: 係唔係官話借詞 Whether the input feature is a Mandarin loan word
    '''

    return any(feature_span[0] >= loan_span[0] and feature_span[1] <= loan_span[1] for loan_span in loan_spans)


def is_all_loan(s: str) -> bool:
    '''
    判斷一句話入面所有官話特徵係唔係都係借詞
    Judge whether all Mandarin features in a sentence are loan words.
    '''
    mando_features = MANDO_FEATURE.finditer(s)
    mando_loans = MANDO_LOAN.finditer(s)
    feature_spans = set(m.span() for m in mando_features)
    loan_spans = set(m.span() for m in mando_loans)

    # 如果所有官話特徵都喺借詞區間，噉就全部都係借詞
    # If all Mandarin features are within loan word spans, then all are loan words.
    return all(is_within_loan_span(feature_span, loan_spans) for feature_span in feature_spans)


def judge(s: str) -> LanguageType:
    '''
    判斷一句話係粵語、官話、官話溝粵語定係中性
    Judge whether a sentence is Cantonese, Mandarin, mixed-Mandarin-Cantonese, or neutral.

    Args:
        s (str): 一句話  A sentence
    Returns:
        LanguageType: 粵語、官話、官話溝粵語定係中性 LanguageType.CANTONESE, LanguageType.MANDARIN, LanguageType.MIXED, or LanguageType.NEUTRAL.
    '''
    has_canto_unique = bool(CANTO_UNIQUE.search(s))
    has_mando_unique = bool(MANDO_UNIQUE.search(s))
    has_mando_feature = bool(MANDO_FEATURE.search(s))

    if has_canto_unique:
        # 含有粵語成分
        # Contain Cantonese features
        if not (has_mando_unique or has_mando_feature):
            # 冇官話成分，純粵語
            # No Mandarin features, pure Cantonese
            return LanguageType.CANTONESE
        elif has_mando_unique:
            # 含有官話成分，有官話專屬詞，所以係官話溝粵語
            # Contain Mandarin features, has Mandarin unique words, so it is Mandarin-Cantonese mixed
            return LanguageType.MIXED
        else:
            # 既有粵語特徵亦有官話特徵。如果全部官話特徵都係借詞，則算粵語。如果有官話特徵唔係借詞，則為官話溝粵語。
            # Contain both Cantonese and Mandarin features. If all Mandarin features are loan words, then it is Cantonese. Otherwise, it is Mandarin-Cantonese mixed.
            return LanguageType.CANTONESE if is_all_loan(s) else LanguageType.MIXED
    elif has_mando_unique:
        # 冇粵語成分，且包含官話獨有詞，則判斷為官話
        # No Cantonese features and contains Mandarin unique words, it is Mandarin
        return LanguageType.MANDARIN
    elif has_mando_feature:
        # 冇粵語特徵且有官話特徵，但如果全部都係借詞就唔算官話，否則係官話
        # No Cantonese features while has Mandarin features. But if all these Mandarin features are loan words then not count as Mandarin. Otherwise, it is Mandarin.
        return LanguageType.NEUTRAL if is_all_loan(s) else LanguageType.MANDARIN
    else:
        # 冇任何特徵，既可以當粵語亦可以當官話
        # No features, can be either Cantonese or Mandarin
        return LanguageType.NEUTRAL
