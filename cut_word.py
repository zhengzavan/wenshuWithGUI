# encoding=utf-8
import re
def get_reason(text):
    '''案由'''
    r = r'''案[　]*由
(.*)'''
    words = re.findall(r,text)
    words = [word.replace('　', '') for word in words]
    return set(words)
def get_keywords(text):
    '''关键词'''
    r = r'''关[　]*键[　]*词
[　]*(.*)'''
    words = re.findall(r, text)
    wordSpilt = []
    for word in words:
        wordSpilt = wordSpilt + word.split('；')
    return set(wordSpilt)
def get_plantiff(text):
    '''原告'''
    r = r'''原告.*）：*(.*?)。'''
    words = re.findall(r, text)
    print(words)
    return set(words)
def get_defandant(text):
    '''被告'''
    r = '''被告.*）：(.*?)。'''
    words = re.findall(r, text)
    print(words)
    return set(words)
def get_result(text):
    '''裁判结果'''
    r = r'''判决如下：
[　]*([^。]*)。'''
    words = re.findall(r, text)
    wordSpilt = []
    for word in words:
        wordSpilt = wordSpilt +  word.split('；')
    print(wordSpilt)
    word = wordSpilt
    words = [word.replace('　', '') for word in words]
    return set(words)
def get_laws(text):
    '''涉案法条'''
    r = '''(《.*?》)'''
    words = re.findall(r, text)
    words = [word for word in words if word.find('法') != -1]
    print(words)
    return set(words)
def get_date(text):
    '''裁判日期'''
    r = '''.{4}?年.{1,2}?月.{1,2}?日'''
    words = re.findall(r, text)
    print(words)
    return set(words)
def get_court(text):
    '''法院'''
    r = '''.*?法院'''
    words = re.findall(r, text)[0]
    print(words)
    return set([words])
def get_number(text):
    ''''案号'''
    r = '''(（\d{4}）.*?号)'''
    words = re.findall(r, text)
    print(words)
    return set(words)
factors = ['案由','关键词','原告','被告','裁判结果','涉案法条','裁判日期','法院','案号']
cut_methods = [get_reason, get_keywords, get_plantiff, get_defandant, get_result, get_laws, get_date, get_court, get_number]
def get_words(factor, text):
    text = text
    try:return cut_methods[factors.index(factor)](text)
    except:return []
if __name__ == '__main__':
    text = '''　　关键词
　　侵害发明专利权；现有技术抗辩'''
    get_words('关键词', text)
