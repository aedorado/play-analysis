from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
s=set(stopwords.words('english'))
import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB
import re
import json	
import create_file
import operator

#filter(lambda w: not w in s,txt.split())

centrality = ()

def read_file(filename) :
	with open(filename) as json_data:
		d = json.load(json_data)
	
	return d



def process(connector, connected):
	global centrality

	# class wise overlap

	final_result = {}
	final_result_2 = {}

	print "Non-Clubbed :: \n"
	for top in sorted([int(x) for x in connector]) :
		top = str(top)
		result = []
		result2 = []
		for outdegree in sorted(connector[top]) :
			if outdegree == '1' :
				continue

			result = set(connector[top][outdegree]) & set(connected[top][outdegree])

			if top in final_result :
				if not outdegree in final_result[top] :
					final_result[top].update({outdegree : list(result)})
			else :
				final_result.update({top : {outdegree : list(result)}}) 

			print("top = %s outdegree =  %s len = %d" %(top, outdegree, len(result)))


	result = []
	result2 = []

	print "Clubbed :: \n"
	for top in sorted([int(x) for x in connector]) :
		top = str(top)
		result = []
		result2 = []
		for outdegree in connector[top] :
			if outdegree == '1' :
				continue
			result += connector[top][outdegree]
			result2 += connected[top][outdegree]

		result = set(result) & set(result2)
		print(top + " : " + str(len(result)))
		final_result_2.update({top : list(result)})


	output1 = 'interclass.txt'
	output2 = 'clubbed_interclass.txt'

	with open(output1, 'w') as outfile:
		json.dump(final_result, outfile, indent = 2)

	with open(output2, 'w') as outfile:
		json.dump(final_result_2, outfile, indent = 2)


def main() :
	global centrality

	create_file.mode()
	data1 = read_file('output_connector.txt')
	data2 = read_file('output_connected.txt')
	process(data1, data2)	

if __name__ == "__main__":
	main()
