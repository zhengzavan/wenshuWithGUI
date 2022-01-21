# -*- coding:utf-8 -*
import json

from transformFiles import filesInFolder

path = r'D:\Program Files\QQ\DATA\2535956107\FileRecv\批注后的文本'
names = filesInFolder(path, '.json')
result = {'驳回':0, '维持':0, '其他':0}
for name in names:
    with open(path + '\\' + name) as f:
        dic = json.load(f)
        # print(type(dic))
        if '驳回' in dic['裁判结果']:
            result['驳回'] = result['驳回'] + 1
        if '维持' in dic['裁判结果']:
            result['维持'] = result['维持'] + 1
        if '驳回' not in dic['裁判结果'] and '维持' not in dic['裁判结果']:
            result['其他'] = result['其他'] + 1
print(result)
