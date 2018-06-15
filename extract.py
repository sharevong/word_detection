#!/usr/bin/env python
# -*- coding: utf8 -*-

# http://www.matrix67.com/blog/archives/5044


# 将一个句子中所有可能的词切分出来，可以指定一个词最多字数
# 为了方便定位词的左邻字和右邻字，返回词在句子中的左右位置
def extract_word(doc, max_word_len):
    """extract word from doc"""
    indexes = []
    doc_len = len(doc)
    for i in range(doc_len):
        for j in range(i+1, min(i+1+max_word_len, doc_len+1)):
            indexes.append((i, j))
    return indexes


# 为了计算pmi，将一个词切分成两个部分，输出所有可能的二元组
# pmi 点互信息，用于判断一个词是否是真实的词，如蝙蝠，则计算蝙蝠出现的概率除以蝙、蝠出现的概率
# pmi值越大，说明词越可能是真实的词 freq(蝙蝠) / (freq(蝙)*freq(蝠))
def split_word(word):
    """split word to two parts"""
    return [(word[0:i], word[i:]) for i in range(1, len(word))]


def test():
    doc = '我还想到了更有意思的玩法'
    words = list(map(lambda x: doc[x[0]:x[1]], extract_word(doc, max_word_len=5)))
    print(words)
    word = '北京理工大学'
    print(split_word(word))


if __name__ == '__main__':
    test()
