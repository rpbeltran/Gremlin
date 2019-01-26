class CFG_Nonterm:
    cnt = 0
    def __init__(self):
        CFG_Nonterm.cnt += 1
        self.hasEmptyProd = False
        self.name = 'N' + str(CFG_Nonterm.cnt)
        self.num = CFG_Nonterm.cnt
    def __str__(self):
        return self.name
    def __repr__(self):
        if self.hasEmptyProd:
            return self.name + '(hasE)'
        else:
            return self.name + '(noE)'
    def __hash__(self):
        return hash(self.num)

def hasEmptyForm(rhs):
    for x in rhs:
        if not isinstance(x, CFG_Nonterm):
            return False
        if not x.hasEmptyProd:
            return False
    return True

class CFG:
    def __init__(self):
        self.isCNF = False
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
        if self.isCNF:
            ret = 'In Chomsky Normal Form:\n'
        else:
            ret = 'Not in Chomsky Normal Form:\n'
        ret += 'Start: ' + repr(self.start) + '\n'
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

    def propogateEmptyProd(self):
        changed = True
        while changed:
            changed = False
            for lhs, rhsSet in self.productions.items():
                if lhs.hasEmptyProd:
                    continue
                for rhs in rhsSet:
                    if hasEmptyForm(rhs):
                        lhs.hasEmptyProd = True
                        changed = True
                        break
    def eliminateStart(self):
        newStart = self.addNonterm()
        self.addProduction(newStart, [self.start])
        self.start = newStart

    def convertToCNF(self):
        if self.isCNF:
            return
        self.eliminateStart()
        self.propogateEmptyProd()
        self.isCNF = True

if __name__ == '__main__':
    class Num:
        def __init__(self):
            pass
        def __str__(self):
            return 'Num'
        def __repr__(self):
            return 'Num'

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

    print(gram)

    gram.convertToCNF()
    print(gram)
