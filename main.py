import sys
from src.tree import Tree
from Bio import SeqIO

max_node = [1,1]

def generate_tree(texts):
	trees = {}
	for i in range(len(texts)):
		trees.update({i:texts[i]})
	return Tree(trees)	

def generate_tree_from_file(dir):
	with open(dir, "rU") as handle:
		texts_with_ids =  SeqIO.parse(handle, "fasta")
		texts = list(map(lambda x: x.seq, texts_with_ids))
		return generate_tree(texts)

def find_all(tree, query):
	all_paths = tree.find_all(query)
	res = {}
	for tree_id, path in all_paths:
		if not tree_id in res.keys():
			res[tree_id] = []
		res[tree_id].append(path.k)
	return res

def compute_leaf_number (node):
	if(node.is_leaf()):
		node.leaf_numbers = {node.str_id:1}
	else:
		node.leaf_numbers = {}
		
		for child in node.children.values():			
			temp = compute_leaf_number(child)  
			for key in temp :
				node.leaf_numbers[key] = temp[key] + node.leaf_numbers.get(key,0)
	return(node.leaf_numbers)

def compute_k_repeat(node,k):
	if( node.leaf_numbers.get(0,-1) >= k  and node.string_depth() >max_node[1] ):
		max_node[0] = node 
		max_node[1] = node.string_depth()
	if(node.is_leaf() == False):
		for child in node.children.values():
			compute_k_repeat(child,k)



def compute_k_lcs(node, k):
	global max_node
	if( len(node.leaf_numbers.keys()) >= k  and node.string_depth() > max_node[1] ):
		max_node[0] = node 
		max_node[1] = node.string_depth()
	if node.is_internal():
		for child in node.children.values():
			compute_k_lcs(child,k)


def find_repeats(tree, k):
	global max_node
	compute_leaf_number(tree.root)
	max_node = [tree.root, 0]
	compute_k_repeat(tree.root, k)
	paths = max_node[0].get_positions()
	res = {}
	for tree_id, path in paths:
		if not tree_id in res.keys():
			res[tree_id] = []
		res[tree_id].append(path.k)
	return str(max_node[0]), res


def find_lcs(tree, k):
	global max_node
	compute_leaf_number(tree.root)
	max_node = [tree.root, 0]
	compute_k_lcs(tree.root, k)
	paths = max_node[0].get_positions()
	res = {}
	for tree_id, path in paths:
		if not tree_id in res.keys():
			res[tree_id] = []
		res[tree_id].append(path.k)
	return str(max_node[0]), res


def find_palindrom(text):
	tree = generate_tree([text, text[::-1]])
	tree.prepare_lca()
	all_paths = tree.root.get_positions()
	string_paths = [x[1] for x in all_paths if x[0] == 0]
	reverse_paths = [x[1] for x in all_paths if x[0] == 1]
	string_paths.sort(key=lambda x: x.k)
	reverse_paths.sort(key=lambda x: x.k)
	for path in string_paths:
		print(path, ",", path.k)
	for path in reverse_paths:
		print(path, ",", path.k)
	

if __name__ == "__main__":
	find_palindrom("banana")