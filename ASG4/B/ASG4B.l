%{
#include "y.tab.h"
#include <stdlib.h>
#include <string.h>
%}

%%
[0-9]+          { yylval.num = atoi(yytext); return NUMBER; }

sqrt            { return SQRT; }
strlen          { return STRLEN; }

\"[^\"]*\"      { 
                    yylval.str = strdup(yytext);
                    return STRING;
                }

[ \t\n]         ;   /* ignore whitespace */

.               { return yytext[0]; }
%%

int yywrap() {
    return 1;
}