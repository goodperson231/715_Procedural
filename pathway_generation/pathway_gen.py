import networkx as nx
import matplotlib.pyplot as plt
import math
import random
from utils import doIntersect, fix_connections

def get_max_len_list(big_list):
	l = len(max(big_list, key=len))
	small_list = []
	for ll in big_list:
		if len(ll) == l:
			small_list.append(ll)
	return(small_list)

def make_graph(G):
	G.add_node(1,pos=(1,1), boundary="outer-boundary")
	G.add_node(2,pos=(1,12), boundary="outer-boundary")
	G.add_node(3,pos=(6,1), boundary="outer-boundary")
	G.add_node(4,pos=(6,12), boundary="outer-boundary")

	G.add_node(5,pos=(1,6), boundary="outer-boundary")
	G.add_node(6,pos=(3,1), boundary="outer-boundary")
	G.add_node(7,pos=(6,6), boundary="outer-boundary")
	G.add_node(8,pos=(4,12), boundary="outer-boundary")
	G.add_node(9,pos=(1,10), boundary="outer-boundary")
	G.add_node(10,pos=(6,9), boundary="outer-boundary")
	G.add_node(11,pos=(4,6), boundary="inner-boundary")
	G.add_node(12,pos=(4,9), boundary="inner-boundary")
	G.add_node(13,pos=(4,10), boundary="inner-boundary")
	G.add_node(14,pos=(3,6), boundary="inner-boundary")

	edges = [(1, 5), (5,9),(9,2), (1, 6),(6,3), (2,8),(8,4), (5,14), (3,7),(7,10),(10,4),
	 (6,14), (14,11), (11,7), (11,12), (12,13), (13,8), (13, 9), (12,10)]

	G.add_edges_from(edges)

	attrs = {(1, 5): {"boundary": "outer-boundary", "part_of": "hall"}, 
	(1, 6): {"boundary": "outer-boundary", "part_of": "hall"},
	(5,14): {"boundary": "inner-boundary", "part_of": "hall"},
	(6,14): {"boundary": "inner-boundary", "part_of": "hall"},
	(5,9): {"boundary": "outer-boundary", "part_of": "null"},
	(9,2): {"boundary": "outer-boundary", "part_of": "null"},
	(6,3): {"boundary": "outer-boundary", "part_of": "null"},
	(2,8): {"boundary": "outer-boundary", "part_of": "null"},
	(8,4): {"boundary": "outer-boundary", "part_of": "null"},
	(3,7): {"boundary": "outer-boundary", "part_of": "null"},
	(7,10): {"boundary": "outer-boundary", "part_of": "null"},
	(10,4): {"boundary": "outer-boundary", "part_of": "null"},
	(14,11): {"boundary": "inner-boundary", "part_of": "null"},
	(11,7): {"boundary": "inner-boundary", "part_of": "null"},
	(11,12): {"boundary": "inner-boundary", "part_of": "null"},
	(12,13): {"boundary": "inner-boundary", "part_of": "null"},
	(13,8): {"boundary": "inner-boundary", "part_of": "null"},
	(13,9): {"boundary": "inner-boundary", "part_of": "null"},
	(12,10): {"boundary": "inner-boundary", "part_of": "null"}}
	nx.set_edge_attributes(G, attrs)
	return(G)

def remove_irrlevant_nodes(G, node_coords):

	outer_boundary = []
	hall_inner = []
	inner_edge = []

	for edges in G.edges:
		
		if G[edges[0]][edges[1]]["part_of"] == "hall" and G[edges[0]][edges[1]]["boundary"] == "inner-boundary":
			hall_inner.append((edges[0], edges[1]))
			G.remove_edge(edges[0],edges[1])

		elif G[edges[0]][edges[1]]["boundary"] == "outer-boundary":
			outer_boundary.append((edges[0], edges[1]))
			G.remove_edge(edges[0],edges[1])
		else:
			inner_edge.append((edges[0], edges[1]))

	return(outer_boundary, hall_inner, inner_edge)

