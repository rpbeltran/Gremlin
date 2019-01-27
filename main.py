from lib.levenshtein import levenshtein_automata
from lib.algorithms import intersect
from lib.nfa import NFA
from lib.cfg import CFG

def main(grammarFile, testString):
    cfg = CFG() # TODO
    cfg.convertToCNF(allow_recursive_start = True,
        allow_mixed_terms = True,
        allow_epsilon_rules = True,
        allow_unit_rules = True)
    if cfg.findMember() == None:
        return None
    def runTest(k):
        lev = levenshtein_automota(testString, k)
        return intersect(cfg, lev).findMember()


    if runTest(0) != None:
        return testString

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
    return maxMatch
