
if __name__ == '__main__':
    from cfg import CFG
    from nfa import NFA, WILDCARD
else:
    from lib.cfg import CFG
    from lib.nfa import NFA, WILDCARD


# CFG intersection of a CFG c and an NFA n
def intersect(cfg, nfa):
    ret = CFG()
    Nt = cfg.nonterms
    St = list(nfa.states)
    for _ in range(len(Nt) * len(St)**2  -  1):
        ret.addNonterm()
    NtInv = { Nt[i]:i for i in range(len(Nt)) }
    StInv = { St[i]:i for i in range(len(St)) }
    def getNterm(p, A, q):
        idx = (NtInv[A]*len(St) + StInv[p])*len(St) + StInv[q]
        return ret.nonterms[idx]
    ret.start = getNterm(nfa.start, cfg.start, nfa.final)
    for lhs, rhsSet in cfg.productions.items():
        for rhs in rhsSet:
            items = [(x, [], x) for x in St]
            for term in rhs:
                if term in Nt:
                    newItems = []
                    for z in St:
                        newItems.extend([(x, R + [getNterm(y, term, z)], z) for (x, R, y) in items])
                    items = newItems
                else:
                    newItems = []
                    for (x, R, y) in items:
                        newItems.extend([(x, R + [term], z) for z in nfa.transitions.get(x, {}).get(term,     [])])
                        newItems.extend([(x, R + [term], z) for z in nfa.transitions.get(x, {}).get(WILDCARD, [])])
                    items = newItems
            for (p, R, q) in items:
                ret.addProduction(getNterm(p, lhs, q), R)
    return ret


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

    from levenshtein import levenshtein_automata
    lev = levenshtein_automata([Num(), '+', '*', Num()], 1)

    gram.convertToCNF(allow_recursive_start = True,
        allow_mixed_terms = True,
        allow_epsilon_rules = True,
        allow_unit_rules = True)

    inter = intersect(gram, lev)
    print(inter)
    print(inter.findMember())
