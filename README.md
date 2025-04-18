# 粵文分類篩選器

[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)
[![Publish to PyPI](https://github.com/CanCLID/canto-filter/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/CanCLID/canto-filter/actions/workflows/publish-to-pypi.yml)

[English](https://github.com/CanCLID/canto-filter#cantonese-text-filter)

## 簡介

呢個係個粵文篩選器，用嚟區分粵語同官話文本，對於篩選粵語語料好有用。個分類器會將輸入文本分成四類:

1. `cantonese`: 純粵文，僅含有粵語特徵字詞，例如“你喺邊度”
1. `mandarin`: 純官話文，僅含有官話特徵字詞，例如“你在哪裏”
1. `mixed`：官粵混雜文，同時含有官話同粵語特徵嘅字詞，例如“是咁的”
1. `neutral`：無特徵漢語文，唔含有官話同粵語特徵，既可以當成粵文亦可以當成官話文，例如“去學校讀書”

分類方法係官話同粵語嘅特徵字詞識別。如果同時含有官話同粵語特徵詞彙就算官粵混雜，如果唔含有任何特徵，就算冇特徵中性文本。

本分類器為咗照顧性能，淨係用咗簡單嘅邏輯判斷，所以會犧牲一定嘅分類召回率（recall）。如果想要更高嘅分類準確率，請使用本工作組嘅 [`cantonesedetect`](https://pypi.org/project/cantonesedetect/) 包。`cantonesedetect` 會計算各個類別嘅分佈比例再綜合判別，而且可以精細到 6 個類別輸出，準確度更高，但係速度亦會更慢。

### 設計思想同假設

本篩選器嘅主要設計目標係「篩選出可以用作訓練數據嘅優質粵文」，而非「準確分類輸入文本」。所以喺判斷粵語/官話嗰陣會用偏嚴格嘅判別標準，即係會犧牲 recall 嚟換取高 precision （寧願篩漏粵文句子都唔好將官話文誤判成粵文）。

本篩選器**默認所有輸入文本都用[推薦用字方案](https://jyutping.org/blog/typo/)書寫**。如果輸入文本採用其他用字方案（有錯別字），會影響分類篩選結果。例如輸入`畀本書我`分類器會輸出`cantonese`，但寫成`比本書我`會輸出`neutral`。你可以用[錯別字修正器](https://github.com/CanCLID/typo-corrector)嚟清洗被分成`neutral`嘅文本，噉樣可能會得到更多粵文。

呢隻篩選器**默認所有輸入文本都係傳統漢字**。如果要分類簡化字文本，要將佢哋轉化成傳統漢字先。推薦使用 [OpenCC](https://github.com/BYVoid/OpenCC)嚟轉換。

### 引用本篩選器

本工具以字詞特徵抽出「純粵文」文本嘅策略同埋實踐方式。呢個策略首先喺以下場合提出。討論本分類器時，請引用：

```bibtex
@inproceedings{lau-etal-2024-extraction,
    title = "The Extraction and Fine-grained Classification of Written {C}antonese Materials through Linguistic Feature Detection",
    author = "Lau, Chaak-ming  and
      Lau, Mingfei  and
      To, Ann Wai Huen",
    editor = "Ojha, Atul Kr.  and
      Ahmadi, Sina  and
      Cinkov{\'a}, Silvie  and
      Fransen, Theodorus  and
      Liu, Chao-Hong  and
      McCrae, John P.",
    booktitle = "Proceedings of the 2nd Workshop on Resources and Technologies for Indigenous, Endangered and Lesser-resourced Languages in Eurasia (EURALI) @ LREC-COLING 2024",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.eurali-1.4",
    pages = "24--29",
    abstract = "This paper presents a linguistically-informed, non-machine-learning tool for classifying Written Cantonese, Standard Written Chinese, and the intermediate varieties used by Cantonese-speaking users from Hong Kong, which are often grouped into a single {``}Traditional Chinese{''} label. Our approach addresses the lack of textual materials for Cantonese NLP, a consequence of a lower sociolinguistic status of Written Cantonese and the interchangeable use of these varieties by users without sufficient language labeling. The tool utilizes key strings and quotation markers, which can be reduced to string operations, to effectively extract Written Cantonese sentences and documents from materials mixed with Standard Written Chinese. This allows for the flexible and efficient extraction of high-quality Cantonese data from large datasets, catering to specific classification needs. This implementation ensures that the tool can process large amounts of data at a low cost by bypassing model-inferencing, which is particularly significant for marginalized languages. The tool also aims to provide a baseline measure for future classification systems, and the approach may be applicable to other low-resource regional or diglossic languages.",
}
```

「粵文」同「官話文」嘅定義同界線取決於使用者嘅語言意識形態，呢度嘅分類方法以下文所描述嘅粵文書寫體作為基礎。討論本工具採取嘅分類準則，請引用：

```bibtex
@incollection{lau2024ideologically,
  title={Ideologically driven divergence in Cantonese vernacular writing practices},
  author={Lau, Chaak Ming},
  booktitle={The Politics of Language in Hong Kong},
  pages={19--42},
  year={2024},
  publisher={Routledge}
}
```

## 依賴

Python >= 3.11

## 用法

首先用 pip 安裝

```bash
pip install canto-filter
```

你可以喺 Python 代碼入面用，亦都可以直接喺命令行入面用。

### Python 函數用法

本篩選器剩得一個函數 `judge()`，輸入一句話輸出佢嘅語言分類：

```python
from cantofilter import judge

print(judge('你喺邊度')) # cantonese
print(judge('你在哪裏')) # mandarin
print(judge('是咁的'))  # mixed
print(judge('去學校讀書'))  # neutral
```

### 命令行用法

首先要有一個輸入文檔，例如`input.txt`，入面每行一個句子.

#### 輸出標籤同原文

然後運行下面命令

```bash
cantofilter --input input.txt > output.txt
```

噉樣會得到一個 `output.txt`，入面有由 \t 分成嘅兩列，第一列係判斷標籤，第二列係句子原文本。

#### 僅輸出一類

如果你想直接篩選出某一類嘅文本，噉可以加一個 `--mode <LABEL>` 參數喺後面，例如

```bash
cantofilter --input input.txt --mode cantonese > output.txt
```

噉樣輸出嘅 `output.txt` 就會係純粵文句子。如果想剩係要官話、官粵混合或者中性文本，將個 `--mode` 參數定成 `mandarin`、`mixed`、`neutral`就得。

#### 僅輸出標籤

你亦都可以剩係輸出啲句子嘅分類結果，用 `--mode label` 就得：

```bash
cantofilter --input input.txt --mode label > output.txt
```

噉樣嘅 `output.txt` 剩得一列，全部都係分類標籤。

# Cantonese text filter

## Overview

This is a text filter for Cantonese, designed for filtering Cantonese text corpus. It classifies input sentences with four output labels:

1. `cantonese`: Pure Cantonese text, contains Cantonese-featured words. E.g. 你喺邊度
1. `mandarin`: Pure Mandarin text, contains Mandarin-feature words. E.g. 你在哪裏
1. `mixed`：Mixed Cantonese-Mandarin text, contains both Cantonese and Mandarin-featured words. E.g. 是咁的
1. `neutral`：No feature Chinese text, contains neither Cantonese nor Mandarin feature words. Such sentences can be used for both Cantonese and Mandarin text corpus. E.g. 去學校讀書

The filter is regex rule-based, by detecting Mandarin and Cantonese feature characters and words. If a sentence contains both Cantonese and Mandarin feature words, then it is a mixed-Cantonese-Mandarin sentence. If it contains neither features, it is a no-feature, neutral Chinese text.

This package uses simple if-else logic to classify input sentences for better performance, at the price of lower recalls. If you want more accurate classification sacrificing performance, please use our another package [`cantonesedetect`](https://pypi.org/project/cantonesedetect/). `cantonesedetect` uses calculates the proportions linguistic features and classify the input sentence based on the aggregated number. It can achieve more fine-grained classification with 6 output labels.

### Design priciples and assumptions

This filter is designed for the purpose of "obtaining high-quality Cantonese text", as opposed to "accurately classifying input texts". Therefore, it maximizes precision at the price of recall, to minimize the false positive rate / avoid including potential Mandarin sentences (we rather miss some Cantonese sentences, than mistaking potential Mandarin sentences as Cantonese).

This filter **assumes all input text written in [the recommended orthography](https://jyutping.org/blog/typo/)**. Spelling errors or typos in input text might affect the classification result. For instance, `畀本書我` yields `cantonese`, while `比本書我` yields `neutral`. You can use the [spelling corrector](https://github.com/CanCLID/typo-corrector) to correct the `neutral` text, which might give you more Cantonese text.

This filter **assumes all input text in Traditional Chinese characters**. If you want to filter texts written in simplified characters, please convert them into Traditional characters first. We recommend using [OpenCC](https://github.com/BYVoid/OpenCC) to do the conversion.

### Citing this package

The implementation and methodology of this filter was first proposed in the following contexts. below. When discussing this filter, please cite:

```bibtex
@inproceedings{lau-etal-2024-extraction,
    title = "The Extraction and Fine-grained Classification of Written {C}antonese Materials through Linguistic Feature Detection",
    author = "Lau, Chaak-ming  and
      Lau, Mingfei  and
      To, Ann Wai Huen",
    editor = "Ojha, Atul Kr.  and
      Ahmadi, Sina  and
      Cinkov{\'a}, Silvie  and
      Fransen, Theodorus  and
      Liu, Chao-Hong  and
      McCrae, John P.",
    booktitle = "Proceedings of the 2nd Workshop on Resources and Technologies for Indigenous, Endangered and Lesser-resourced Languages in Eurasia (EURALI) @ LREC-COLING 2024",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.eurali-1.4",
    pages = "24--29",
    abstract = "This paper presents a linguistically-informed, non-machine-learning tool for classifying Written Cantonese, Standard Written Chinese, and the intermediate varieties used by Cantonese-speaking users from Hong Kong, which are often grouped into a single {``}Traditional Chinese{''} label. Our approach addresses the lack of textual materials for Cantonese NLP, a consequence of a lower sociolinguistic status of Written Cantonese and the interchangeable use of these varieties by users without sufficient language labeling. The tool utilizes key strings and quotation markers, which can be reduced to string operations, to effectively extract Written Cantonese sentences and documents from materials mixed with Standard Written Chinese. This allows for the flexible and efficient extraction of high-quality Cantonese data from large datasets, catering to specific classification needs. This implementation ensures that the tool can process large amounts of data at a low cost by bypassing model-inferencing, which is particularly significant for marginalized languages. The tool also aims to provide a baseline measure for future classification systems, and the approach may be applicable to other low-resource regional or diglossic languages.",
}
```

The definitions and boundaries of 'Cantonese text' and 'Mandarin text' depend on the user's language ideology. The classification method used here is based on the Cantonese written style described in the following text. When discussing the criteria adopted by this tool, please cite:

```bibtex
@incollection{lau2024ideologically,
  title={Ideologically driven divergence in Cantonese vernacular writing practices},
  author={Lau, Chaak Ming},
  booktitle={The Politics of Language in Hong Kong},
  pages={19--42},
  year={2024},
  publisher={Routledge}
}
```

## Requirement

Python >= 3.11

## How to use

Install the package with pip first

```bash
pip install canto-filter
```

This package can be used in python codes, or as a CLI tool.

### Python function usage

There is only one function in this package, `judge()`, which accepts a string input and outputs one of the labels:

```python
from cantofilter import judge

print(judge('你喺邊度')) # cantonese
print(judge('你在哪裏')) # mandarin
print(judge('是咁的'))  # mixed
print(judge('去學校讀書'))  # neutral
```

### CLI usage

Assume an input text file, e.g. `input.txt` where each line is a sentence.

#### Output both labels and original texts

Then run

```bash
cantofilter --input input.txt > output.txt
```

There will be a `output.txt` which has two columns. The first column is the language label, and the second column is the original input text.

#### Output only text of one class

If you want only one class of text, use the `--mode <LABEL>` argument. Say if you want pure Cantonese text only:

```bash
cantofilter --input input.txt --mode cantonese > output.txt
```

The `output.txt` will contain only Cantonese text.

#### Output label only

If you want to include the classification labels in the output, use `--mode label` like this:

```bash
cantofilter --input input.txt --mode label > output.txt
```

Then your `output.txt` will contain only classification results of the input sentences.
