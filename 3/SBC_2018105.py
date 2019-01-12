#!/usr/bin/env python3

import re
import itertools

#Name : Suchet Aggarwal
#Roll. No. : 2018105
#Section : A
#Group : 1

ROLLNUM_REGEX = "201[0-9]{4}"


class Graph(object):
	name = "Suchet Aggarwal"
	email = "suchet18105@iiitd.ac.in"
	roll_num = "2018105"

	def __init__ (self, vertices, edges):
		"""
		Initializes object for the class Graph

		Args:
			vertices: List of integers specifying vertices in graph
			edges: List of 2-tuples specifying edges in graph
		"""

		self.vertices = vertices
		
		ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
		
		self.edges    = ordered_edges
		
		self.validate()

	def validate(self):
		"""
		Validates if Graph if valid or not

		Raises:
			Exception if:
				- Name is empty or not a string
				- Email is empty or not a string
				- Roll Number is not in correct format
				- vertices contains duplicates
				- edges contain duplicates
				- any endpoint of an edge is not in vertices
		"""

		if (not isinstance(self.name, str)) or self.name == "":
			raise Exception("Name can't be empty")

		if (not isinstance(self.email, str)) or self.email == "":
			raise Exception("Email can't be empty")

		if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
			raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

		if not all([isinstance(node, int) for node in self.vertices]):
			raise Exception("All vertices should be integers")

		elif len(self.vertices) != len(set(self.vertices)):
			duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

			raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

		edge_vertices = list(set(itertools.chain(*self.edges)))

		if not all([node in self.vertices for node in edge_vertices]):
			raise Exception("All endpoints of edges must belong in vertices")

		if len(self.edges) != len(set(self.edges)):
			duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

			raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))


	def getNeighbour(self,node):
		'''
		Finds all the neighbours to the given node

		Args:
			node : vertex adjacent to which neighbours are to be found

		Returns:
			list of neighbours
		'''
		ls=[]
		for i in self.edges:
			if node in i:
				ls.append(i[0])
				ls.append(i[1])
		while node in ls:
			ls.remove(node)
		return ls


	def min_dist(self, start_node, end_node):
		'''
		Finds minimum distance between start_node and end_node

		Args:
			start_node: Vertex to find distance from
			end_node: Vertex to find distance to

		Returns:
			An integer denoting minimum distance between start_node
			and end_node
			'''

		mark=[]

		#BFS Traversal
		queue=[start_node]
		BFS=Graph([],[])
		
		#ds records distance of each node from start node
		ds=[]
		for i in range(len(self.vertices)+1):
			ds.append(-1)
		ds[start_node]=0
		while queue:
			start_node= queue.pop(-1)
			mark.append(start_node)
			BFS.vertices.append(start_node)
			for i in self.getNeighbour(start_node):
				if i not in mark :
					mark.append(i)
					BFS.edges.append((start_node,i))
					queue.insert(0,i)
					ds[i]=ds[start_node]+1
					
		steps=ds[end_node]

		return steps


	def all_shortest_paths(self,start_node, end_node):
		"""
		Finds all shortest paths between start_node and end_node

		Args:
			start_node: Starting node for paths
			end_node: Destination node for paths

		Returns:
			A list of path, where each path is a list of integers.
		"""
		dist = self.min_dist(start_node, end_node)
		paths = self.all_paths(start_node, dist,visited=[], path=[])

		#chooding those paths which end on end node
		final=[]
		for j in paths:
			if j[dist] == end_node:
				final.append(j)
		return final
	


	def all_paths(self,node, dist,visited, path):
		"""
		Finds all paths from node with length = dist

		Args:
			node: Node to find path from
			dist: Allowed distance of path
			path: path already traversed

		Returns:
			List of path

			Returns None if there no paths
		"""
		path.append(node)
		returned_paths =[]

		#Base Cases
		if len(path) == dist+1:
			return path
					
		#Recursion
		for next_node in self.getNeighbour(node):
			if next_node not in path :
				returned_paths = self.all_paths(next_node, dist, visited, path[:])
				if returned_paths not in visited and returned_paths is not None:
					visited.append(returned_paths)
		
		mypaths=[]
		for i in visited:
			if not(isinstance(i[0],list)):
				mypaths.append(i)

		if len(mypaths) != 0 :
			return mypaths
		else:
			return None


	def betweenness_centrality(self, node):
		"""
		Find betweenness centrality of the given node

		Args:
			node: Node to find betweenness centrality of.

		Returns:
			Single floating point number, denoting betweenness centrality
			of the given node
		"""
		t=0
		BetCen=0
		n=len(self.vertices)
		for i in range(n):
			for j in range(i+1,n):
				if self.vertices[j]!=node and node!=self.vertices[i]:
					l=self.all_shortest_paths(self.vertices[i],self.vertices[j])
					X=len(l)
					Y=0
					for k in l:
						if node in k:
							Y=Y+1
					t= Y/X
					BetCen +=Y/X
					SBC= BetCen/(((n-1)*(n-2))/2)

		return "%0.2f" % SBC


	def top_k_betweenness_centrality(self):
		"""
		Find top k nodes based on highest equal betweenness centrality.

		
		Returns:
			List a integer, denoting top k nodes based on betweenness
			centrality.
		"""
		
		lsBC=[]
		for i in self.vertices:
			lsBC.append(self.betweenness_centrality(i))
		lsBC=list(map(float,lsBC)) 
		knode=[]
		for i in range(len(self.vertices)):
			if lsBC[i] == max(lsBC):
				knode.append(i+1) 
		return knode
		
		

if __name__ == "__main__":
	#Sample Input
	#vertices = [1, 2, 3, 4, 5, 6, 7]
	#edges    = [(1, 2),(1, 3),(2, 3), (3, 7),(7, 4),(7, 6),(4, 5),(6, 5)]
	vertices = [1, 2, 3, 4, 5, 6]
	edges    = [(1, 2), (1, 5), (2, 3), (2, 5), (3, 4), (4, 5), (4, 6), (3,6)]
	graph = Graph(vertices, edges)
	#Main Function Call
	knode=graph.top_k_betweenness_centrality()
	#Output
	print("The Top "+ str(len(knode)) + " Node(s) is/are: "+ str(knode))
	
	vertices = [1, 2, 3, 4, 5, 6]
	edges    = [(1, 2), (1, 5), (2, 5), (3, 4), (4, 5), (4, 6), (3,6)]
	graph = Graph(vertices, edges)
	#Main Function Call
	knode=graph.top_k_betweenness_centrality()
	#Output
	print("The Top "+ str(len(knode)) + " Node(s) is/are: "+ str(knode))
	
	vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
	edges    = [(0, 5), (1, 2), (2, 7), (3, 13), (0, 4), (5, 9), (6, 8), (4, 7), (1, 8), (8, 9), (10, 13), (6, 11), (3, 12), (6, 13)]
	graph = Graph(vertices, edges)
	#Main Function Call
	knode=graph.top_k_betweenness_centrality()
	#Output
	print("The Top "+ str(len(knode)) + " Node(s) is/are: "+ str(knode))
	