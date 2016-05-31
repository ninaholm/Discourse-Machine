# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import matplotlib
import sys
import scipy
import numpy as np
from scipy import stats
import random
import pickle




def output_graph():

	print "BOW baseline:", (0.71 + 0.86 + 0.079 + 0.55 + 0.565 + 0.538 + 0.413 + -0.3 + 0.202 + 1.219 + 0.641 + 0.643 + 0.64 + 0.365 + 0.526 + 0.125 + 0.206 + 0.083 + 0.595 + 0.441 + 0.754 + 0.5 + 1.235 + 0.716 + 0.238 + -1.054 + 0.585 + 0.125 + 0.542 + 0.95) / 30

	statistics = [
	["DF", {"dansk folkeparti": [0.318, 0.0278171], "pia kjærsgård": [0.347, 0.0357288], "kristian thules": [0.787, 0.0303447]}],
	["Konservative", {"konservativ": [0.407, 0.0176835], "bende bendts": [0.333, 0.0115459], "søren pape": [0.565, 0.0505051]}],
	["Liberal Alliance", {"liberal alliance": [0.607, 0.0631338], "joachim b. olse": [0.381, 0.0654762], "ande samuelse": [0.75, 0.0812358]}],
	["Venstre", {"venstre": [0.49, 0.0431016], "ing støjberg": [0.337, -0.0153469], "lar løkke": [0.469, 0.0265518]}],
	["Radikale", {"radikal venstre": [0.56, 0.0280794], "margrethe vestage": [0.574, 0.0255854], "mort østergaard": [0.545, 0.0118056]}],
	["Socialdemokraterne", {"socialdemokrat": [0.471, 0.0344828], "helle thorning": [0.703, -0.0122129], "mette frederiks": [0.583, 0.043111]}],
	["Alternativet", {"alternativ": [0.515, 0.0449795], "uffe elbæk": [0.636, 0.0369808], "josephine fock": [0, 0]}],
	["SF", {"sf": [0.471, 0.0237825], "villy søvndal": [0.37, 0.00669193], "pia olse dyhr": [0.519, 0.0954885]}],
	["Enhedslisten", {"enhedsliste": [0.421, 0.0312822], "johanne schmidt-nielse": [0.363, -0.00843709], "frank aa": [0.702, 0.0260696]}]
	]

	allnames = []
	for lst in [p[1] for p in statistics]:
		for name in lst:
			allnames.append(name.decode('utf-8'))

	bowscores = []
	parscores = []
	for lst in [p[1] for p in statistics]:
		for name in lst:
			bowscores.append(lst[name][0])
			parscores.append(lst[name][1])

	#Normalize values
	# normalized = (x-min(x))/(max(x)-min(x))
	tmp = []
	for value in bowscores:
		nv = (value - min(bowscores)) / (max(bowscores) - min(bowscores))
		tmp.append(nv)
	norm_bow_baseline = (0.4564 - min(bowscores)) / (max(bowscores) - min(bowscores))
	bowscores = tmp
	tmp = []
	for value in parscores:
		nv = (value - min(parscores)) / (max(parscores) - min(parscores))
		tmp.append(nv)
	norm_par_baseline = (0.028 - min(parscores)) / (max(parscores) - min(parscores))
	parscores = tmp

	# Plot all values
	for j in range(0, len(allnames)*3, 3):
		i = j/3
		handle_1 = plt.bar(j, bowscores[i], color="red", label="BOW scores")
		handle_2 = plt.bar(j+1, parscores[i], color="blue", label="parse scores")


	# Set baseline
	handle_3 = plt.plot([0,80], [norm_bow_baseline, norm_bow_baseline], color="red", label="BOW baseline") # bow random baseline
	handle_4 = plt.plot([0,80], [norm_par_baseline, norm_par_baseline], color="blue", label="parse baseline") # parser random baseline

	# Labels and graphics
	LABELS = []
	for name in allnames:
		LABELS.append(""); LABELS.append(name); LABELS.append("")
	plt.xticks(range(len(allnames)*3), LABELS, rotation='vertical')
	plt.subplots_adjust(bottom=0.35)
	plt.legend(handles=[handle_2, handle_1])
	plt.margins(0.01)
	plt.ylim([0,1.2])
	plt.gca().invert_xaxis()

	plt.show()






