#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import log


# 吃葡萄不吐葡萄皮不吃葡萄倒吐葡萄皮
# 葡萄的左邻字分别为[吃，吐，吃，吐]，右邻字分别为[不，皮，倒，皮]
# 左邻字的信息熵为-1/2 * log(1/2) -1/2 * log(1/2) = 0.693
def compute_entropy(words):
    """get left and right entropy of word"""
    length = float(len(words))
    if length == 0:
        return 0
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return sum(map(lambda x: -x/length * log(x/length), frequency.values()))


def test():
    words = ['吃', '吐', '吃', '吐']
    entropy = compute_entropy(words)
    print(entropy)


if __name__ == '__main__':
    test()
