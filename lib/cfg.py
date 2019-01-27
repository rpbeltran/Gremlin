class CFG_Nonterm:
    cnt = 0
    def __init__(self):
        CFG_Nonterm.cnt += 1
        self.name = 'N' + str(CFG_Nonterm.cnt)
        self.num = CFG_Nonterm.cnt
    def __str__(self):
        return self.name
    __repr__ = __str__
    def __hash__(self):
        return hash(self.num)
    def __eq__(self, other):
        return isinstance(other, CFG_Nonterm) and self.num == other.num

def hasEmptyForm(rhs, empSet):
    for x in rhs:
        if not isinstance(x, CFG_Nonterm):
            return False
        if not x in empSet:
            return False
    return True

def noReps(lst):
    newLst = []
    for x in lst:
        if not x in newLst:
            newLst.append(x)
    return newLst

class CFG:
    def __init__(self):
        self.start = CFG_Nonterm()
        self.nonterms = [self.start]
        self.productions = {}
    def addNonterm(self):
        newNonterm = CFG_Nonterm()
        self.nonterms.append(newNonterm)
        return newNonterm
    def addProduction(self, lhs, rhs):
        assert isinstance(lhs, CFG_Nonterm)
        assert isinstance(rhs, list)
        if not lhs in self.productions:
            self.productions[lhs] = []
        if not rhs in self.productions[lhs]:
            self.productions[lhs].append(rhs)

    def __str__(self):
        ret = 'Start: ' + str(self.start) + '\n'
        for lhs, rhsSet in self.productions.items():
            ret += str(lhs) + ' ->'
            conn = False
            for rhs in rhsSet:
                if conn:
                    ret += ' |'
                if len(rhs) == 0:
                    ret += ' epsilon'
                for x in rhs:
                    ret += ' ' + str(x)
                conn = True
            ret += '\n'
        return ret
    def __repr__(self):
        ret = 'Start: ' + repr(self.start) + '\n'
        for lhs, rhsSet in self.productions.items():
            ret += repr(lhs) + ' ->'
            conn = False
            for rhs in rhsSet:
                if conn:
                    ret += ' |'
                if len(rhs) == 0:
                    ret += ' epsilon'
                for x in rhs:
                    ret += ' ' + repr(x)
                conn = True
            ret += '\n'
        return ret

    def eliminateStart(self):
        newStart = self.addNonterm()
        self.addProduction(newStart, [self.start])
        self.start = newStart
    def eliminateTerms(self):
        termRules = {}
        for lhs, rhsSet in self.productions.items():
            for rhs in rhsSet:
                if len(rhs) > 1:
                    for i in range(len(rhs)):
                        if not isinstance(rhs[i], CFG_Nonterm):
                            if not rhs[i] in termRules:
                                termRules[rhs[i]] = self.addNonterm()
                            rhs[i] = termRules[rhs[i]]
        for term, nonterm in termRules.items():
            self.addProduction(nonterm, [term])
    def makeBinaryTerms(self):
        P = self.productions
        searchDict = { a:[x for x in b if len(x) > 2] for a, b in P.items() }
        self.productions = { a:[x for x in b if len(x) < 3] for a, b in P.items() }
        for lhs, rhsSet in searchDict.items():
            for rhs in rhsSet:
                rng = range(len(rhs) - 2)
                nterms = [self.addNonterm() for _ in rng]
                nterms.append(lhs)
                nterms = nterms[::-1]
                for i in rng:
                    self.addProduction(nterms[i], [rhs[i], nterms[i + 1]])
                self.addProduction(nterms[-1], [rhs[-2], rhs[-1]])
    def eliminateEpsilons(self):
        P = self.productions
        empSet = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhsSet in P.items():
                if lhs in empSet:
                    continue
                for rhs in rhsSet:
                    if hasEmptyForm(rhs, empSet):
                        empSet.add(lhs)
                        changed = True
                        break
        for lhs in P.keys():
            rhsSet = P[lhs]
            P[lhs] = []
            for rhs in rhsSet:
                options = [[]]
                for x in rhs:
                    if x in empSet:
                        options.extend([o + [x] for o in options])
                    else:
                        options = [o + [x] for o in options]
                if lhs != self.start:
                    options = [o for o in options if o != []]
                P[lhs].extend(options)
            P[lhs] = noReps(P[lhs])
    def eliminateUnits(self):
        P = self.productions
        changed = True
        while changed:
            changed = False
            for lhs in P.keys():
                units  = [rhs[0] for rhs in P[lhs] if len(rhs) == 1 and    isinstance(rhs[0], CFG_Nonterm)]
                P[lhs] = [rhs    for rhs in P[lhs] if len(rhs) != 1 or not isinstance(rhs[0], CFG_Nonterm)]
                for nterm in units:
                    P[lhs].extend([rhs for rhs in P[nterm] if len(rhs) != 1 or lhs != rhs[0]])
                    P[lhs] = noReps(P[lhs])
                    changed = True

    def convertToCNF(self, **kwargs):
        if not kwargs.get('allow_recursive_start', False):
            self.eliminateStart()
        if not kwargs.get('allow_mixed_terms', False):
            self.eliminateTerms()
        if not kwargs.get('allow_long_rules', False):
            self.makeBinaryTerms()
        if not kwargs.get('allow_epsilon_rules', False):
            self.eliminateEpsilons()
        if not kwargs.get('allow_unit_rules', False):
            self.eliminateUnits()

    def findMember(self):
        memberDict = {}
        changed = True
        while changed:
            changed = False
            for lhs, rhsSet in self.productions.items():
                if lhs in memberDict:
                    continue
                for rhs in rhsSet:
                    member = []
                    for x in rhs:
                        if x in memberDict:
                            member.extend(memberDict[x])
                        elif isinstance(x, CFG_Nonterm):
                            member = None
                            break
                        else:
                            member.append(x)
                    if member != None:
                        if lhs == self.start:
                            return member
                        memberDict[lhs] = member
                        changed = True
                        break
        return None

if __name__ == '__main__':
    class Num:
        def __init__(self):
            pass
        def __str__(self):
            return 'Num'
        def __repr__(self):
            return 'Num'
        def __hash__(self):
            return hash(0)
        def __eq__(self, other):
            return isinstance(other, Num)

    gram = CFG()
    expr = gram.start
    term = gram.addNonterm()
    fact = gram.addNonterm()
    WS = gram.addNonterm()
    gram.addProduction(fact, [WS, Num(), WS])
    gram.addProduction(fact, [WS, '-', Num(), WS])
    gram.addProduction(fact, [WS, '(', expr, ')', WS])
    gram.addProduction(term, [term, WS, '*', WS, fact])
    gram.addProduction(term, [term, WS, '/', WS, fact])
    gram.addProduction(term, [WS, fact, WS])
    gram.addProduction(expr, [expr, '+', term])
    gram.addProduction(expr, [expr, '-', term])
    gram.addProduction(expr, [WS, term, WS])
    gram.addProduction(WS, [WS, '\t'])
    gram.addProduction(WS, [WS, ' '])
    gram.addProduction(WS, [])

    print(repr(gram))
    print(gram.findMember())

    gram.convertToCNF()
    print(repr(gram))
    print(gram.findMember())
