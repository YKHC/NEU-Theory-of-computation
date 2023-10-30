import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

MAX_INPUT_SIZE = 128
MAX_DATA_SIZE = 20000

data_rules = {}
num_for_sentence = {}
database = ""
data_deal = ""
grammar_now = 0
position = 0
state_now = '0'
tot_grammar = 0
set_text = ""


def read_from_file(filename):
    global database
    with open(filename, 'r') as file:
        database = file.read()


def initialize_data():
    global tot_grammar, database

    check = 0
    tot_grammar = 1
    little_check = 1
    data_rules[tot_grammar] = []

    for i, char in enumerate(database):
        if char == '\n':
            if i + 1 < len(database) and database[i + 1] == '\n':
                num_for_sentence[tot_grammar] = little_check
                little_check = 0
                tot_grammar += 1
                data_rules[tot_grammar] = []
            else:
                little_check += 1
            continue
        if char == ' ':
            continue

        if len(data_rules[tot_grammar]) < little_check:
            data_rules[tot_grammar].append(['']*5)
        data_rules[tot_grammar][little_check - 1][check] = char

        check += 1
        check %= 5

    num_for_sentence[tot_grammar] = little_check


def select_grammar():
    global grammar_now
    grammar_now = simpledialog.askinteger("请选择语法", "1. 0^n1^n\n2. 减法(格式为000100)\n3.读取wcw，w∈{0,1}的正闭包\n\n请选择语法:")


def read_sentence():
    global data_deal, position, state_now
    sentence = simpledialog.askstring("Input", "输入句子:")
    if not sentence:
        messagebox.showerror("Error", "请输入合法的句子")
        return

    data_deal = 'B' + sentence + 'B'
    position = 1
    state_now = '0'


def execute_rules():
    global data_deal, position, state_now, set_text, grammar_now

    while state_now != '#':
        trigger = 0
        for i, rule in enumerate(data_rules[grammar_now]):
            if rule[0] == state_now and rule[1] == data_deal[position]:
                state_now = rule[2]
                data_deal = data_deal[:position] + rule[3] + data_deal[position+1:]

                if rule[4] == 'R':
                    position += 1
                    if position == len(data_deal) - 1:
                        data_deal += 'B'
                elif rule[4] == 'L':
                    position -= 1
                    if position == len(data_deal) - 1:
                        data_deal += 'B'

                trigger = 1
                break

        if not trigger:
            messagebox.showerror("Error", "不合法的输入")
            return

    set_text = data_deal + '\n' + (' ' * (position)) + '*'
    messagebox.showinfo("Result", set_text)


def main():
    root = tk.Tk()
    root.title("Turing machine")
    root.geometry("500x300")
    label = tk.Label(root, text="请按顺序点击每个按钮:")
    label.pack(pady=20)

    button1 = tk.Button(root, text="加载语法规则", command=lambda: [read_from_file('in.txt'), initialize_data()])
    button1.pack(pady=10)

    button2 = tk.Button(root, text="选择图灵机功能", command=select_grammar)
    button2.pack(pady=10)

    button3 = tk.Button(root, text="输入你的句子", command=read_sentence)
    button3.pack(pady=10)

    button4 = tk.Button(root, text="开始运行", command=execute_rules)
    button4.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()