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

root = tk.Tk()
root.title("Turing machine")
root.geometry("500x300")


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

def center_window(win, width=400, height=200):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    win.geometry(f"{width}x{height}+{x}+{y}")

def show_custom_messagebox(message):
    message_window = tk.Toplevel(root)
    message_window.title("Message")
    message_window.geometry("400x200")
    center_window(message_window)
    message_label = tk.Label(message_window, text=message, wraplength=380, font=("Courier", 12))
    message_label.pack(expand=True)

    # 自动关闭窗口的功能
    def close_messagebox():
        message_window.destroy()

    message_window.after(2000, close_messagebox)


def execute_step():
    global data_deal, position, state_now, set_text, grammar_now

    if state_now == '#':
        # 如果状态为'#'，则表示图灵机结束运行，不需要再次显示字符串
        # set_text = data_deal + '\n' + (' ' * (position - 1)) + '*'
        # show_custom_messagebox(set_text)
        messagebox.showinfo("完成", "图灵机执行完成！")
        return  # 结束函数执行

    trigger = False
    for rule in data_rules[grammar_now]:
        if rule[0] == state_now and rule[1] == data_deal[position]:
            # 更新状态和字符串
            state_now = rule[2]
            data_deal = data_deal[:position] + rule[3] + data_deal[position + 1:]
            position += {'R': 1 , 'L': -1}.get(rule[4], 0)

            if position == len(data_deal):
                data_deal += 'B'  # 如果到达字符串末尾，添加'B'
            elif position < 0:
                data_deal = 'B' + data_deal  # 如果到达字符串开头，添加'B'
                position = 0

            # 展示当前字符串和读写头的位置
            set_text = data_deal + '\n' + (' ' * (position - 1)) + '*'
            show_custom_messagebox(set_text)

            trigger = True
            break

    if not trigger:
        messagebox.showerror("错误", "不合法的输入")
        return

    root.after(1000, execute_step)  # 延迟1秒调用execute_step



def execute_rules():
    # 首先显示原始的符号串
    initial_text = data_deal + '\n' + (' ' * (position - 1)) + '*'
    show_custom_messagebox(initial_text)

    root.after(2000, execute_step)  # 2秒后开始执行步骤

def main():
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


# 确保在这里调用root.mainloop()来启动Tkinter事件循环
if __name__ == "__main__":
    main()
    root.mainloop()

