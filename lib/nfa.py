
class Epsilon:

	def __eq__( self, b ):

		return isinstance( b, Epsilon )

	
	def __hash__( self ):

		return hash( str( self ) )


	def __str__( self ):

		return "epsilon"

	__repr__ = __str__

EPSILON  = Epsilon()


class Wildcard:

	def __eq__( self, b ):

		return isinstance( b, Wildcard )

	
	def __hash__( self ):

		return hash( str( self ) )


	def __str__( self ):

		return "wildcard"

	__repr__ = __str__

WILDCARD = Wildcard()


class NFA:

	epsilon = Epsilon()

	def __init__( self, states = set([]), start = None, final = set([]), transitions = {} ):

		self.states = states
		self.start  = start
		self.final  = final

		self.transitions = transitions

		self.epsilon_resolved = self.finals_combined = False

		self.next_id = 1+max(states) if len(states) else 0


	# Build

	def set_start( self, state ):

		self.start = state

	def make_final( self, state ):

		self.final.add( state )

	def add_state( self, state ):

		self.states.add( state )

		self.next_id = max( state, self.next_id ) + 1

	def add_transition( self, a, b, sym ):

		if a not in self.transitions:
			self.transitions[a] = {}
		if sym not in self.transitions[a]:
			self.transitions[a][sym] = set([])

		self.transitions[a][sym].add( b )


	# Modify

	def normalize( self ):

		self.combine_finals()
		self.resolve_epsilons()		

	def combine_finals( self ):

		new_state = self.next_id

		if len( self.final ) > 1:

			for f in self.final:

				self.add_transition( f, new_state, EPSILON )

			self.add_state( new_state )

			self.final = new_state

			return

		for f in self.final:

			self.final = f

	def resolve_epsilons( self ):

		epsilon_found = True

		while epsilon_found:

			epsilon_found = False

			for a in self.transitions.keys():

				if EPSILON not in self.transitions[a]:

					continue

				for b in self.transitions[a][EPSILON]:

					for c in self.transitions.keys():

						# ( c --sym--> a ) => ( c --sym--> b )

						for sym in self.transitions[c].keys():

							if a in self.transitions[c][sym]:

								self.add_transition( c, b, sym )

				del self.transitions[a][EPSILON]

				epsilon_found = True


	# Builtins

	def __str__( self ):

		ret = ""

		for state in self.states:

			if state in self.transitions:

				ret += '\n' + str(state) + " : " + str(self.transitions[state] )

			else:

				ret += '\n' + str(state) + " : "

		ret += "\nstart : " + str( self.start )
		ret += "\nfinal : " + str( self.final )

		return ret




if __name__ == '__main__':	
			
	nfa = NFA()

	nfa.add_state( 1 )
	nfa.add_state( 2 )
	nfa.add_state( 3 )

	nfa.add_transition( 1, 2, 'a' )
	nfa.add_transition( 2, 3, 'b' )
	nfa.add_transition( 2, 1, EPSILON )
	nfa.add_transition( 3, 2, EPSILON )

	nfa.set_start( 1 )

	nfa.make_final( 3 )

	nfa.normalize()

	print(nfa)




