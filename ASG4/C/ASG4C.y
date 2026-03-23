%{
#include<stdio.h>
#include<stdlib.h>

int yylex();
void yyerror(const char *s);
%}

%token A N U

%%
a : A N
  | a A
  | a N
  | a U a
  | a U N
  | A
  ;
%%

int main()
{
    printf("enter the string: ");
    yyparse();
    printf("valid variable\n");
    return 0;
}

void yyerror(const char *s)
{
    printf("invalid variable\n");
    exit(0);
}