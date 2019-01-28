
%start a

%%

a : '(' ')' | '(' a ')' | a a ;

%%