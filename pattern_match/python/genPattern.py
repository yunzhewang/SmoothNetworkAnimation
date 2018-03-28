import csv
import networkx as nx
import matplotlib.pyplot as plt

class genPattern:
	"""docstring for genPattern"""
	def __init__(self, graph_file):
		self.graph_file = graph_file

	def gen_pattern(self):		
		data = []
		with open(self.graph_file, 'rb') as fr:
			reader = csv.reader(fr)
			reader.next()
			data = list(reader)

		node_num = int(data[0][-1])      # weight encode the 'num of nodes'
		print ('node num: ', node_num)
		print ('edge num: ', len(data))
		print ('\n')

		# gen string pattern
		head = 1
		links = []
		link_weight = 10
		for i in range(2, node_num+1):
			tmp_link = [head, i, link_weight]
			head = i
			links.append(tmp_link)

		# write to current project for NetSimile
		with open('../data/pattern1.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)
		# write to graph_generator folder for displaying
		with open('/Users/WANGYunzhe/Desktop/Journal/program/graph_generator/data/pattern/pattern1.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)

		# gen ring pattern
		links.append([head, 1, link_weight])
		with open('../data/pattern2.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)
		with open('/Users/WANGYunzhe/Desktop/Journal/program/graph_generator/data/pattern/pattern2.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)

		# gen dense pattern
		links = []
		for i in range(1, node_num):
			for j in range(i+1, node_num+1):
				tmp_link = [i, j, link_weight]
				links.append(tmp_link)
		with open('../data/pattern3.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)
		with open('/Users/WANGYunzhe/Desktop/Journal/program/graph_generator/data/pattern/pattern3.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)

		# gen star pattern
		links = []
		center = 1
		for i in range(2, node_num+1):
			tmp_link = [center, i, link_weight]
			links.append(tmp_link)
		with open('../data/pattern4.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)
		with open('/Users/WANGYunzhe/Desktop/Journal/program/graph_generator/data/pattern/pattern4.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(links)





# g_draw = nx.Graph()
# for link in links:
# 	g_draw.add_edge(link[0], link[1])
# nx.draw(g_draw)
# plt.show()

