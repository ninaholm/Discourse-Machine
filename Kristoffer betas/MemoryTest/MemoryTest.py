import guppy
from guppy import hpy

hp = hpy()

print "lol"

hp.setrelheap()

test = {}
lol = "hahalol"

for x in range(1000):
	test[x] = "test2" * 1000 * x

print "test2" * 1000

h = hp.heap().by

print h.bytype