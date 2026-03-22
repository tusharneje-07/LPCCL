%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* Define the structure for the Symbol Table node */
struct symnode {
    char word[50];
    char pos[20];
    struct symnode *next;
};

struct symnode *head = NULL;

/* Function to insert a word and its part of speech into the symbol table */
void insert(char *w, char *p) {
    struct symnode *ptr = head;
    
    /* Check if the word already exists in the symbol table */
    while(ptr != NULL) {
        if(strcmp(ptr->word, w) == 0) {
            return; /* Word already in symbol table, skip insertion */
        }
        ptr = ptr->next;
    }
    
    /* Create a new node and add it to the head of the list */
    struct symnode *newnode = (struct symnode *)malloc(sizeof(struct symnode));
    strcpy(newnode->word, w);
    strcpy(newnode->pos, p);
    newnode->next = head;
    head = newnode;
}

/* Function to display the symbol table */
void display() {
    struct symnode *ptr = head;
    printf("\n\n--- SYMBOL TABLE ---\n");
    printf("%-20s | %-15s\n", "WORD", "PART OF SPEECH");
    printf("----------------------------------------\n");
    while(ptr != NULL) {
        printf("%-20s | %-15s\n", ptr->word, ptr->pos);
        ptr = ptr->next;
    }
    printf("----------------------------------------\n");
}
%}

%%
    /* Lex Rules for Parts of Speech based on the provided subset */

"car"|"house"|"man"|"state"|"ocean"|"country"|"city"              { insert(yytext, "NOUN"); }
"She"|"he"|"we"|"they"|"it"                                       { insert(yytext, "PRONOUN"); }
"Come"|"go"|"walk"|"did"|"have"|"read"|"write"                    { insert(yytext, "VERB"); }
"Pretty"|"Old"|"Blue"|"smart"                                     { insert(yytext, "ADJECTIVE"); }
"abnormally"|"accidentally"|"actually"|"beautifully"|"bitterly"|"brightly"|"calmly" { insert(yytext, "ADVERB"); }
"By"|"with"|"About"|"until"                                       { insert(yytext, "PREPOSITION"); }
"And"|"but"|"or"|"while"|"because"                                { insert(yytext, "CONJUNCTION"); }
"Oh!"|"Wow!"|"Oops!"                                              { insert(yytext, "INTERJECTION"); }

[a-zA-Z]+                                                         { insert(yytext, "UNKNOWN"); }
[ \t\n.,]                                                         { /* Ignore whitespace and standard punctuation */ }
.                                                                 { /* Ignore any other characters */ }
%%

int yywrap() {
    return 1;
}

int main() {
    printf("Enter English text (Press Ctrl+D on Linux/Mac or Ctrl+Z on Windows to stop):\n");
    yylex();
    display();
    return 0;
}