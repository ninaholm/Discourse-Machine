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

		# print ">>",self.left_side, " ---> \t", self.constituents
		for x in range(1,len(self.constituents)):
			if x == len(self.constituents)-2:
				left_side = "@X" + str(newRuleCount)
				constituents = [self.constituents[x]]
				constituents.append(self.constituents[x+1])
				# print "NEW RULE: %s --> %s" %(left_side, constituents)
				tmp = GrammarRule(left_side, constituents, 1)
				subRules.append(tmp)
				break

			left_side = "@X" + str(newRuleCount)
			newRuleCount += 1
			constituents = [self.constituents[x]]
			constituents.append("@X" + str(newRuleCount))
			# print "NEW RULE: %s --> %s" %(left_side, constituents)
			tmp = GrammarRule(left_side, constituents, 1)
			subRules.append(tmp)

		self.constituents = [self.constituents[0]]
		self.constituents.append(subRules[1].left_side)
		subRules[0] = self
		# print self.left_side, " ---> ", self.constituents, self.prob
		# for lol in subRules:
		# 	print lol.left_side, " ---> \t", lol.constituents, lol.prob
		return subRules

	def key(self):
		key = ""
		for x in self.constituents:
			key += str(x)
		print "KEY: %s" %key
		return key

	def __hash__(self):
		return hash((str(self.constituents)))

	def __eq__(self, other):
		return (str(self.constituents), self.left_side) == (str(self.constituents), self.left_side)

	def __name__(self):
		return self.key

	def __getstate__(self): return self.__dict__
	def __setstate__(self, d): self.__dict__.update(d)


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
		for lists in self.rules:
			print type(lists)
			for rule in self.rules[lists]:
				print rule.constituents, " <--- \t", rule.left_side, "\t", rule.prob

	def __getstate__(self): return self.__dict__
	def __setstate__(self, d): self.__dict__.update(d)