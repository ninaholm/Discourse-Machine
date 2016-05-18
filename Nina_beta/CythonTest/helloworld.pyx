class ParseOption(object):
	def __init__(self):
		pass

	def set_variables(self, str const, float prob, left):
		self.constituent = const
		self.probability = prob
		self.left_coord = left

	def __repr__(self):
		return self.constituent + " " + str(self.probability)