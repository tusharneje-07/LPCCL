%{
#include <stdio.h>
#include <string.h>

#define MAX 100

char symtab[MAX][50];
int count = 0;

/* Search identifier */
int search(char *str) {
    for(int i = 0; i < count; i++) {
        if(strcmp(symtab[i], str) == 0)
            return i;
    }
    return -1;
}

/* Insert identifier */
void insert(char *str) {
    if(search(str) == -1 && count < MAX) {
        strcpy(symtab[count], str);
        count++;
    }
}
%}

DIGIT      [0-9]
LETTER     [a-zA-Z]
ID         {LETTER}({LETTER}|{DIGIT})*
NUM        {DIGIT}+(\.{DIGIT}+)?

%%

"if"        { printf("KEYWORD: %s\n", yytext); }
"while"     { printf("KEYWORD: %s\n", yytext); }
"for"       { printf("KEYWORD: %s\n", yytext); }
"printf"    { printf("KEYWORD: %s\n", yytext); }

"%d"        { printf("FORMAT SPECIFIER: %s\n", yytext); }
"%c"        { printf("FORMAT SPECIFIER: %s\n", yytext); }
"%s"        { printf("FORMAT SPECIFIER: %s\n", yytext); }
"%f"        { printf("FORMAT SPECIFIER: %s\n", yytext); }

"=="        { printf("RELATIONAL OPERATOR: %s\n", yytext); }
"<="        { printf("RELATIONAL OPERATOR: %s\n", yytext); }
">="        { printf("RELATIONAL OPERATOR: %s\n", yytext); }
"<"         { printf("RELATIONAL OPERATOR: %s\n", yytext); }
">"         { printf("RELATIONAL OPERATOR: %s\n", yytext); }

"&&"        { printf("LOGICAL OPERATOR: %s\n", yytext); }
"||"        { printf("LOGICAL OPERATOR: %s\n", yytext); }

"+"         { printf("ARITHMETIC OPERATOR: %s\n", yytext); }
"-"         { printf("ARITHMETIC OPERATOR: %s\n", yytext); }
"*"         { printf("ARITHMETIC OPERATOR: %s\n", yytext); }
"/"         { printf("ARITHMETIC OPERATOR: %s\n", yytext); }
"%"         { printf("ARITHMETIC OPERATOR: %s\n", yytext); }

";"         { printf("PUNCTUATION: %s\n", yytext); }
","         { printf("PUNCTUATION: %s\n", yytext); }
"("         { printf("PUNCTUATION: %s\n", yytext); }
")"         { printf("PUNCTUATION: %s\n", yytext); }
"{"         { printf("PUNCTUATION: %s\n", yytext); }
"}"         { printf("PUNCTUATION: %s\n", yytext); }
"["         { printf("PUNCTUATION: %s\n", yytext); }
"]"         { printf("PUNCTUATION: %s\n", yytext); }
"#"         { printf("PUNCTUATION: %s\n", yytext); }

{NUM}       { printf("NUMBER: %s\n", yytext); }

{ID}        { printf("IDENTIFIER: %s\n", yytext); insert(yytext); }

[ \t\n]+    ;

.           { printf("UNKNOWN: %s\n", yytext); }

%%

int main() {
    yylex();

    printf("\n----- SYMBOL TABLE -----\n");
    printf("Index\tIdentifier\n");

    for(int i = 0; i < count; i++) {
        printf("%d\t%s\n", i, symtab[i]);
    }

    return 0;
}

int yywrap() {
    return 1;
}


*/
>>> // lex ASG3A.l && gcc lex.yy.c -o ASG3A && ./ASG3A < code.c

#include <stdio.h>

int main() {
    int a = 10, b = 20;
    float result = 0.0;

    if (a < b && b > 0) {
        result = a + b * 2;
        printf("Sum is: %d\n", result);
    }

    for (int i = 0; i < 5; i++) {
        printf("Value: %d\n", i);
    }

    while (a <= b) {
        a = a + 1;
    }

    return 0;
}

/*