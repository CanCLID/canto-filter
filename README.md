# 粵文分類器

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)

[English](https://github.com/CanCLID/cantonese-classifier#cantonese-text-classifier)

## 簡介

呢個係個粵文分類器，用嚟區分粵語同官話文本，對於篩選粵語語料好有用。個分類器會將輸入文本分成四類:

1. `cantonese`: 純粵文，僅含有粵語特徵字詞，例如“你喺邊度”
1. `mandarin`: 純官話文，僅含有官話特徵字詞，例如“你在哪裏”
1. `mixed`：官粵混雜文，同時含有官話同粵語特徵嘅字詞，例如“是咁的”
1. `neutral`：無特徵漢語文，唔含有官話同粵語特徵，既可以當成粵文亦可以當成官話文，例如“去學校讀書”

分類方法係官話同粵語嘅特徵字詞識別。如果同時含有官話同粵語特徵詞彙就算官粵混雜，如果唔含有任何特徵，就算冇特徵中性文本。

注意：呢隻分類器**默認所有輸入文本都係傳統漢字**。如果要分類簡化字文本，要將佢哋轉化成傳統漢字先。推薦使用 [OpenCC](https://github.com/BYVoid/OpenCC)嚟轉換。

## 用法

本篩選器既可以喺 Python 代碼入面用，亦都可以直接喺命令行入面用。

### 命令行

首先要有一個輸入文檔，例如`input.txt`，入面每一行係一個句子，然後運行下面命令

```bash
python3 main.py --input input.txt > output.txt
```

噉樣會得到一個 `output.txt`，入面有由 \t 分成嘅兩列，第一列係判斷標籤，第二列係句子原文本。

如果你想直接篩選出某一類嘅文本，噉可以加一個 `--type <LABEL>` 參數喺後面，例如

```bash
python3 main.py --input input.txt --type cantonese > output.txt
```

噉樣輸出嘅 `output.txt` 就會係純粵文句子。如果想剩係要官話、官粵混合或者中性文本，將個 `--type` 參數定成 `mandarin`、`mixed`、`neutral`就得。

### 作為 Python 函數

```python
from cantofilter import judge

print(judge('你喺邊度'))
print(judge('你在哪裏'))
print(judge('是咁的'))
print(judge('去學校讀書'))
```

# Cantonese text filter

This is a text filter for Cantonese, a very useful tool for filtering Cantonese text corpus. It classifies input sentences with four output labels:

1. `cantonese`: Pure Cantonese text, contains Cantonese-featured words. E.g. 你喺邊度
1. `mandarin`: Pure Mandarin text, contains Mandarin-feature words. E.g. 你在哪裏
1. `mixed`：Mixed Cantonese-Mandarin text, contains both Cantonese and Mandarin-featured words. E.g. 是咁的
1. `neutral`：No feature Chinese text, contains neither Cantonese nor Mandarin feature words. Such sentences can be used for both Cantonese and Mandarin text corpus. E.g. 去學校讀書

The filter is rule-based, by detecting Mandarin and Cantonese feature characters and words. If a sentence contains both Cantonese and Mandarin feature words, then it is a mixed-Cantonese-Mandarin sentence. If it contains neither features, it is a no-feature, neutral Chinese text.

Notice: This filter **assumes all input text in Traditional Chinese characters**. If you want to filter texts written in simplified characters, please convert them into Traditional characters first. We recommend using [OpenCC](https://github.com/BYVoid/OpenCC) to do the conversion.

## How to use

Prepare an input text file, e.g. `input.txt` where each line is a sentence. Then run

```bash
python3 main.py --input <INPUT.TXT>
```

There will be a `output.tsv` which has two columns. The first column is the classification label, and the second column is the original input text.
