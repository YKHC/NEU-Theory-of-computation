#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_INPUT_SIZE 128
#define MAX_DATA_SIZE 20000

char a[100][100][100];
int Numforsentence[7];
char database[MAX_DATA_SIZE];
char datadeal[MAX_DATA_SIZE];
int grammernow = 0;
int position;
char settext[MAX_DATA_SIZE];
char statenow;
int totGrammer;

void readFromFile(const char* fileName, char* destination, size_t maxSize) {
    FILE* file = fopen(fileName, "r");
    if (file == NULL) {
        perror("打开文件出错");
        exit(1);
    }

    size_t bytesRead = fread(destination, 1, maxSize, file);
    destination[bytesRead] = '\0';

    fclose(file);
}

void initializeData() {
    readFromFile("in.txt", database, MAX_DATA_SIZE);

    int check = 0;
    totGrammer = 1;
    int littlecheck = 1;

    for (int i = 0; i < strlen(database); i++) {
        if (database[i] == '\n') {
            if (database[i + 1] == '\n') {
                Numforsentence[totGrammer] = littlecheck;
                littlecheck = 0;
                totGrammer++;
            } else {
                littlecheck++;
            }
            continue;
        }
        if (database[i] == ' ') {
            continue;
        }
        a[totGrammer][littlecheck][check] = database[i];
        check++;
        check %= 5;
    }
    Numforsentence[totGrammer] = littlecheck;
}

void selectGrammar() {
    char input[MAX_INPUT_SIZE];
    printf("请选择语法：\n");
    printf("1. 0^n1^n\n");
    printf("2. 减法(格式为000100)\n");
    printf("3.读取wcw，w∈{0,1}的正闭包\n");
    fgets(input, MAX_INPUT_SIZE, stdin);

    if (strlen(input) == 0 || input[0] == '\n') {
        printf("输入为空。请选择一个语法。\n");
        exit(1);
    }

    input[strlen(input) - 1] = '\0'; // 去除末尾的换行符

    if (strlen(input) != 1 || (input[0] < '1' || input[0] > '3')) {
        printf("无效的输入。请选择有效的语法编号（1、2、3）。\n");
        exit(1);
    }

    grammernow = input[0] - '0';
    printf("成功选择了语法 %d。\n", grammernow);
}

void readSentence() {
    char input[MAX_INPUT_SIZE];
    printf("请输入一个句子：");
    fgets(input, MAX_INPUT_SIZE, stdin);

    if (strlen(input) == 0 || input[0] == '\n') {
        printf("输入为空。请提供一个句子。\n");
        exit(1);
    }

    input[strlen(input) - 1] = '\0'; // 去除末尾的换行符

    if (strlen(input) == 0) {
        printf("不合法。\n");
        exit(1);
    }

    for (int i = 0; i < strlen(input); i++) {
        datadeal[i + 1] = input[i];
    }

    datadeal[strlen(input) + 1] = 'B';  // 在末尾添加'B'
    datadeal[strlen(input) + 2] = '\0';  // 字符串末尾添加null

    datadeal[0] = 'B'; // 将第一个字符设置为'B'

    position = 1;
    statenow = '0';
}

int executeRules() {
    while (statenow != '#') {
        int trigger = 0;
        for (int i = 1; i <= Numforsentence[grammernow]; i++) {
            if (a[grammernow][i][0] == statenow && a[grammernow][i][1] == datadeal[position]) {
                statenow = a[grammernow][i][2];
                datadeal[position] = a[grammernow][i][3];

                if (a[grammernow][i][4] == 'R') {
                    if (position == strlen(datadeal) - 1) {
                        datadeal[position + 1] = 'B';
                        datadeal[position + 2] = '\0';
                    }
                    position++;
                } else {
                    if (a[grammernow][i][4] == 'L') {
                        if (position == strlen(datadeal) - 1) {
                            datadeal[position + 1] = 'B';
                            datadeal[position + 2] = '\0';
                        }
                        position--;
                    }
                }
                trigger = 1;
                break;
            }
        }
        if (!trigger) {
            printf("不合法。\n");
            return 1;
        }
    }

    settext[0] = '\0';
    strcpy(settext, datadeal);

    int pp = strlen(settext) + 1;
    settext[pp - 1] = '\n';

    for (int i = 1; i <= position; i++) {
        settext[pp] = ' ';
        pp++;
    }

    settext[pp] = '*';
    settext[pp + 1] = '\0';

    return 0;
}

int main() {
    initializeData();
    selectGrammar();
    readSentence();
    int result = executeRules();

    if (result == 0) {
        // 输出 settext
        printf("%s\n", settext);
        printf("输入合法。\n");
    }

    return result;
}
