class GrammarRule(object):
	def __init__(self, rule_head, constituents, prob):
		self.constituents = constituents
		self.rule_head = rule_head
		self.prob = prob

	def print_rule(self):
		s = self.rule_head + " --->"
		for c in self.constituents:
			s = s + " " + c
		return s

	def makeSubRules(self, newRuleCount, count):
		subRules = [""]

		# print ">>",self.rule_head, " ---> \t", self.constituents
		for x in range(1,len(self.constituents)):
			if x == len(self.constituents)-2:
				rule_head = "@X" + str(newRuleCount)
				constituents = [self.constituents[x]]
				constituents.append(self.constituents[x+1])
				# print "NEW RULE: %s --> %s" %(rule_head, constituents)
				tmp = GrammarRule(rule_head, constituents, 1)
				subRules.append(tmp)
				break

			rule_head = "@X" + str(newRuleCount)
			newRuleCount += 1
			constituents = [self.constituents[x]]
			constituents.append("@X" + str(newRuleCount))
			# print "NEW RULE: %s --> %s" %(rule_head, constituents)
			tmp = GrammarRule(rule_head, constituents, 1)
			subRules.append(tmp)

		self.constituents = [self.constituents[0]]
		self.constituents.append(subRules[1].rule_head)
		subRules[0] = self
		# print self.rule_head, " ---> ", self.constituents, self.prob
		# for lol in subRules:
		# 	print lol.rule_head, " ---> \t", lol.constituents, lol.prob
		return subRules

	def key(self):
		key = ""
		for x in self.constituents:
			key += str(x)
		print "KEY: %s" %key
		return key

	def __hash__(self):
		return hash((str(self.constituents)))

	def __repr__(self):
		return (self.rule_head + "-->" + " ".join(self.constituents))

	def __eq__(self, other):
		return (str(self.constituents), self.rule_head) == (str(self.constituents), self.rule_head)

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
			for rule in self.rules[lists]:
				print " ".join(rule.constituents), " <--- \t", rule.rule_head, "\t", rule.prob

	def __getstate__(self): return self.__dict__
	def __setstate__(self, d): self.__dict__.update(d)