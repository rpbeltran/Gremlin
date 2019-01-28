from lib.levenshtein import levenshtein_automata
from lib.algorithms import intersect
from lib.nfa import NFA
from lib.parser import Parser



def tokenize( program ):

    program += ' '

    block = ''

    tokens = []

    for c in program:

        if c == '{' or c == '}':

            if len( block ):

                tokens.append( 'UNARY' )
                block = ""

            tokens.append( "'%s'"%c )

        elif c in ' \t\n\r':

            if len( block ):

                tokens.append( 'UNARY' )
                block = ''

        elif c == ',':

            if len( block ):
                tokens.append( 'UNARY' )
                block = ''

            tokens.append( "','" )

        else:

            block += c

    return tokens


def main(grammarFile, tokenizer, testString):
    
    parser = Parser( grammarFile, tokenizer )

    testString = parser.process_input( testString )

    print( 'tokenization: ' + ' '.join( map( lambda s : s.replace( '\'', '' ) , ( testString ) ) ) )

    parser.cfg.convertToCNF(allow_recursive_start = True,
        allow_mixed_terms = False,
        allow_epsilon_rules = True,
        allow_unit_rules = True)

    if parser.cfg.findMember() == None:
        return None, INF

    def runTest(k):
        lev   = levenshtein_automata(testString, k)
        inter = intersect(parser.cfg, lev)
        return inter.findMember()


    if runTest(0) != None:
        return testString, 0


    mn = 0 # exclusive
    mx = 1 # inclusive
    match = runTest(mx)
    while match == None:
        mn = mx
        mx *= 2
        match = runTest(mx)

    maxMatch = match
    while mx - mn > 1:
        h = (mx + mn)//2
        match = runTest(h)
        if match == None:
            mn = h
        else:
            mx = h
            maxMatch = match

    return (maxMatch, mx)


if __name__ == '__main__':

    input_string = r'{ a , a a a a a a }'

    print( 'Original: ' + input_string )

    tokens, k, = main( 'examples/set.yacc', tokenize,  input_string )
    
    print( 'Levenshtein distance: ' + str(k) )

    print( 'Interpretation: ' + ' '.join( map( lambda s : s.replace( '\'', '' ) , ( tokens ) ) ) )


