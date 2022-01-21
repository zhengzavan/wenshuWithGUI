# -*- coding:utf-8 -*-
from typing import Set, Dict, Any

from jieba import enable_paddle
import jieba.posseg as pseg
import jieba.analyse as ana


def jieba_cut(text: str) -> dict:
    '''返回一个含名词动词形容词专有名词的词典
    :param text:
    :return:
    '''
    enable_paddle()
    words = list(pseg.cut(text))
    name = ['n']
    adj = ['a', 'ad', 'an']
    v = ['v', 'vd', 'vn']
    special = ['nr', 'ns', 'nt', 'nw', 'nz']
    result_dic = {'name': set(), 'adj': set(), 'v': set(), 'special': set()}
    for word, gender in words:
        if gender in name:
            result_dic['name'].add(word)
        elif gender in adj:
            result_dic['adj'].add(word)
        elif gender in v:
            result_dic['v'].add(word)
        elif gender in special:
            result_dic['special'].add(word)
    return result_dic


def keyword(text: str) -> list:
    '''获取关键词
    :param text:
    :return:
    '''
    words = ana.textrank(text, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
    return words
