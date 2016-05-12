from treelib import Node, Tree
import sys


s = "Jeg er glad".split(" ")

nt_start = len(s)
print nt_start

tree = Tree()
tree.create_node("S", nt_start)
tree.create_node("NP", nt_start+1, parent=nt_start)
tree.create_node("VP", nt_start+2, parent=nt_start)

tree.create_node("Jeg", s.index("Jeg"), parent=4)
tree.create_node("er", s.index("er"), parent=5)
tree.create_node("glad", s.index("glad"), parent=5)

tree.show()

searchword = "glad"
wid = s.index(searchword)
node = tree.get_node(wid)

print




entity = "er"
opinionw = "glad"


# Find lowest common ancestor

def get_LCA(root, n1, n2):
	if root is None: return None
	if root == n1 or root == n2: return root
	if len(tree.get_node(root).fpointer) == 0: return None #if leaf, return None
	if len(tree.get_node(root).fpointer) == 1: #if terminal node, check its single leaf node
		return get_LCA(tree.get_node(root).fpointer[0], n1, n2)

	if len(tree.get_node(root).fpointer) == 2:
		left = get_LCA(tree.get_node(root).fpointer[0],n1,n2)
		right = get_LCA(tree.get_node(root).fpointer[1],n1,n2)

	if left is not None and right is not None: return root
	if left is not None: return left
	if right is not None:return right

	return None


LCA = get_LCA(tree.root, s.index(entity), s.index(opinionw))

# Calculate distance between two nodes
distance = tree.depth(tree.get_node(s.index(entity))) + tree.depth(tree.get_node(s.index(opinionw)))
distance = distance - 2 * tree.depth(tree.get_node(LCA))

print "Looking for words:", entity, opinionw
print "LCA is", tree.get_node(LCA).tag
print "Distance is", distance





def get_distance(word1, word2, tree):
	pass








sys.exit()

# DICTIONARY TREE TEST

from collections import defaultdict

def Tree():
    return defaultdict(Tree)

def prettyprint(t): return {k: prettyprint(t[k]) for k in t}

tree = Tree()

tree['S']['NP']['fish']
tree['S']['VP']['swim']

print prettyprint(tree)