def get_min_max(O_points, node_coords):

	x_max = 0
	x_min = 999
	y_max = 0
	y_min = 999

	for point in O_points:
		if node_coords[point][0] > x_max:
			x_max = node_coords[point][0]
		if node_coords[point][0] < x_min:
			x_min = node_coords[point][0]
		if node_coords[point][1] > y_max:
			y_max = node_coords[point][1]
		if node_coords[point][1] < y_min:
			y_min = node_coords[point][1]
	return([x_min, x_max, y_min, y_max])


def check_intersect(p1, p2, q1, q2, node_coords):

	X1 = node_coords[p1][0]
	X2 = node_coords[p2][0] 
	Y1 = node_coords[p1][1]
	Y2 = node_coords[p2][1]
	X3 = node_coords[q1][0]
	X4 = node_coords[q2][0]
	Y3 = node_coords[q1][1]
	Y4 = node_coords[q2][1]

	if X1 - X2 == 0:
		A1 = float("inf")
	else:
		A1 = (Y1-Y2)/(X1-X2)  

	if X3 - X4 == 0:
		A2 = float("inf")
	else:
		A2 = (Y3-Y4)/(X3-X4)  

	if (max(X1,X2) < min(X3,X4)):
		return(0)

	if min(X1,X2) > max(X3,X4): 
		return(0)
	if max(Y1,Y2) > min(Y3,Y4): 
		return(0)
	if min(Y1,Y2) > max(Y3,Y4): 
		return(0)

	b1 = Y1 - A1*X1 
	b2 = Y3 - A2*X3 

	if A1 == A2:
		return(0)
	
	Xa = (b2 - b1) / (A1 - A2)

	Ya = A1 * Xa + b1

	if ((Xa < max( min(X1,X2), min(X3,X4) )) or (Xa > min(max(X1,X2), max(X3,X4)))):
		return(0)  # intersection is out of bound
	elif ((Ya < max( min(Y1,Y2), min(Y3,Y4) )) or (Ya > min(max(Y1,Y2), max(Y3,Y4)))):
		return(0)
	else:
		return(1)


# def fix_connections(G):
# 	G.remove_edge(11,7)
# 	G.remove_edge(12,10)
# 	G.remove_edge(14,6)
# 	G.remove_edge(8,4)
# 	G.add_edge(140,6)
# 	G.add_edge(8,80)
# 	G.add_edge(80,4)
# 	node_coords = nx.get_node_attributes(G, 'pos')

# 	G.add_node(150, pos=(node_coords[110][0], node_coords[7][1]))
# 	G.add_node(160, pos=(node_coords[110][0], node_coords[10][1]))

# 	G.remove_node(120)
# 	G.remove_node(130)

# 	G.add_edge(150,7)
# 	G.add_edge(160,10)
# 	G.add_edge(110,150)
# 	G.add_edge(150,160)
# 	G.add_edge(160,80)

# 	return(G)

