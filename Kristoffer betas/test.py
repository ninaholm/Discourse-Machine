for x in range(1997,2017):
	for y in range(01,13):
		if y>9:
			print "%s%s,0"%(x,y)
		else:
			print "%s0%s,0"%(x,y)