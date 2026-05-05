%{
#include<stdio.h>
%}

%%
car|house|man|city|country        { printf("%-15s  ->  NOUN\n",yytext); }

he|she|they|we|i|it               { printf("%-15s  ->  PRONOUN\n",yytext); }

run|eat|drives|read|write|go      { printf("%-15s  ->  VERB\n",yytext); }

big|small|blue|fast|good          { printf("%-15s  ->  ADJECTIVE\n",yytext); }

quickly|slowly|very               { printf("%-15s  ->  ADVERB\n",yytext); }

in|on|at|with|under|over          { printf("%-15s  ->  PREPOSITION\n",yytext); }

and|or|but                        { printf("%-15s  ->  CONJUNCTION\n",yytext); }

oh|wow|oops                       { printf("%-15s  ->  INTERJECTION\n",yytext); }

a|an|the                          { printf("%-15s  ->  ARTICLE\n",yytext); }

[a-zA-Z]+                         { printf("%-15s  ->  UNKNOWN WORD OR TOKEN\n",yytext); }

[ \t\n]                           ;

%%

int main()
{
    printf("\nWORD             PART OF SPEECH\n");
    printf("-----------------------------------\n");

    yylex();
    return 0;
}

int yywrap()
{
    return 1;
}

// lex ASG3A.l && gcc lex.yy.c -o ASG3A && ./ASG3A < english.txt