def plot_innermost_iterations():

	statistics = []
	with open('innermost_iterations.csv', 'r') as myfile:
		wr = csv.reader(myfile, quoting=csv.QUOTE_ALL)
		for row in wr:
			statistics.append(row)

	print "Number of sentences parsed:", len(statistics)

	# Graph: Plot the innermost iterations
	x = [int(x[0]) for x in statistics]
	y = [int(y[1]) for y in statistics]
	# z = [(int(z[0])**3)*18548 for z in statistics] # Running time of grammar loop solution
	# w = [(int(w[0])**3)*11065**2 for w in statistics] # Worst case for our solution

	handle_1 = plt.scatter(x, y, color="blue", label='Cross-product', s=2)
	# handle_2 = plt.scatter(x, z, color="red", label='Grammar Loop', s=2)
	# handle_3 = plt.scatter(x, w, color="green", label='Worst case cross-product', s=2)
	# plt.legend(handles=[handle_3, handle_2, handle_1])
	plt.title('No. of iterations of innermost loop')
	plt.ylabel('No. of iterations (logscaled)')
	plt.xlabel('Length of sentence')
	# plt.ylim([0,1000000])
	# plt.yscale('log')
	plt.show()

# plot_innermost_iterations()



# Graph: Plot the actual runtime based on the timecounters
def plot_runtime():

	statistics = []
	with open('runtime_statistics.csv', 'r') as myfile:
		wr = csv.reader(myfile, quoting=csv.QUOTE_ALL)
		for row in wr:
			statistics.append(row)

	print "Statistics:", len(statistics)
	x = [float(x[0]) for x in statistics]
	y = [float(y[1]) for y in statistics]
	z = [float(z[2]) for z in statistics]

	handle_1 = plt.scatter(x, y, color="blue", label='Cross product', s=2)
	handle_2 = plt.scatter(x, z, color="red", label='Grammar Loop', s=2)
	plt.legend(handles=[handle_2, handle_1])
	plt.title('Actual runtime comparison')
	plt.ylabel('Runtime in seconds (logscaled)')
	plt.xlabel('Length of sentence')
	plt.yscale('log')
	plt.ylim([0.0001, 10000]) # Show ratio!
	plt.show()



# plot_runtime()




