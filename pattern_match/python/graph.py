from __future__ import division
import os
import csv
import networkx as nx
from numpy import linalg as LA
import numpy as np
import statistics as st
import scipy.stats
from collections import defaultdict
import heapq

# from sklearn import manifold
# import scipy.spatial.distance as dist

class graph:
	""" graph class definition"""

	def __init__(self, graph_file):
		# create a graph from graph_file
		# load input graph: each line [src, tar, w]
		G = nx.Graph()
		with open(graph_file, 'r') as fr:
			reader = csv.reader(fr)
			reader.next()
			node_list = list(reader)
			for row in node_list:
				G.add_edge(row[0],row[1],weight=row[2])

		self.G = G
		self.statistics = {"#node": len(G.nodes()), "#edge": len(G.edges())}

	# get statistics result
	def getStatistics(self):
		return self.statistics


	# check if egonet 
	# max node degree is much larger than the second max
	def isEgo(self, th_ego1, th_ego2):
		G = self.G
		isEgo = False
		nodes = G.nodes()
		degrees = []

		for node in nodes:
			deg = G.degree(node)
			degrees.append(deg)

		max_deg = max(degrees)
		second_max_deg = heapq.nlargest(2, degrees)[1]

		# print('max degree is: ', max_deg)
		ego_ratio = max_deg/(len(nodes)-1)
		second_ego_ratio = second_max_deg/(len(nodes)-1)
		print('th_ego is: ', ego_ratio)
		self.statistics['th_ego'] = round(ego_ratio, 3)

		if( (ego_ratio>th_ego1) and (second_ego_ratio<th_ego2) ):
			isEgo = True
		return isEgo 

	# detect cycle in the graph
	# if yes, return #nodes in the cycle; if no, return -1
	def maxCycle(self, th_cyc):
		G = self.G
		isCycle = False
		nodes = G.nodes()

		# detect all cycles
		cycles = [[node]+path  for node in G for path in self.dfs(G, node, node)]
		# largest
		max_cyc_size = 0
		max_cyc = []
		for cycle in cycles:
			if(len(cycle)>3 and len(cycle)>max_cyc_size):
				max_cyc = cycle
				max_cyc_size = len(cycle)-1

		# print ("the max cycle:", max_cyc)
		# print ("size of the max cycle:", max_cyc_size)
		cyc_ratio = max_cyc_size/len(nodes)
		print ("th_cyc:", cyc_ratio)
		self.statistics['th_cyc'] = round(cyc_ratio, 3)

		if(cyc_ratio > th_cyc):
			isCycle = True
