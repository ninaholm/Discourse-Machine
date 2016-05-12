# Binary tree for extracting the most probably parse of a sentence in the sentence_matrix
class Tree(object):
	def __init__(self, sentence_matrix):
		self.matrix = sentence_matrix
		self.size = 0

	# Builds a syntactic tree based on the ParseOption object for a legal S in the sentence_matrix.
	def build_tree(self, parse_root):
		self.root = self._create_node(parse_root, 1)

	# recursive utility function for building the tree
	def _create_node(self, parse_option, depth):
		if parse_option is None:
			return None
		else:
			value = parse_option.constituent
			if parse_option.left_coord is not None:
				left_child = self.matrix[parse_option.left_coord[0]][parse_option.left_coord[1]][parse_option.left_coord[2]]
				right_child = self.matrix[parse_option.right_coord[0]][parse_option.right_coord[1]][parse_option.right_coord[2]]
				self.size = self.size +1
				self.depth = depth
				return Node(value, self._create_node(left_child, depth+1), self._create_node(right_child, depth+1))
			else:
				node = Node(value, None, None)
				node.leaf = True
				node.leaf_word = self.matrix[parse_option.own_coord[0]-1][parse_option.own_coord[1]][0]
				self.size = self.size +1
				return node

	def print_tree(self):
		print self.root.print_self(0)

	def get_distance(word1, word2):
		return 0

	def 



class Node(object):
	def __init__(self, value, left_child, right_child):
		self.value = value
		self.left_child = left_child
		self.right_child = right_child
		self.leaf = False
		self.head = ""
		self.depth = 0


	def print_self(self, depth,):
		ret = ""

		# Print right branch
		if self.right_child != None:
			ret += self.right_child.print_self(depth + 1)

		# Print own value
		ret += "\n" + ("    "*depth) + str(self.value)
		if self.right_child is None:
			ret += " --- " + str(self.leaf_word) + str(depth)

		# Print left branch
		if self.left_child != None:
			ret += self.left_child.print_self(depth + 1)

		return ret