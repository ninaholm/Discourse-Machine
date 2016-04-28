from Grammar import *
import pickle

# Takes a raw grammar (based on the DDT extraction) and makes it binary (CNF) and normalizes it's counts into our probabilities.

inputfile = open("rawgrammar.in", 'rb')

rawgrammar = pickle.load(inputfile)
sumOcc = sum(rawgrammar.rules.values())

grammar = Grammar()

for x in rawgrammar.rules:

	x.prob = float(rawgrammar.rules[x]) / sumOcc
	# print "%s = %s / %s" %(x.prob, rawgrammar.rules[x], sumOcc)
	if len(x.constituents) > 2:
		subRules = x.makeSubRules(grammar.newRuleCount, rawgrammar.rules[x])
		for rule in subRules:
			if rule.key() in grammar.rules:
				grammar.rules[rule.key()].append(rule)
			else:
				grammar.rules[rule.key()] = [rule]
		# print 
		grammar.newRuleCount += len(subRules)
		continue
	# print x.left_side, " ---> \t", x.constituents, x.prob 
	# print
	grammar.newRuleCount += 1
	if x.key() in grammar.rules:
		grammar.rules[x.key()].append(x)
	else:
		grammar.rules[x.key()] = [x]

# grammar.print_grammar()

outputfile = open("grammar.in", 'wb')
pickle.dump(grammar, outputfile)
outputfile.close()