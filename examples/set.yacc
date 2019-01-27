
%token	UNARY

%start set

%%

set : '{' set_contents '}' | '{' '}' ;

set_contents : UNARY | set | UNARY ',' set_contents | set ',' set_contents ;

%%