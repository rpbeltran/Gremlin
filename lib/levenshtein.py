
if __name__ == '__main__':
	from nfa import NFA, EPSILON, WILDCARD
else:
	from lib.nfa import NFA, EPSILON, WILDCARD



def levenshtein_automata( tokens, k ):

	l = len( tokens )

	nfa = NFA( states = set(range((l+1)*(k+1))) )

	# Insert forward edges

	for i in range( l ):

		for j in range( k + 1 ):

			nfa.add_transition( (j*(l+1))+i, (j*(l+1))+i+1, tokens[i] )

	# Insert lifting edges

	for row in range( k ):

		for col in range( l + 1 ):

			nfa.add_transition( (row*(l+1))+col, ((row+1)*(l+1))+col, WILDCARD )

	# Insert Diagnol

	for row in range( k ):

		for col in range( l ):

			nfa.add_transition( (row*(l+1))+col, ((row+1)*(l+1))+col+1, EPSILON  )
			nfa.add_transition( (row*(l+1))+col, ((row+1)*(l+1))+col+1, WILDCARD )


	nfa.set_start( 0 )

	for i in range( k + 1 ):

		nfa.make_final( i*(l+1) + l )

	nfa.normalize()

	return nfa



if __name__ == '__main__':
	
	a = [1,2,'a']
	print ( levenshtein_automata( a, 5 ) )
	print ( levenshtein_automata( [1], 0 ) )

