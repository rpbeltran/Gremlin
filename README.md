
# GREMLIN

Levenshtein optimal interpretation of context free grammars for robust semantic analysis

## What is GREMLIN

Gremlin is a big sloppy algorithm. Messy with math its very premise carries a promise of vernacular slosh, as sloshing with promise its very premise carries with it the mess of the murky math it makes away with.

Gremlin is a language tool... mostly, but also the hero nobody asked for, as it continuously questioning the answers that have long puzzled society.

## But really, what is GREMLIN?

Gremlin is an algorithm that identifies the ideal reinterpretation of token strings under constraint. The output of Gremlin is immediately useful as an intelligent debugger for arbitrary programming languages. Capable of reading YACC grammar definitions and buggy programs, Gremlin can actually tell you how to fix a program without any additional guidance. 

Gremlin can also be used to solve challenging tasks in Natural Language Processing by realigning language to its model. CFGs are commonly used for domain-specific NLP tasks but often lack in robustness. Gremlin provides adaptable antifragility to this class of semantic analysis without interfering with the simplicity that makes it desirable.

We also strongly hypothesise that Gremlin may be a suitable metric for machine learning topologies for languages against a corpus. An example application for this use case would include deriving domain-specific language models from a data set of relevant materials.

The name Gremlin is made by compacting two major and relevant jargons: Grammar-Levenshtein.... loosely.

## But what is it actually doing

Gremlin actually does a few distinct doings; I guess that's why they say little things come in lots of packages.

At its heart though, Gremlin computes the nearest interpretation of a sequence of tokens in order to force alignment with a Context Free Grammar, as measured by the Levenshtein distance of the interpretation from its source. The theory behind this action is heavily rooted in Formal Language and Automata Theory. More specifically, we use the input tokens to generate nondeterministic Levenshtein Automatas, computes their intersection with a Context Free Grammar, and look for hits.

## And what parting words have thee to thine reader?

A Nondeterministic Finite Automata and a Context Free Grammar powered a search problem as the crux of a language-matching application, and yet we never actually found the need for a match() function in either class. 

