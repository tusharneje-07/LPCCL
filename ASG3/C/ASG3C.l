%{
#include <stdio.h>
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
{ID}        { printf("IDENTIFIER: %s\n", yytext); }

[ \t\n]+    ;

.           { printf("UNKNOWN: %s\n", yytext); }

%%

int main() {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}