def testing_baseline():
	
	statistics = [
	["DF", {"dansk folkeparti": [0.318, 0.0278171], "pia kjærsgård": [0.347, 0.0357288], "kristian thules": [0.787, 0.0303447]}],
	["Konservative", {"konservativ": [0.407, 0.0176835], "bende bendts": [0.333, 0.0115459], "søren pape": [0.565, 0.0505051]}],
	["Liberal Alliance", {"liberal alliance": [0.607, 0.0631338], "joachim b. olse": [0.381, 0.0654762], "ande samuelse": [0.75, 0.0812358]}],
	["Venstre", {"venstre": [0.49, 0.0431016], "ing støjberg": [0.337, -0.0153469], "lar løkke": [0.469, 0.0265518]}],
	["Radikale", {"radikal venstre": [0.56, 0.0280794], "margrethe vestage": [0.574, 0.0255854], "mort østergaard": [0.545, 0.0118056]}],
	["Socialdemokraterne", {"socialdemokrat": [0.471, 0.0344828], "helle thorning": [0.703, -0.0122129], "mette frederiks": [0.583, 0.043111]}],
	["Alternativet", {"alternativ": [0.515, 0.0449795], "uffe elbæk": [0.636, 0.0369808], "josephine fock": [0, 0]}],
	["SF", {"sf": [0.471, 0.0237825], "villy søvndal": [0.37, 0.00669193], "pia olse dyhr": [0.519, 0.0954885]}],
	["Enhedslisten", {"enhedsliste": [0.421, 0.0312822], "johanne schmidt-nielse": [0.363, -0.00843709], "frank aa": [0.702, 0.0260696]}]
	]

	par_baseline = [-0.0588235294118, -0.25, 0.0714285714286, 0.0769230769231, -0.00512820512821, 0.0215277777778, 0, -0.24863803189, 0, 0.102786663153, 0, -0.0106889204545, 0, 0.149741435036, -0.0194996843434, -0.0438492063492, -0.00171130952381, 0.00882005045608, 0, 0.0835082962381, 0.1, -0.0556807056704, 0, 0.170454545455, -0.00982142857143, 0, 0, 0.0598108037604, 0, 0.028413925201, 0, 0.00274725274725, -0.142857142857, 0, 0.125, 0.142857142857, 0.0347222222222, 0.125, 0, -0.1, 0.0674305555556, 0, 0.118520021645, 0.166666666667, 0, 0.0249053030303, 0.111111111111, 0, 0, -0.0238095238095, 0.0358455882353, 0, 0, 0, 0, 0, 0, 0, -0.0512351288357, 0, 0, 0, -0.0341247750787, 0, -0.0380952380952, 0, 0, -0.0178979864492, -0.00172514436646, 0, 0.25, 0.151315789474, 0, 0, -0.0499188311688, -0.0115384615385, 0, -0.0268060393608, 0, 0.0588235294118, 0, 0.0266560120907, -0.0309027777778, 0.125, 0, -0.0320596359659, -0.00321307417783, 0, 0, -0.0276879370629, -0.236111111111, 0.0346878232058, 0, -0.173214285714, 0.104761904762, 0, 0.0666666666667, -0.166666666667, 0.1, -0.0687421679198, 0.05, 0.0909090909091, 0, 0.0833333333333, 0.2, 0, -0.0833333333333, 0.113305322129, 0.0885015451557, -0.166666666667, -0.0240384615385, 0.103335813492, 0, 0.091958041958, 0, 0.25, 0, 0.05, 0.141666666667, 0, 0.233766233766, 0.0977443609023, 0, 0, 0.0555555555556, 0, -0.111111111111, 0, 0, -0.0525568181818, -0.125, 0, 0, 0, 0, 0.0651017731479, 0.0226925236847, 0.0662878787879, 0.0833333333333, 0.230693695788, 0.11667284719, 0.00338985193143, 0, -0.000930812026022, 0, 0.0787037037037, 0.00941461962767, 0, 0.0681684680451, 0, 0.168297847985, 0, 0.0833333333333, 0.0363771645022, 0, 0.0669637989244, -0.1, 0.14683596263, 0.125, 0.0611111111111, 0.0937049062049, -0.125, 0.071875, 0.0625, 0, 0.111111111111, 0.0374203170971, 0.0321557971014, -0.125, 0.142857142857, 0.0625, 0, 0.0491010030695, -0.00804195804196, 0, 0.0645833333333, 0.113495454253, 0.165133477633, 0, 0, 0, -0.0180555555556, 0, 0.122253787879, -0.0151723276723, 0.0650793650794, 0.0714285714286, 0, 0, 0, 0.1, -0.125, 0, -0.0228472222222, 0.122394220846, 0.0958333333333, -0.0659226190476, 0, 0]

	bow_baseline = [0.333, 0.385, 2.0, 1.167, 0.5, 0.429, -0.75, 0.104, 0, 1.179, 0, 0.419, 0.8, 0.438, 0.718, 0.313, 0.136, 0.35, -1.0, 0.772, 0.556, 0.929, 0, 1.0, 0.4, 0.875, 0.286, 0.326, -0.667, 0.482, 0, 1.25, -1.0, 0, -0.5, 1.0, 0.25, 1.875, 0, 0.667, 0.905, 0, 0.025, 0.0, 1.222, 0.591, 1.0, 1.0, -1.0, 0.611, 0.333, 1.5, -0.75, 1.0, 1.5, 0, 0, -1.0, 0.53, 0, 1.0, -0.6, 0.625, 1.2, 0.5, 0, 1.0, 0.423, 0.308, 0.7, 0.833, 0.643, 0, 1.111, 1.163, 0.625, 1.0, 0.561, 0, 0.333, 0.667, 0.44, -0.15, 1.0, 1.0, 0.655, 0.625, 1.0, 0.333, 0.682, 0.053, 0.545, -0.333, -1.0, 0.556, 1.0, 0.727, 0.143, 1.0, 0.326, 1.0, 0.833, 0, 0.5, 0.8, 0, 0.435, 0.625, 0.67, 0.143, 0.5, 0.273, 0, 0.667, 0, 1.0, 0, 0.467, 0.714, 0.333, 0.667, 1.0, 1.143, 0, 0.095, 0, 0.0, 0, 0, -0.4, -1.0, 0.333, 0, 0.2, 0, 0.361, 0.466, 0.0, 0.632, 1.239, 0.364, -0.837, 0, 0.397, 1.0, 0.5, 0.614, -1.0, 0.0, 0, 0.067, 0, 0.923, 0.622, 0, 0.612, -0.333, 0.8, 0.5, 1.0, 1.032, 0.545, 0.1, -0.333, 0, -0.818, 0.412, 0.583, -1.1, 0.143, 1.0, 0.333, 0.582, 0.917, 0.0, 0.667, 0.435, 1.0, 0, 0, 0, 0.89, 0, 0.658, 1.022, 0.9, 1.0, 1.0, 0.25, 0.0, 0.0, 0.45, 0, 0.267, 0.333, 0.167, 0.143, 2.0, 1.444]

	# Get p-values on a party basis
	pvalues = []
	for i in range(len(statistics)):
		party_name = statistics[i][0]
		bowscores = [statistics[i][1][x][0] for x in statistics[i][1].keys()]
		parscores = [statistics[i][1][x][1] for x in statistics[i][1].keys()]
		rand_pt = [stats.ttest_ind(parscores, [random.uniform(1, -1) for i in range(len(parscores))], axis=0, equal_var=True) for j in range(1000)]
		rand_pt = sum([x.pvalue for x in rand_pt]) / len(rand_pt)
		rand_bt = [stats.ttest_ind(bowscores, [random.uniform(1, -1) for i in range(len(bowscores))], axis=0, equal_var=True) for j in range(1000)]
		rand_bt = sum([x.pvalue for x in rand_bt]) / len(rand_bt)
		pt = stats.ttest_ind(parscores, par_baseline, axis=0, equal_var=True)
		bt = stats.ttest_ind(bowscores, bow_baseline, axis=0, equal_var=True)
		print party_name + ": ", bt.pvalue, "|", pt.pvalue, "|\nBOW: ", rand_bt, "\nParse: ", rand_pt
		pvalues.append([party_name, pt.pvalue, bt.pvalue])

	# Get p-values on a (blue) block basis
	bow_pvalues = []
	par_pvalues = []
	# for i in range(4): # Right-leaning statistics	
	for i in range(4, len(statistics)): # Left-leaning statistics
		bowscores = [statistics[i][1][x][0] for x in statistics[i][1].keys()]
		parscores = [statistics[i][1][x][1] for x in statistics[i][1].keys()]
		rand_pt = [stats.ttest_ind(parscores, [random.uniform(1, -1) for i in range(len(parscores))], axis=0, equal_var=True) for j in range(1000)]
		rand_pt = sum([x.pvalue for x in rand_pt]) / len(rand_pt)
		rand_bt = [stats.ttest_ind(bowscores, [random.uniform(1, -1) for i in range(len(bowscores))], axis=0, equal_var=True) for j in range(1000)]
		rand_bt = sum([x.pvalue for x in rand_bt]) / len(rand_bt)		
		pt = stats.ttest_ind(parscores, par_baseline, axis=0, equal_var=True)
		bt = stats.ttest_ind(bowscores, bow_baseline, axis=0, equal_var=True)
		bow_pvalues.append(bt.pvalue)
		par_pvalues.append(pt.pvalue)
	print "Right-leaning:", (sum(bow_pvalues) / len(bow_pvalues)), "|", (sum(par_pvalues) / len(par_pvalues)), "|\nBOW: ", rand_bt, "\nParse: ", rand_pt








