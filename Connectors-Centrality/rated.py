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

import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB


def create():
	db = DB('../db/play.db')
	#f = open('rating.txt', 'w')
	all_meta = db.qry('select metadata.id, genre, (one + two * 2 + three * 3 + four * 4 + five * 5.0)/(one + two + three + four + five) as avgr, (one + two + three + four + five) as numr from metadata, rating WHERE metadata.id=rating.id ORDER BY (avgr * numr) DESC;')
	
	count = 0
	total = 2000

	all_meta_2 = db.select_all('metadata')

	temp_dic = {}

	for meta in all_meta_2 :
		temp_dic.update({meta[0] : count})
		count += 1

	count = 0
	rating_desc = []

	#extracting top 2000 rated app
	for meta in all_meta:
		count += 1
		if count <= total :
			rating_desc += [temp_dic[meta[0]]]
		#f.write('"' + meta[0] + '"' + ' "' + meta[1] + '" ' + str(meta[2]) + ' ' + str(meta[3]) + '\n')
		count = count + 1

	#f.close()

	return rating_desc


def read_file(filename) :
	fHandle = open(filename, 'r')
	data = fHandle.read()
	fHandle.close()

	top_k_centrality = 2000

	centrality = {}
	for line in data.split('\n') :
		if (line.strip() == '') :
			continue

		arr = line.split(',')
		centrality.update({int(arr[0]) : float(arr[2])})

	#print centrality

	sorted_centrality = sorted(centrality.items(), key=operator.itemgetter(1), reverse = True)

	centrality = []

	#print sorted_centrality

	count = -1

	# extracting top 2000  apps with highest centrality
	for elem in sorted_centrality :
		count += 1
		if count < top_k_centrality :
			centrality += [elem[0]]

	return centrality


def sub_community():
	global centrality

	db = DB('../db/play.db')
	#f = open('myfile', 'w')
	all_meta = db.select_all('metadata')
	all_edges = db.select_all('edges')
	p = re.compile("(([A-Za-z])\w+)")
	
	#print all_meta
	#stemmer = SnowballStemmer("english")
	stemmer =  LancasterStemmer()
	
	meta_map = {}
	meta_map_rev = {}
	meta_map_genre_id = {}
	meta_map_id_genre = {}
	#meta_map_id_name = {}
	meta_map_genre_name = {}

	meta_map_app_edge_to_genre = {}
	overlap = {}

	count = 0
	for meta in all_meta:
		meta_map[count] = meta[0]
		meta_map_rev[meta[0]] = count
		if not meta[3] in meta_map_genre_id :
			meta_map_genre_id.update({meta[3] : [count]})
		else :
			meta_map_genre_id[meta[3]] += [count]

		meta_map_genre_name.update({count : meta[1]})
		meta_map_id_genre.update({count : meta[3]})
		
		count = count + 1



	for edge in all_edges :

		if not edge[0] in meta_map_rev or not edge[1] in meta_map_rev :
			continue

		if meta_map_rev[edge[0]] in meta_map_app_edge_to_genre :
			if meta_map_id_genre[meta_map_rev[edge[1]]] in meta_map_app_edge_to_genre[meta_map_rev[edge[0]]] :
				pass
			else :
				meta_map_app_edge_to_genre[meta_map_rev[edge[0]]] += [meta_map_id_genre[meta_map_rev[edge[1]]]]
		else :
			meta_map_app_edge_to_genre.update({meta_map_rev[edge[0]] : [meta_map_id_genre[meta_map_rev[edge[1]]]]})
	
	result = {}
	'''
	for app_id in meta_map_app_edge_to_genre :
		result.update({meta_map[app_id] : meta_map_app_edge_to_genre[app_id]})
	'''

	for app_id in meta_map_app_edge_to_genre :
		#result.update({app_id : len(meta_map_app_edge_to_genre[app_id])})

		if len(meta_map_app_edge_to_genre[app_id]) in result :
			result[len(meta_map_app_edge_to_genre[app_id])] += [app_id]
		else  :
			result.update({len(meta_map_app_edge_to_genre[app_id]) : [app_id]})

	#print centrality[200]

	result2 = {}

	#print centrality

	for i in range(100, 1000, 100) :
		centrality_subset = set(centrality[:i])

		for connectedness in result :
			result2.update({connectedness : set(result[connectedness]) & centrality_subset})

		for connectedness in result2 :
			print("conn = %d : len = %d" %(connectedness, len(result2[connectedness])))


	#print result2

	#f.write(result)
	#f.close()
	'''with open('output.txt', 'w') as outfile:
		json.dump(result2, outfile, indent = 2)'''


def main() :
	global centrality

	create_file.mode()
	centrality = create()
	print sub_community()	

if __name__ == "__main__":
	main()
