%{
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

int yylex();
void yyerror(const char *s);
%}

%union {
    int num;
    char *str;
}

%token <num> NUMBER
%token <str> STRING
%token SQRT STRLEN

%type <num> expr

%%

input:
    expr { 
        printf("Result = %d\n", $1); 
        exit(0);   // terminate after one input
    }
    ;

expr:
      SQRT '(' NUMBER ')'   
        { $$ = (int)sqrt($3); }

    | STRLEN '(' STRING ')' 
        { $$ = strlen($3) - 2; }  /* remove quotes */
    ;

%%

void yyerror(const char *s) {
    printf("Error: %s\n", s);
}

int main() {
    printf("Enter function: ");
    yyparse();
    return 0;
}