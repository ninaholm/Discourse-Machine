import pickle
from Grammar import *

def compress(cnfgrammar):
	startcount = 0
	endcount = 0 
	delKeys = []
	newRules = []
	# print len(cnfgrammar.rules)

	for ids in cnfgrammar.rules:
		delList = []
		startcount += len(cnfgrammar.rules[ids])
		if len(cnfgrammar.rules[ids]) > 1:
			noMainRule = True
			mainrule = None
			# print "ID: ", ids
			for rule in cnfgrammar.rules[ids]:
				# print len(cnfgrammar.rules[ids])
				if rule.prob == 1:
					# print "RULE: ", rule.print_rule()
				 	if noMainRule == True:
						mainrule = rule
						noMainRule = False
						continue
					for key in cnfgrammar.rules:
						if key.endswith(rule.left_side):
							ruleChange = cnfgrammar.rules[key][0]
							# print "PRE: ", ruleChange.print_rule()
							ruleChange.constituents[1] = mainrule.left_side
							newRules.append([ruleChange])
							delKeys.append(key)
							delList.append(rule.left_side)
							# print "POST: ", ruleChange.print_rule()
							break
					# cnfgrammar.rules[ids].remove(rule)
					
			# print ">>>>>>>>MAINRULE: ", mainrule.print_rule(), "\n"

			newList = []
			# print "PRESIZE: ", len(cnfgrammar.rules[ids])		
			for x in cnfgrammar.rules[ids]:
				if x.left_side not in delList:
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



	# print "Keys up for deletion: ", len(delKeys)
	for x in range(len(delKeys)):
		# print "Deleting", cnfgrammar.rules[delKeys[x]][0].print_rule()
		# print "info: ", len(cnfgrammar.rules[delKeys[x]]), delKeys[x]
		del cnfgrammar.rules[delKeys[x]]
		if newRules[x][0].key() not in cnfgrammar.rules:
			# print "Adding: ", newRules[x][0].print_rule()
			cnfgrammar.rules[newRules[x][0].key()] = newRules[x] 
		# else:
		# 	print "Exists: ", cnfgrammar.rules[newRules[x][0].key()][0].print_rule()
		# 	print "Denied: ", newRules[x][0].print_rule()

		# print 



with open("grammar.out", 'rb') as inputfile:
	cnfgrammar = pickle.load(inputfile)

compress(cnfgrammar)