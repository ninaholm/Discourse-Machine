from Grammar import *

# Takes a raw grammar (based on the DDT extraction) and makes it binary (CNF) and normalizes it's counts into our probabilities.

def convert_to_probabilistic_chomsky(rawgrammar):

	sumOcc = sum(rawgrammar.rules.values())
	print "SUMOCC:", sumOcc
	grammar = Grammar()
	leftsideOcc = {}

	for x in rawgrammar.rules:
		if x.rule_head in leftsideOcc:
			leftsideOcc[x.rule_head] += 1
		else:
			leftsideOcc[x.rule_head] = 1
	
	for x in rawgrammar.rules:
		x.prob = float(rawgrammar.rules[x]) / leftsideOcc[x.rule_head]
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
		# print x.rule_head, " ---> \t", x.constituents, x.prob 
		# printd
		grammar.newRuleCount += 1
		if x.key() in grammar.rules:
			grammar.rules[x.key()].append(x)
		else:
			grammar.rules[x.key()] = [x]
		# if len(gramcd .

	return grammar

def compress(cnfgrammar):
	startcount = 0
	endcount = 0 
	delKeys = []
	newRules = []
	print len(cnfgrammar.rules)

	for ids in cnfgrammar.rules:
		delList = []
		startcount += len(cnfgrammar.rules[ids])
		# print cnfgrammar.rules[ids]
		if len(cnfgrammar.rules[ids]) > 1:
			noMainRule = True
			mainrule = None
			# print "ID: ", ids
			for rule in cnfgrammar.rules[ids]:
				print "RULE2:",rule.print_rule()
				# print len(cnfgrammar.rules[ids])
				if rule.prob == 1:
					# print "RULE: ", rule.print_rule()
				 	if noMainRule == True:
						mainrule = rule
						noMainRule = False
						continue
					for key in cnfgrammar.rules:
						if key.endswith(rule.rule_head):
							ruleChange = cnfgrammar.rules[key][0]
							# print "PRE: ", ruleChange.print_rule()
							ruleChange.constituents[1] = mainrule.rule_head
							newRules.append([ruleChange])
							delKeys.append(key)
							delList.append(rule.rule_head)
							# print "POST: ", ruleChange.print_rule()
							break
					# cnfgrammar.rules[ids].remove(rule)
					
			# print ">>>>>>>>MAINRULE: ", mainrule.print_rule(), "\n"

			newList = []
			# print "PRESIZE: ", len(cnfgrammar.rules[ids])		
			for x in cnfgrammar.rules[ids]:
				if x.rule_head not in delList:
					newList.append(x)
					# if x.prob == 1:
			# 			print "SURVIVOR: ", x.print_rule()
				# else:
					# if x.prob == 1:
						# print "DELETED: ", x.print_rule()
			# print "POSTSIZE: ", len(newList)
			endcount += len(cnfgrammar.rules[ids]) - len(newList)

			cnfgrammar.rules[ids] = newList		

	endcount = startcount - endcount
	percent = abs((endcount / float(startcount))-1) * 100

	print ">>GRAMMARCREATOR: Rules compressed %s%% (%s to %s)" %(round(percent, 1), startcount, endcount)



	print "Keys up for deletion: ", len(delKeys)
	for x in range(len(delKeys)):
		print "delkey:",delKeys[x]
		print "newrule:",newRules[x][0].print_rule()
		print "Deleting", cnfgrammar.rules[delKeys[x]][0].print_rule()
		print "info: ", len(cnfgrammar.rules[delKeys[x]]), delKeys[x]
		del cnfgrammar.rules[delKeys[x]]
		if newRules[x][0].key() not in cnfgrammar.rules:
			print "Adding: ", newRules[x][0].print_rule()
			cnfgrammar.rules[newRules[x][0].key()] = newRules[x] 
		else:
			print "Exists: ", cnfgrammar.rules[newRules[x][0].key()][0].print_rule()
			print "Denied: ", newRules[x][0].print_rule()
			for y in cnfgrammar.rules[newRules[x][0].key()]:
				print "PRE:",y.print_rule()
			print "TYPE:",type(cnfgrammar.rules[newRules[x][0].key()])
			print "newRules type", type(newRules[x])
			cnfgrammar.rules[newRules[x][0].key()] += (newRules[x])
			for y in cnfgrammar.rules[newRules[x][0].key()]:
				print "POST:",y.print_rule()

		print 
	return cnfgrammar

def convertToTuples(grammar):