%{
#include "y.tab.h"
#include<stdio.h>
#include<stdlib.h>
%}

%%
[0-9]+      { yylval = atoi(yytext); return NUM; }
"+"         return PLUS;
"-"         return MINUS;
"*"         return MUL;
"/"         return DIV;
"("         return LPAREN;
")"         return RPAREN;
\n          return 0;
[ \t]       ;   /* ignore spaces */
.           return yytext[0];
%%

int yywrap()
{
    return 1;
}