def sentence_analysis():
	statistics = []
	with open('sentences_output', 'r') as myfile:
		for row in myfile:
			statistics.append(row.strip("\n").split("|")[1:])


	# Remove scores from unparsed sentences
	tmp = []
	for i in range(len(statistics)):
		if float(statistics[i][0]) != 0:
			tmp.append(statistics[i])
	statistics = tmp


	# Plot the rest
	x = [float(x[0]) for x in statistics] # parse score
	y = [float(y[1]) for y in statistics] # annotated score
	plt.scatter(y,x)
	fit = np.polyfit(y, x, 1)
	plt.plot(y, (fit[0] * (y + fit[1])), color='red')
	plt.title("Correlation between parse scores and \nmanually annotated sentiment scores")
	plt.ylabel('Parse score')
	plt.xlabel('Annotated score')
	# plt.show()

	print "Average annotated score:", sum(y) / len(y)
	print "Average parse score:", sum(x) / len(x)

	# Make t-test
	rand = [random.uniform(1, -1) for i in range(len(x))]
	print "Min:", min(x)
	print "Max:", max(x)

	pvalues = []
	for i in range(1000):
		t = stats.ttest_ind(y, [random.choice([1, 0.5, 0, -0.5, -1]) for i in range(len(x))], axis=0, equal_var=True)
		# t = stats.ttest_ind(y, [random.uniform(1, -1) for i in range(len(x))], axis=0, equal_var=True)
		pvalues.append(t.pvalue)
	
#	t = stats.ttest_ind(x, rand, axis=0, equal_var=True)
	print "Average p-value:", sum(pvalues) / len(pvalues)




