import pickle

class GrammarRule(object):
	def __init__(self, left_side, constituents, prob):
		self.constituents = constituents
		self.left_side = left_side
		self.prob = prob

	def print_rule(self):
		s = self.left_side + " --->"
		for c in self.constituents:
			s = s + " " + c
		return s

	def makeSubRules(self, newRuleCount, count):
		subRules = [""]

		print ">>",self.left_side, " ---> \t", self.constituents
		for x in range(1,len(self.constituents)):
			if x == len(self.constituents)-2:
				left_side = "@X" + str(newRuleCount)
				constituents = [self.constituents[x]]
				constituents.append(self.constituents[x+1])
				# print "NEW RULE: %s --> %s" %(left_side, constituents)
				subRules.append(GrammarRule(left_side, constituents, 1))
				break

			left_side = "@X" + str(newRuleCount)
			newRuleCount += 1
			constituents = [self.constituents[x]]
			constituents.append("@X" + str(newRuleCount))
			# print "NEW RULE: %s --> %s" %(left_side, constituents)
			subRules.append(GrammarRule(left_side, constituents, 1))

		self.constituents = [self.constituents[0]]
		self.constituents.append(subRules[1].left_side)
		subRules[0] = self
		# print self.left_side, " ---> ", self.constituents, self.prob
		for lol in subRules:
			# if len(lol.left_side) > 2:
			# 	print lol.left_side, " ---> \t", lol.constituents, lol.prob
			# else:
			print lol.left_side, " ---> \t", lol.constituents, lol.prob
		return subRules

	def __hash__(self):
		return hash((str(self.constituents), self.left_side))

	def __eq__(self, other):
		return (str(self.constituents), self.left_side) == (str(self.constituents), self.left_side)


class Grammar(object):
	def __init__(self):
		self.rules = {}
		self.newRuleCount = 0

	def count_rule(self, gr):
		if gr in self.rules:
			self.rules[gr] = self.rules[gr] + 1
		else:
			self.rules[gr] = 1

	def print_grammar(self):
		for rule in self.rules:
			print rule.print_rule(), " \t", self.rules[rule]




inputfile = open("grammar.in", 'rb')

rawgrammar = pickle.load(inputfile)
sumOcc = sum(rawgrammar.rules.values())

grammar = Grammar()

for x in rawgrammar.rules:

	x.prob = float(rawgrammar.rules[x]) / sumOcc
	# print "%s = %s / %s" %(x.prob, rawgrammar.rules[x], sumOcc)
	if len(x.constituents) > 2:
		subRules = x.makeSubRules(grammar.newRuleCount, rawgrammar.rules[x])
		for rule in subRules:
			# print rule.left_side
			grammar.rules[rule] = rule
		print 
		grammar.newRuleCount += len(subRules)
		continue
	print x.left_side, " ---> \t", x.constituents, x.prob 
	print
	grammar.newRuleCount += 1
	grammar.rules[x] = x


