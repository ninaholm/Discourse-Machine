import csv
import matplotlib.pyplot as plt
import sys



df = [[0.318, 0.787] [0.0278171, 0.0357288, 0.0303447]]
kon = [[0.407, 0.333, 0.565] [0.0176835, 0.0115459, 0.0505051]]
lib = [[0.607, 0.381, 0.75] [0.0631338, 0.0654762, 0.0812358]]
v = [[0.49, 0.337, 0.469] [0.0431016, -0.0153469, 0.0265518]]


statistics = {
"DF": {"dansk folkeparti": [0.318, 0.0278171], "pia kjærsgård": [None, 0.0357288], "kristian thules": [0.787, 0.0303447]},
"Konservative": {"konservativ": [0.407, 0.0176835], "bende bendts": [0.333, 0.0115459], "søren pape": [0.565, 0.0505051]},
"Liberal Alliance": {"liberal alliance": [0.607, 0.0631338], "joachim b. olse": [0.381, 0.0654762], "ande samuelse": [0.75, 0.0812358]},
"Venstre": {"venstre": [0.49, 0.0431016], "ing støjberg": [0.337, -0.0153469], "lar løkke": [0.469, 0.0265518]},
"Radikale": {"radikal venstre": [0.56, 0.0280794], "margrethe vestage": [0.574, 0.0255854], "mort østergaard": [0.545, 0.0118056]},
"Socialdemokraterne": {"socialdemokrat": [0.471, 0.0344828], "helle thorning": [0.703, -0.0122129], "mette frederiks": [0.583, 0.043111]},
"Alternativet": {"alternativ": [0.515, 0.0449795], "uffe elbæk": [0.636, 0.0369808], "josephine fock": [0, 0]},
"SF": {"sf": [0.471, 0.0237825], "villy søvndal": [0.37, 0.00669193], "pia olse dyhr": [0.519, 0.0954885]},
"Enhedslisten": {"enhedsliste": [0.421, 0.0312822], "johanne schmidt-nielse": [0.363, -0.00843709], "frank aa": [0.702, 0.0260696]},
}












sys.exit()











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





# # Graph: runs through innermost loop
# x = [x[0] for x in statistics] # sentence length
# y = [y[1] for y in statistics] # Empirical counter
# z = [(z[0]**3)*len(parser.grammar.rules) for z in statistics] # Running time of grammar loop solution
# w = [(w[0]**3)*11065**2 for w in statistics] # Worst case for our solution

# handle_1 = plt.scatter(x, y, color="blue", label='Cross product', s=2)
# handle_2, = plt.plot(x, z, "r--", color="red", label='Grammar Loop')
# handle_2.set_antialiased(True)
# #plt.legend(handles=[handle_1, handle_2])
# plt.title('No. of runs through innermost loop')
# plt.ylabel('No. of runs through innermost loop')
# plt.xlabel('Length of sentence')

# plt.axis([-10.0,100.0, -10.0,4000000.0])
# # ax = p.gca()
# # ax.set_autoscale_on(False)

# plt.show()


# sys.exit()




