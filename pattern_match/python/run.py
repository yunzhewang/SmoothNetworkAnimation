from __future__ import division
import json
import csv
import os
import networkx as nx
import numpy as np
from graph import graph
from util import util
from genPattern import genPattern
import scipy.spatial.distance as dist
import time

if __name__ == '__main__':

	directory = '../data/'
	filename = 'graph.csv'

	# convert json graph to csv format
	json_file = '/Users/WANGYunzhe/Downloads/data.json'
	util = util()
	util.json2csv(json_file)

	#######################    Gen Patterns    #######################
	gen_ptn = genPattern(directory+filename)  # according to graph data
	gen_ptn.gen_pattern()
	#######################    Gen Patterns    #######################


	#######################    Custom    #######################
	# load pieces, if data in json, transfer to  CSV first !!!
	# ptn1: chain;  ptn2: loop;  ptn3: clique;  ptn4: egocentric
	#  calc ALL Metrics!!!    &&  Logic
	predict_graph = graph(directory+filename)
	pattern = None
	th_ego1 = 0.85
	th_ego2 = 0.5
	th_cyc = 0.59
	th_den = 0.84
	th_dep = 0.85
	start_time = time.time()
	isEgo = predict_graph.isEgo(th_ego1, th_ego2)    
	if(isEgo):
		pattern = 'egocentric'         # ego: threshold, check if it is ego
	else:
		cyc_result = predict_graph.maxCycle(th_cyc)
		isCycle = cyc_result[0]
		cyc_nodes = cyc_result[1]

		if(isCycle):
			isDense = predict_graph.isDense(cyc_nodes, th_den)
			if(isDense):
				pattern = 'clique'        # clique: cycle && high density
			else:                         # loop: cycle &&  low density
				pattern = 'loop'
		else:
			if(predict_graph.isChain(th_dep)):
				pattern = 'chain'                           # chain: no large cycle  &   have long path
			else:
				pattern = 'unknown'
	end_time = time.time()
	print('\n')
	print('time taken is: ', (end_time-start_time)%60, 'seconds')
	print('\n')
	print('custom pattern is: ', pattern)

	#######################    Custom    #######################





	#######################    NetSimiler    #######################
	graph_sig = predict_graph.signature()
	# print('graph signature: ', graph_sig)

	# pattern signatures
	chain = graph('../data/pattern1.csv')
	loop = graph('../data/pattern2.csv')
	clique = graph('../data/pattern3.csv')
	egocentric = graph('../data/pattern4.csv')
	sig_ptn1 = chain.signature()
	sig_ptn2 = loop.signature()
	sig_ptn3 = clique.signature()
	sig_ptn4 = egocentric.signature()

	# distances
	dist_1 = dist.canberra(sig_ptn1, graph_sig)
	dist_2 = dist.canberra(sig_ptn2, graph_sig)
	dist_3 = dist.canberra(sig_ptn3, graph_sig)
	dist_4 = dist.canberra(sig_ptn4, graph_sig)

	# find min
	distances = [dist_1, dist_2, dist_3, dist_4]
	dist_min = min(distances)


	# find pattern
	patterns = ['chain', 'loop', 'clique', 'egocentric']
	print("netsimile pattern is: ", patterns[distances.index(dist_min)])
 
	#######################    NetSimiler    #######################

	# statistics = {}
	statistics = predict_graph.getStatistics()
	statistics['pattern'] = pattern
	statistics['netsimile'] = patterns[distances.index(dist_min)]
	statistics['time'] = (end_time-start_time)%60
	print('Statistics is: ', statistics)
	#######################    Write Statistics    #######################
	header = ["#node", "#edge", "th_den", "th_dep", "th_ego", "th_cyc", "pattern", "netsimile", "time"]

	with open('/Users/WANGYunzhe/Desktop/Journal/program/graph_generator/pattern_statistics.csv', 'a') as fw:
		writer = csv.writer(fw, delimiter=',')
		for item in header:
			if(item not in statistics):
				statistics[item] = '-'
		row = [statistics['#node'], statistics['#edge'], statistics['th_den'], statistics['th_dep'],
			   statistics['th_ego'], statistics['th_cyc'], statistics['pattern'], statistics['netsimile'],
			   statistics['time']]
		writer.writerow(row)
	#######################    Write Statistics    #######################

