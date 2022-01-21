# -*- coding:utf-8 -*-
import os
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import Toplevel
import pyperclip
import json

import cut_word
from jieba_cut import jieba_cut, keyword
from transformFiles import filesInFolder

text = [""]  # 全局裁判文书
fontSize = 12
width = 80
font = ("Arial Bold", fontSize)
factors = ['案由', '关键词', '原告', '被告', '裁判结果', '涉案法条', '裁判日期', '法院', '案号']
txtarea_row_span = 8
txtarea_column_span = 4
Max_column = 1
Max_row = 15


# 选择子窗口类
class selectWord(Toplevel):
    chks = []
    words = []
    check = {}
    choosed = []
    Max_items = Max_row * Max_column
    Max_row = 5
    Max_column = 5
    page = 0
    row = 1  # 当前行
    column = 0  # 当前列
    genders_dict = {0:'name', 1:'adj', 2:'v', 3:'special'}

    def __init__(self, num, gender = -1):
        super().__init__()
        self.Max_row = Max_row
        self.Max_column = Max_column
        self.Max_items = Max_row * Max_column
        self.chks = []
        self.check = {}
        self.choosed = []
        self.title(factors[num])
        if gender < 0 :
            self.words = self.cutWords(num)
        else:
            if num == 1:
                self.words = keyword(text[0])
                # print('keyword')
            else:self.words = jieba_cut(text[0])[self.genders_dict[gender]]
            # print(self.genders_dict[gender])
        # print('words is ', self.words)
        # 弹窗界面
        self.setup_UI()

    # 针对不同项目的分词方案
    def cutWords(self, num):
        words = cut_word.get_words(factor=factors[num], text=text[0])
        if words == None:
            return []
        else:
            return words

    # 获取下一列行
    def nextcr(self):
        column = self.column
        row = self.row
        if self.column == self.Max_column - 1:
            self.column = 0
            self.row = self.row + 1
        else:
            self.column = self.column + 1
        return column, row

    # 启动窗口
    def setup_UI(self):

        # 分词复选框
        for i in self.words:
            chk_state = BooleanVar()
            chk_state.set(False)  # Set check state
            self.check[i] = chk_state
        for chk in list(self.check.items())[0:self.Max_items]:
            self.chks.append(Checkbutton(self, font=font, text=chk[0], var=chk[1]))
            column, row = self.nextcr()
            self.chks[-1].grid(column=column, row=row)

        # 保存和取消
        def save():
            self.choosed = [key for (key, value) in self.check.items() if value.get() == TRUE]
            self.destroy()  # 销毁窗口

        def cancel():
            self.choosed = None
            self.destroy()

        # 翻页
        def nextPage():
            self.column = 0
            self.row = 1
            for chk in self.chks.__reversed__():
                chk.destroy()
                self.chks.remove(chk)
            self.page = self.page + 1
            for chk in list(self.check.items())[self.page * self.Max_items:(self.page + 1) * self.Max_items]:
                column, row = self.nextcr()
                self.chks.append(Checkbutton(self, font=font, text=chk[0], var=chk[1]))
                self.chks[-1].grid(column=column, row=row)

        def prePage():
            self.column = 0
            self.row = 1
            for chk in self.chks.__reversed__():
                self.chks.remove(chk)
                chk.destroy()
            self.page = self.page - 1
            for chk in list(self.check.items())[self.page * self.Max_items:(self.page + 1) * self.Max_items]:
                column, row = self.nextcr()
                self.chks.append(Checkbutton(self, font=font, text=chk[0], var=chk[1]))
                self.chks[-1].grid(column=column, row=row)

        Button(self, text='上一页', font=font, command=prePage).grid(column=2, row=0)
        Button(self, text='下一页', font=font, command=nextPage).grid(column=3, row=0)
        Button(self, text='选择', font=font, command=save).grid(column=0, row=0)
        Button(self, text='取消', font=font, command=cancel).grid(column=1, row=0)


