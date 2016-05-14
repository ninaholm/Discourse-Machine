import time

def testing(self):
	try:
		x = int(raw_input("Please enter a number: "))
	except ValueError:
		print "lol"
		time.sleep(10)
		print "rofl"


	print "continued"

for x in range(10):
	testing(0)
