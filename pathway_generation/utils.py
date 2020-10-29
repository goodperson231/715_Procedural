import networkx as nx

def onSegment(p, q, r): 
	if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
		(q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))): 
		return True
	return False

def orientation(p, q, r): 

	
	val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
	if (val > 0): 
		
		# Clockwise orientation 
		return 1
	elif (val < 0): 
		
		# Counterclockwise orientation 
		return 2
	else: 
		
		# Colinear orientation 
		return 0

# The main function that returns true if 
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
	
	# Find the 4 orientations required for 
	# the general and special cases 
	o1 = orientation(p1, q1, p2) 
	o2 = orientation(p1, q1, q2) 
	o3 = orientation(p2, q2, p1) 
	o4 = orientation(p2, q2, q1) 

	# General case 
	if ((o1 != o2) and (o3 != o4)): 
		return False

	# Special Cases 

	# p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
	if ((o1 == 0) and onSegment(p1, p2, q1)): 
		return False

	# p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
	if ((o2 == 0) and onSegment(p1, q2, q1)): 
		return False

	# p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
	if ((o3 == 0) and onSegment(p2, p1, q2)): 
		return False

	# p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
	if ((o4 == 0) and onSegment(p2, q1, q2)): 
		return False

	# If none of the cases 
	return True

def fix_connections(G):
	G.remove_edge(11,7)
	G.remove_edge(12,10)
	G.remove_edge(14,6)
	G.remove_edge(8,4)
	G.add_edge(140,6)
	G.add_edge(8,80)
	G.add_edge(80,4)
	node_coords = nx.get_node_attributes(G, 'pos')

	G.add_node(150, pos=(node_coords[110][0], node_coords[7][1]))
	G.add_node(160, pos=(node_coords[110][0], node_coords[10][1]))

	G.remove_node(120)
	G.remove_node(130)

	G.add_edge(150,7)
	G.add_edge(160,10)
	G.add_edge(110,150)
	G.add_edge(150,160)
	G.add_edge(160,80)

	return(G)