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

def odd_pal(neighbors,tree):
	head = tree.root
	for node_1, node_2 in neighbors:
		lca_node = tree.lca(node_1,node_2)
		if lca_node.string_depth() > head.string_depth():
			head = lca_node
	res = str(head)
	res = (res[::-1])[:-1] + res
	return res

def even_pal(neighbors,tree):
	if not len(neighbors):
		return ""

	head = None
	mid = ""
	for mid_char, node_2,node_3 in neighbors:
		lca_node = tree.lca(node_2,node_3)
		if head is None or  lca_node.string_depth() > head.string_depth():
			head = lca_node
			mid = mid_char

	if(head == tree.root):
		head = ""

	res = str(head)
	res = (res[::-1]) + (mid*2) + res
	return res

def get_pal_neighbor_leaves(tree, text):
	n = len(text)
	string_leaves = {}
	reverse_leaves = {}
	
	def f(node):
		if node.is_leaf():
			if node.str_id == 0: string_leaves[node.path.start] = node
			if node.str_id == 1: reverse_leaves[node.path.start] = node
	tree.root.post_order(f)

	odd_neighbors = [(string_leaves[i], reverse_leaves[n - i - 1]) for i in range(n)]
	even_neighbors = [(text[i], string_leaves[i+1], reverse_leaves[n - i + 1]) for i in range(1, n - 1) if text[i] == text[i-1]]
	return odd_neighbors, even_neighbors


def find_palindrom(text):
	tree = generate_tree([text, text[::-1]])
	tree.prepare_lca()
	odd_leaves, even_leaves = get_pal_neighbor_leaves(tree, text)
	odd_pal_str = odd_pal(odd_leaves, tree)
	even_pal_str = even_pal(even_leaves, tree)
	ans = max(odd_pal_str, even_pal_str, key=len)
	positions = find_all(tree, ans)[0]
	return ans, positions
	
if __name__ == "__main__":
	ans = find_palindrom("abcggecba")
	print(ans)