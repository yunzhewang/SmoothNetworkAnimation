# utilities
import json
import csv

class util:
	"""docstring for utility"""
	def __init__(self):
		print('utility initialized!')
		
	# JSON 2 CSV
	def json2csv(self, filename):
		with open(filename) as fr:
			data = json.load(fr)

			csv_data = []
			for link in data:
				csv_data.append(link)

		with open('../data/graph.csv', 'wb') as fw:
			writer = csv.writer(fw)
			writer.writerow(['source', 'target', 'value'])
			writer.writerows(csv_data)