# 
		return [ isCycle, max_cyc[:-1] ]    # start node same with end node 


	# calc edge density
	def isDense(self, node_set, th_den):
		G = self.G
		isDense = False
		edges = G.edges()
		nodes = G.nodes()
		edge_count = 0
		n = len(node_set)

		for n1 in node_set:
			for n2 in node_set:
				if (n1, n2) in edges:
					edge_count += 1
		density = edge_count / (n*(n-1)/2)
		# print('edge num in cycle: ', edge_count)
		print('th_den: ', density)
		self.statistics['th_den'] = round(density, 3)

		if(density>th_den):
			isDense = True

		return isDense


	# find the longest path in graph
	def isChain(self, th_dep):
		G = self.G
		isChain = False
		nodes = G.nodes()
		len_paths = []       # store longest paths from all nodes
		longest_path = []

		for node in nodes:
			start_node = node   
			all_paths = self.path_DFS(start_node, seen=None, path=None)

			max_len   = max(len(p) for p in all_paths)
			max_paths = [p for p in all_paths if len(p) == max_len]   # longest path from current node
			if(len(max_paths[0]) > len(longest_path) ):
				longest_path = max_paths[0]
			len_paths.append(len(max_paths[0]))

		depth = max(len_paths)
		# print ("Longest path: ", longest_path)
		# print ("Depth: ", depth)
		dep_ratio = depth/len(nodes)
		print ("th_dep: ", dep_ratio)
		self.statistics['th_dep'] = round(dep_ratio, 3)

		if(depth > th_dep*len(nodes)):
			isChain = True

		return isChain


	# dfs, complexity : O(V+E)
	def dfs(self, graph, start, end):
	    fringe = [(start, [])]
	    while fringe:
	        state, path = fringe.pop()
	        if path and state == end:
	            yield path
	            continue
	        for next_state in graph[state]:
	            if next_state in path:
	                continue
	            fringe.append((next_state, path+[next_state]))



	# path_DFS
	def path_DFS(self, v, seen=None, path=None):
		G = self.G
		edges = G.edges()
		
		lists = defaultdict(list)
		for (s,t) in edges:
		    lists[s].append(t)
		    lists[t].append(s)

		if seen is None: seen = []
		if path is None: path = [v]

		seen.append(v)

		paths = []
		for t in lists[v]:
			if (t not in seen):
				t_path = path + [t]
				paths.append(tuple(t_path))
				paths.extend(self.path_DFS(t, seen[:], t_path))

		return paths


	# graph signature
	def signature(self):
		G = self.G
		edges = G.edges() 
		nodes = G.nodes()

		graph_feature = []   # 2D: node_num * feature dimention
		feature_num = 6      # 6 basic metrics from Netsimile  &  4 custom defined

		for node in nodes:
			feature = []    # for each node
			neighbor_num = len(G.neighbors(node))  # 1: number of neighbors
			feature.append(neighbor_num)

			coefficient = nx.clustering(G, node)   # 2: clustering coefficient
			feature.append(coefficient)

			up_two_hop = nx.single_source_shortest_path_length(G, node, cutoff=2)  # all nodes which has shortest path to "node" with length less than 2
			up_one_hop = nx.single_source_shortest_path_length(G, node, cutoff=1)
			two_hop = {k:v for k,v in up_two_hop.items() if k not in up_one_hop}
			two_hop_avg = len(two_hop)/(neighbor_num)    #  3: average number of node's two-hop away neighbours
			feature.append(two_hop_avg)

			coefficient_sum = 0
			for vertex in G.neighbors(node):
				coefficient_sum += nx.clustering(G, vertex)
			coefficient_avg = coefficient_sum/neighbor_num
			feature.append(coefficient_avg)    #   4: average clustering coefficient of neighbours

			ego_net = nx.ego_graph(G, node, undirected=True)   # egonet of 'node', type: graph
			edge_num = len(ego_net.edges())   # 5:  number of edges in egonet of 'node'
			feature.append(edge_num)

			ego_neighbor_num = 0              # 6: number of egonet's neighbors
			egonet_no_center = nx.ego_graph(G, node, undirected=True, center=False)   # exclude the center vertex
			for vertex in egonet_no_center.nodes():
				G_degree = G.degree(vertex)
				ego_degree = egonet_no_center.degree(vertex)+1
				ego_neighbor_num += (G_degree - ego_degree)     
			feature.append(ego_neighbor_num)  

			graph_feature.append(feature)


		##################    Normalization for 'statistical hypothesis testing'   ################## 
		# L2_norm = LA.norm(graph_feature, ord=2, axis=0)  # vactor, length=6 (#features)

		# # Each feature column divide by corresponding element in L2_norm
		# normalized_mtx = graph_feature / L2_norm[None,:]


		###########################    Aggregation    ########################### 
		graph_signature = []
		feature_matrix = np.asmatrix(graph_feature)   # convert 2D array to matrix
		# print('graph matrix shape: ', feature_matrix.shape)

		for i in range(0,feature_num):
			column = feature_matrix[:,i]

			median = float(st.median(column)) # aggregator 1
			graph_signature.append(median)

			mean = np.mean(column)     # aggregator 2
			graph_signature.append(mean)

			std_dev = np.std(column)  # aggregator 3
			graph_signature.append(std_dev)

			skew = float(scipy.stats.skew(column))   # aggregator 4
			graph_signature.append(skew)

			kurtosis = float(scipy.stats.kurtosis(column))   # aggregator 5
			graph_signature.append(kurtosis)

		# print('signature length: ', len(graph_signature))

		# above: local attributes
		# below: global attributes

		# 7: max node degree 
		# graph_signature.append()
		# 8: largest cycle size
		# 9: longest path
		# 10: edge density among nodes in cycle
		return graph_signature

		