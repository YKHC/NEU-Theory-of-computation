# NEU-Theory-of-computation
东北大学 计算理论 图灵机作业

可以通过在in.txt、info.txt内增加，来拓展这个程序

initializeData(): 从文件中读取数据，解析语法规则，初始化全局数组和变量。
selectGrammar(): 要求用户选择一个语法，检查输入的有效性，设置grammernow为所选语法。
readSentence(): 要求用户输入一个句子，将其处理成特定格式，初始化datadeal、position和statenow。
executeRules(): 根据语法规则，处理datadeal中的句子，直到达到终止状态，同时生成settext。
main(): 主函数，协调整个程序的执行流程，包括初始化、语法选择、句子读取、规则执行和结果输出。

a: 存储语法规则的数组。
Numforsentence: 存储每个语法的规则数量。
database: 用于存储从文件读取的数据。
datadeal: 存储处理后的句子数据。
grammernow: 选择的语法编号。
position: 当前句子处理位置。
settext: 存储最终生成的文本。
statenow: 当前状态。
totGrammer: 存储语法总数。
