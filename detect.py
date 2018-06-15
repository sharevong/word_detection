#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from time import ctime
from entropy import compute_entropy
from extract import split_word, extract_word


class WordInfo(object):
    """record information of a word"""
    def __init__(self, text):
        self.text = text            # 记录该词的文本内容
        self.count = 0.0            # 记录该词的出现次数
        self.freq = 0.0             # 记录该词的出现频率（在所有词语中）
        self.left = []              # 记录该词的左邻字
        self.left_entropy = 0.0     # 记录该词的左邻字信息熵
        self.right = []             # 记录该词的右邻字
        self.right_entropy = 0.0    # 记录该词的右邻字信息熵
        # pmi 点互信息，用于判断一个词是否是真实的词，如蝙蝠，则计算蝙蝠出现的概率除以两个字分别出现的概率相乘
        # pmi值越大，说明词越可能是真实的词 freq(蝙蝠)/(freq(蝙)*freq(蝠))
        self.pmi = 0.0

    def update_data(self, left, right):   # left 左邻字 right 右邻字
        self.count += 1.0
        if left:
            self.left.append(left)
        if right:
            self.right.append(right)

    def compute_freq(self, length):     # length 所有词语的总数
        self.freq = self.count / length

    def compute_entropies(self):
        self.left_entropy = compute_entropy(self.left)
        self.right_entropy = compute_entropy(self.right)

    def compute_pmi(self, words):
        parts = split_word(self.text)
        if len(parts) > 0:
            self.pmi = min(map(lambda part: self.freq / (words[part[0]].freq * words[part[1]].freq),
                               parts))


class DocSegment(object):
    def __init__(self, doc, max_word_len=5, min_freq=0.00005, min_entropy=2, min_pmi=6.0):
        self.max_word_len = max_word_len
        self.min_freq = min_freq
        self.min_entropy = min_entropy
        self.min_pmi = min_pmi

        words = self.get_words(doc)
        self.result = map(lambda w: (w.text, len(w.text), w.freq, min(w.left_entropy, w.right_entropy), w.pmi),
                          filter(self.filter_word, words))

    def get_words(self, doc):
        words = {}
        # 将文档中除中文字符以外的其他字符修改为空格
        symbols = '[^\u4e00-\u9fa5]'
        pattern = re.compile(symbols)
        doc = pattern.sub(' ', str(doc))
        doc = re.sub(' +', ' ', doc)

        # 用空格将文档分为句子，取出句子中的词和它的左邻字/右邻字
        sentences = doc.split(' ')
        for sentence in sentences:
            word_index = extract_word(sentence, self.max_word_len)
            for index in word_index:
                word = sentence[index[0]:index[1]]
                if word not in words:
                    words[word] = WordInfo(word)
                words[word].update_data(sentence[index[0]-1:index[0]], sentence[index[1]:index[1]+1])

        # 计算词的出现频率和左邻字右邻字信息熵
        length = float(sum(map(lambda x: len(x), doc)))
        for word in words:
            words[word].compute_freq(length)
            words[word].compute_entropies()

        # 计算词的pmi
        values = sorted(words.values(), key=lambda x: len(x.text))
        for v in values:
            if v.text == 1:  # 长度为1的词pmi为0，不计算
                continue
            v.compute_pmi(words)

        # 返回WordInfo的列表，按出现频率、信息熵排序
        return sorted(values, key=lambda x: (x.freq, min(x.left_entropy, x.right_entropy)),
                      reverse=True)

    def filter_word(self, wordinfo):
        return len(wordinfo.text) > 1 and wordinfo.freq > self.min_freq and \
               wordinfo.pmi > self.min_pmi and \
               min(wordinfo.left_entropy, wordinfo.right_entropy) > self.min_entropy


def test():
    print('start time: ', ctime())

    read_file_name = './西游记.txt'
    read_file = open(read_file_name, 'r', encoding='utf-8')
    doc = read_file.read()
    read_file.close()

    docseg = DocSegment(doc)

    write_file_name = './result.csv'
    write_file = open(write_file_name, 'w')
    write_file.write('word,len,freq,entropy,pmi\n')
    for word in docseg.result:
        write_file.write(','.join(str(i) for i in word) + '\n')
    write_file.close()

    print('stop time: ', ctime())


if __name__ == '__main__':
    test()
