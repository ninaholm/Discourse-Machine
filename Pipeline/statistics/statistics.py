# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import matplotlib
import sys




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
		plt.bar(j, bowscores[i], color="red")
		plt.bar(j+1, parscores[i], color="blue")


	# Set baseline
	plt.plot([0,80], [norm_bow_baseline, norm_bow_baseline], color="red") # bow random baseline
	plt.plot([0,80], [norm_par_baseline, norm_par_baseline], color="blue") # parser random baseline

	# Labels and graphics
	LABELS = []
	for name in allnames:
		LABELS.append(""); LABELS.append(name); LABELS.append("")
	plt.xticks(range(len(allnames)*3), LABELS, rotation='vertical')
	plt.subplots_adjust(bottom=0.35)
	plt.margins(0.01)
	plt.ylim([0,1.2])

	plt.show()







def plot_innermost_iterations():

	statistics = []
	with open('innermost_iterations.csv', 'r') as myfile:
		wr = csv.reader(myfile, quoting=csv.QUOTE_ALL)
		for row in wr:
			statistics.append(row)


	# Graph: Plot the innermost iterations
	x = [int(x[0]) for x in statistics]
	y = [int(y[1]) for y in statistics]
	z = [(int(z[0])**3)*18548 for z in statistics] # Running time of grammar loop solution
	w = [(int(w[0])**3)*11065**2 for w in statistics] # Worst case for our solution

	handle_1 = plt.scatter(x, y, color="blue", label='Cross-product', s=2)
	handle_2 = plt.scatter(x, z, color="red", label='Grammar Loop', s=2)
	handle_3 = plt.scatter(x, w, color="green", label='Worst case cross-product', s=2)
	plt.legend(handles=[handle_3, handle_2, handle_1])
	plt.title('No. of iterations for innermost loop')
	plt.ylabel('No. of iterations')
	plt.xlabel('Length of sentence')
	plt.yscale('log')
	plt.show()





# Graph: Plot the actual runtime based on the timecounters
def plot_runtime():

	statistics = []
	with open('runtime_statistics.csv', 'r') as myfile:
		wr = csv.reader(myfile, quoting=csv.QUOTE_ALL)
		for row in wr:
			statistics.append(row)


	x = [x[0] for x in statistics]
	y = [y[1] for y in statistics]
	z = [z[2] for z in statistics]

	handle_1 = plt.scatter(x, y, color="blue", label='Cross product', s=2)
	handle_2 = plt.scatter(x, z, color="red", label='Grammar Loop', s=2)
	plt.legend(handles=[handle_2, handle_1])
	plt.title('Actual runtime comparison')
	plt.ylabel('Runtime in microseconds')
	plt.xlabel('Length of sentence')
	# plt.yscale('log')
	plt.show()