def main():
	G = nx.Graph()

	G = make_graph(G)
	
	#print(G[1][5]["part_of"])

	node_coords = nx.get_node_attributes(G, 'pos')

	outer_boundary, hall_inner, inner_edge = remove_irrlevant_nodes(G, node_coords)

	for edges in G.edges:
		distance = math.sqrt((node_coords[edges[0]][0] - node_coords[edges[1]][0])**2 + (node_coords[edges[0]][1] - node_coords[edges[1]][1])**2)
		G[edges[0]][edges[1]]['weight'] = distance

	#print(G.edges)
	weight = nx.get_edge_attributes(G, 'weight')
	node_part = nx.get_node_attributes(G, 'boundary')
	#print(weight)


	outer_points = []
	inner_points = []
	points = []

	for edge in inner_edge:
		points.append(edge[0])
		points.append(edge[1])

	points = set(points)
	for point in points:
		if node_part[point] == "outer-boundary":
			outer_points.append(point)
		else:
			inner_points.append(point)

	# print(inner_points)
	# print(outer_points)

	small_sp = 100
	hallway_path = 0
	big_list = []

	for pt_1 in outer_points:
		for pt_2 in inner_points:
			sp = nx.shortest_path(G, source=pt_2, target=pt_1, weight='weight')
			big_list.append(sp)

	small_list = get_max_len_list(big_list)

	for sl in small_list:
		lp = nx.shortest_path_length(G, source=sl[0],  target=sl[-1], weight='weight')
		if lp < small_sp:
			small_sp = lp
			hallway_path = sl

	print("hallway nodes", hallway_path)

	"""
		Pathway movement
	"""
	G = make_graph(G)


	hallway_path_copy = [x * 10 for x in hallway_path]

	for point in hallway_path:
		G.add_node(point*10, pos=node_coords[point], boundary=node_part[point])


	for i in range(0, len(hallway_path) - 1):
		G.add_edge(hallway_path[i]*10, hallway_path[i+1]*10, boundary="inner-boundary", part_of="null")

	# for point in hallway_path:

	O_points = [k for k,v in node_part.items() if v == "outer-boundary"]

	mm_coords = get_min_max(O_points, node_coords)

	up_flag = 0
	down_flag = 0
	left_flag = 0
	right_flag = 0

	if node_coords[hallway_path[-1]][1] == mm_coords[3]:
		up_flag = 1
	elif node_coords[hallway_path[-1]][1] == mm_coords[2]:
		down_flag = 1
	elif node_coords[hallway_path[-1]][0] == mm_coords[1]:
		right_flag = 1
	elif node_coords[hallway_path[-1]][0] == mm_coords[0]:
		left_flag = 1


	if up_flag or down_flag:
		next_dir = random.randint(0, 1)
		if not next_dir:
			left_flag = 1
		elif next_dir:
			right_flag = 1
	elif left_flag or down_flag:
		next_dir = random.randint(0,1)
		if not next_dir:
			up_flag = 1
		elif next_dir:
			down_flag = 1

	node_coords = nx.get_node_attributes(G, 'pos')
	node_part = nx.get_node_attributes(G, 'boundary')

	move = 0.5

	if not left_flag:
		for node in hallway_path_copy:
			G.nodes[node]['pos'] = (G.nodes[node]['pos'][0] - move, G.nodes[node]['pos'][1])
	elif not right_flag:
		for node in hallway_path_copy[1:]:
			G.nodes[node]['pos'] = (G.nodes[node]['pos'][0] + move, G.nodes[node]['pos'][1])

	if not down_flag:
		for node in hallway_path_copy:
			if node_part[node] != "outer-boundary":
				G.nodes[node]['pos'] = (G.nodes[node]['pos'][0], G.nodes[node]['pos'][1] - move)
	elif not up_flag:
		for node in hallway_path_copy:
			if node_part[node] != "outer-boundary":
				G.nodes[node]['pos'] = (G.nodes[node]['pos'][0], G.nodes[node]['pos'][1] + move)


	node_coords = nx.get_node_attributes(G, 'pos')

	print(up_flag, down_flag, left_flag, right_flag)

	big_flag = [up_flag, down_flag, left_flag, right_flag]

	if_flag = True
	for i in range(0, len(hallway_path)-1):
		for j in range(0, len(hallway_path_copy)-1):
			p1 = [node_coords[hallway_path[i]][0], node_coords[hallway_path[i]][1]]
			q1 = [node_coords[hallway_path[i+1]][0], node_coords[hallway_path[i+1]][1]]
			p2 = [node_coords[hallway_path_copy[j]][0], node_coords[hallway_path_copy[j]][1]]
			q2 = [node_coords[hallway_path_copy[j+1]][0], node_coords[hallway_path_copy[j+1]][1]]
			inter_flag = doIntersect(p1,q1,p2,q2)
			if_flag = if_flag*inter_flag

	print(if_flag)
	if if_flag == 0:
		G.nodes[hallway_path[0]*10]['pos'] = (G.nodes[hallway_path[0]]['pos'][0], G.nodes[hallway_path[0]]['pos'][1] - move)
		G.nodes[hallway_path[-1]*10]['pos'] = (G.nodes[hallway_path[-1]]['pos'][0] + move, G.nodes[hallway_path[-1]]['pos'][1])
		for i in range(1, len(hallway_path)-1):
			G.nodes[hallway_path[i]*10]['pos'] = (G.nodes[hallway_path[i]]['pos'][0] + move, G.nodes[hallway_path[i]]['pos'][1] - move)
			
	G = fix_connections(G)

	nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, node_size=100, font_size=6)

	#nx.draw_networkx_edge_labels(G, nx.get_node_attributes(G, 'pos'), edge_labels=attrs, font_color='red')
	plt.savefig('foo.png')

if __name__ == '__main__':
	main()