def information_dates():
	statistics = []
	with open('information_dates_data.csv', 'r') as myfile:
		wr = csv.reader(myfile, quoting=csv.QUOTE_ALL)
		for row in wr:
			statistics.append(row)

	new_statistics = [[int(z[0][:4]), z[1]] for z in statistics]
	print statistics

	x = list(set([z[0] for z in new_statistics]))
	x.sort()

	tmp = {}
	for i in range(len(new_statistics)):
		if new_statistics[i][0] in tmp:
			tmp[new_statistics[i][0]] += int(new_statistics[i][1])
		else:
			tmp[new_statistics[i][0]] = int(new_statistics[i][1])

	y = [tmp[z] for z in x]


	plt.bar(x,y, color="blue", linewidth=0)
	plt.ylabel('No. of articles')
	plt.xlabel('Year')
	plt.title("'Information' articles by year")
	plt.show()




def parser_accuracy_analysis():
	unparsed_sentences = []
	parsed_sentences = []

	with open("unparsed_sentences_LARGE", "r") as file:
		unparsed_sentences = pickle.load(file)


	with open("parsed_sentences_LARGE", "r") as file:
		parsed_sentences = pickle.load(file)

	un_tags = []
	un_words = []
	for sentence in unparsed_sentences:
		for word in sentence:
			un_words.append(word[0].decode('utf-8', errors='ignore'))
			un_tags.append(word[1].decode('utf-8', errors='ignore'))

	par_tags = []
	par_words = []
	for sentence in parsed_sentences:
		for word in sentence:
			par_words.append(word[0].decode('utf-8', errors='ignore'))
			par_tags.append(word[1].decode('utf-8', errors='ignore'))


	citation_marks = [u"«", u"»", "\""]
	un_cit = 0
	for s in unparsed_sentences:
		cit_found = False
		for word in s:
			if word[0].decode('utf-8', 'ignore') in citation_marks:
				cit_found = True
		if cit_found: un_cit += 1

	par_cit = 0
	for s in parsed_sentences:
		cit_found = False
		for word in s:
			if word[0].decode('utf-8', 'ignore') in citation_marks:
				cit_found = True
		if cit_found: par_cit += 1

	print "Sentences parsed:", len(parsed_sentences)
	print "Sentences not parsed:", len(unparsed_sentences)

	print "Percentage of sentences with a quote:", ((un_cit+par_cit)*100/(len(unparsed_sentences+parsed_sentences)))
	

	print "Percentage of citations in unparsed sentences:", (un_cit*100/(len(unparsed_sentences))), "%"
	print "Percentage of citations tag in parsed sentences:", (par_cit*100/(len(parsed_sentences))), "%"

	all_tags = []
	unique_un_tags = {}
	for i in range(len(un_tags)):
		all_tags.append(un_tags[i])
		if un_tags[i] in unique_un_tags:
			unique_un_tags[un_tags[i]] += 1
		else:
			unique_un_tags[un_tags[i]] = 1

	unique_par_tags = {}
	for i in range(len(par_tags)):
		all_tags.append(par_tags[i])
		if par_tags[i] in unique_par_tags:
			unique_par_tags[par_tags[i]] += 1
		else:
			unique_par_tags[par_tags[i]] = 1

	all_tags = list(set(all_tags))

	# Unparsed tags
	x = [all_tags.index(i) for i in unique_un_tags.keys()]
	y = unique_un_tags.values()
	unparsed_handle = plt.bar(x, y, align='center', color="blue", label="Unparsed sentences")

	# Parsed tags
	x = [all_tags.index(i) for i in unique_par_tags.keys()]
	y = unique_par_tags.values()
	parsed_handle = plt.bar(x, y, align='center', color="red", label="Successfully parsed sentences")

	# Design and plotting
	plt.subplots_adjust(bottom=0.35)
	plt.xticks(range(len(all_tags)), all_tags, rotation='vertical')
	plt.legend(handles=[parsed_handle, unparsed_handle])
	plt.xlim([-1,len(all_tags)])
	plt.title("Distribution of tags")
	# plt.show()

	plt.clf()
	tmp = {}
	for s in unparsed_sentences:
		if len(s) in tmp: tmp[len(s)] += 1
		else: tmp[len(s)] = 1

	tmp2 = {}
	for s in parsed_sentences:
		if len(s) in tmp2: tmp2[len(s)] += 1
		else: tmp2[len(s)] = 1

	# portion*100/total
	percentages = []
	x = []
	for n in tmp:
		if n in tmp2:
			x.append(n)
			percentages.append(tmp[n]*100/(tmp[n]+tmp2[n]))

	# plt.scatter(tmp.keys(), tmp.values(), color="blue")
	# plt.scatter(tmp2.keys(), tmp2.values(), color="red")
	plt.scatter(x, percentages, color="blue", linewidth=0)
	plt.xlabel("Length of sentence")
	plt.ylabel("% unparsable")

	plt.show()


parser_accuracy_analysis()

