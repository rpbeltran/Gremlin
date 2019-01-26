
# GREMLIN

Levenshtein optimal interpretation of context free grammars for robust semantic analysis



## Usage and Syntax

Gremlin parses grammars encoded with YACC-styled production rule syntax, though the following changes are made:

    * Terminating productions with semicolons is an optional practice
    * If time permits: Accepts REGEX patterns


/* Example: set.gram */

    SET : start_set SET_CONTENTS end_set
    SET_CONTENTS : /* empty */ 
                 | unary (comma unary)*

    
/* Example: set_checker.py */

    from gremlin import Engine, Token, Parser

    start_set = Token( r'{' )
	end_set   = Token( r'}' )
	unary     = Token( r'\w+' )
	comma     = Token( r',' )

    set_engine = Engine( "set.gram", [ start_set, end_set, unary, comma ] )

    token_string = set_engine.


## Required Sub-tasks and algorithms:

    1. Parser
    2. Abstract NFA
    3. Levenshtein Automata
    4. NFA -> RG
    5. Abstract CFG
    6. Arbitrary CFG -> CNF
    7. Check if a context free grammar is empty
    8. Find member of a context free grammar
    9. (optional) Regex -> RG