def run():
    window = Tk()
    window.title("裁判文书")
    # 文本区
    txtarea = scrolledtext.ScrolledText(window, font=font)
    txtarea.grid(column=1, row=0, rowspan=txtarea_row_span, columnspan = txtarea_column_span)

    # 选择文书
    def btnFileSelect_command():
        try:
            file = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            f = open(file)
            txt = f.read()
            text[0] = txt
            txtarea.delete(1.0, END)
            txtarea.insert(INSERT, txt)
        except Exception as e:
            pass
        finally:
            try:
                f.close()
            except:
                pass

    btnFileSelect = Button(window, text="选择文书", font=font, command=btnFileSelect_command)
    btnFileSelect.grid(column=0, row=0)

    # 输入文书
    def btnInput_command():
        txt = pyperclip.paste()
        text[0] = txt
        txtarea.delete(1.0, END)
        txtarea.insert(INSERT, txt)

    btnInput = Button(window, font=font, text="粘贴文书", command=btnInput_command)
    btnInput.grid(column=0, row=1)

    # 创建各标记
    txts = []  # 标记输入框集合
    num = 0
    selected = IntVar()
    # 创建单选标记，输入框
    isOpen = [False]

    def btnSelect_comand():
        if isOpen[0]: return
        isOpen[0] = True
        text[0] = txtarea.get('1.0', 'end-1c')
        # print('now textarea is', text[0])
        openIndex = selected.get()
        select = selectWord(openIndex)
        window.wait_window(select)
        isOpen[0] = False
        choosed = select.choosed
        if choosed == None: return
        txts[openIndex].delete(0, END)
        txts[openIndex].insert(INSERT, ';'.join(choosed))

    for factor in factors:
        Radiobutton(window, font=font, value=num, variable=selected, text=factor).grid(
            column=0, row=num + txtarea_row_span)
        txts.append(Entry(window, font=font, width=width))
        txts[num].grid(column=1, row=num + txtarea_row_span, columnspan = txtarea_column_span)
        num = num + 1

    # 选词子窗口
    btnSelect = Button(window, font=font, command=btnSelect_comand, text="选词")
    btnSelect.grid(column=0, row=2)

    # 保存按钮
    def btnSave_command():
        dic = {}
        for i in range(0, factors.__len__()):
            dic[factors[i]] = (str)(txts[i].get())

        f = open(txts[-1].get() + '.txt', 'w')
        f.write(txtarea.get('1.0', 'end-1c'))
        f.close()

        f = open(txts[-1].get() + '.json', 'w')
        json.dump(dic, f, ensure_ascii=False)
        f.close()

    btnSave = Button(window, font=font, text="保存", command=btnSave_command)
    btnSave.grid(column=0, row=3)

    # 清空
    def btnClear_command():
        txtarea.delete(1.0, END)
        for txt in txts:
            txt.delete(0, END)

    btnClear = Button(window, font=font, text="清空", command=btnClear_command)
    btnClear.grid(column=0, row=4)

    # 文件夹
    dir = ['']
    dirindex = [0]
    txtsname = [[]]

    def btnDir_command():
        dirindex[0] = 0
        dir[0] = filedialog.askdirectory()
        txtsname[0] = filesInFolder(dir[0], '.txt')
        if dirindex[0] == txtsname[0].__len__(): return
        f = open(dir[0] + r'/' + txtsname[0][dirindex[0]])
        txtarea.delete(1.0, END)
        for txt in txts:
            txt.delete(0, END)
        txtarea.insert(INSERT, f.read())
        dirindex[0] = dirindex[0] + 1

    def btnNextOne_command():
        # print(txtsname[0].__len__())
        if dirindex[0] == txtsname[0].__len__(): return
        for txt in txts:
            txt.delete(0, END)
        f = open(dir[0] + r'/' + txtsname[0][dirindex[0]])
        txtarea.delete(1.0, END)
        txtarea.insert(INSERT, f.read())
        dirindex[0] = dirindex[0] + 1

    def btnPreOne_command():
        if dirindex[0] <= 1: return
        for txt in txts:
            txt.delete(0, END)
        dirindex[0] = dirindex[0] - 2
        f = open(dir[0] + r'/' + txtsname[0][dirindex[0]])
        txtarea.delete(1.0, END)
        txtarea.insert(INSERT, f.read())
        dirindex[0] = dirindex[0] + 1

    btnDir = Button(window, font=font, text="文件夹", command=btnDir_command).grid(column=0, row=5)
    btnNextOne = Button(window, font=font, text="下一个", command=btnNextOne_command).grid(column=0, row=7)
    btnPreOne = Button(window, font=font, text="上一个", command=btnPreOne_command).grid(column=0, row=6)

    #词性选词
    gender_check = IntVar()
    genders = ['名词', '形容词', '动词', '专有']
    def btnGender_command():
        if isOpen[0]: return
        isOpen[0] = True
        text[0] = txtarea.get('1.0', 'end-1c')
        # print('now textarea is', text[0])
        openIndex = selected.get()
        genderIndex = gender_check.get()
        select = selectWord(openIndex, genderIndex)
        window.wait_window(select)
        isOpen[0] = False
        choosed = select.choosed
        if choosed == None: return
        txts[openIndex].delete(0, END)
        txts[openIndex].insert(INSERT, ';'.join(choosed))
    btnGender = Button(window, font=font, command=btnGender_command, text="分词").grid(column=0, row=txtarea_row_span + 9)
    for gender in range(0,4):
        Radiobutton(window, font=font, value=gender, variable=gender_check, text=genders[gender]).grid(
        column=gender + 1, row=txtarea_row_span + 9)

    # 启动窗口
    window.mainloop()


if __name__ == '__main__':
    run()
