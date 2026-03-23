%{
#include<stdio.h>
#include<stdlib.h>

int yylex();
void yyerror(const char *s);
%}

%token NUM PLUS MINUS MUL DIV LPAREN RPAREN

%%

S : E { printf("Result = %d\n", $1); }
  ;

E : E PLUS T   { $$ = $1 + $3; }
  | E MINUS T  { $$ = $1 - $3; }
  | T          { $$ = $1; }
  ;

T : T MUL F    { $$ = $1 * $3; }
  | T DIV F    { $$ = $1 / $3; }
  | F          { $$ = $1; }
  ;

F : LPAREN E RPAREN { $$ = $2; }
  | NUM              { $$ = $1; }
  ;

%%

int main()
{
    printf("Enter Expression: ");
    yyparse();
    return 0;
}

void yyerror(const char *s)
{
    printf("Invalid Expression\n");
}