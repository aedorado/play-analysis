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


	'''for genre in meta_map_genre_id :
		for app_id in meta_map_genre_id[genre] :
			#app_name = meta_map_genre_name[app_id]
			#print genre
			#print meta_map[app_id]
			#print meta_map_genre_name[app_id]
			app_arr  = filter(lambda w: not w in s,	meta_map_genre_name[app_id].split())
			for elem in app_arr :
				find = p.search(elem)
				if find == None :
					continue

				elem = find.group(1)
				wrd = stemmer.stem(elem)
				if genre in overlap :
					if wrd in overlap[genre] :
						overlap[genre][wrd] += [app_id]
					else :
						overlap[genre].update({wrd : [app_id]})
				else :
					overlap.update({genre : {wrd : [app_id]}})

	#print overlap

	result = ""
	result_inline = ""

	for genre in overlap :
		print genre
		result += genre + ' : \n'
		for wrd in overlap[genre] :
			if len(overlap[genre][wrd]) < 10 :
				continue
			#print "yes"
			result_inline = '\t\t'
			result += '\t' + wrd + ' : \n'
			for app_id in overlap[genre][wrd] :
				result += result_inline + meta_map[app_id] + '\n'''
	
	#print all_edges[0:100]
	#print all_meta[0:10]

	for edge in all_edges :

		if not edge[0] in meta_map_rev or not edge[1] in meta_map_rev :
			continue

		if meta_map_rev[edge[1]] in meta_map_app_edge_to_genre :
			if meta_map_id_genre[meta_map_rev[edge[0]]] in meta_map_app_edge_to_genre[meta_map_rev[edge[1]]] :
				pass
			else :
				meta_map_app_edge_to_genre[meta_map_rev[edge[1]]] += [meta_map_id_genre[meta_map_rev[edge[0]]]]
		else :
			meta_map_app_edge_to_genre.update({meta_map_rev[edge[1]] : [meta_map_id_genre[meta_map_rev[edge[0]]]]})
	
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
	result_final = {}
	#print centrality

	count = 0
	lower = 10
	upper = 210
	step = 10

	for i in range(lower, upper, step) :
		result2 = {}
		centrality_subset = set(centrality[:i])

		for connectedness in result :
			#result2.update({connectedness : [x for x in list(set(result[connectedness]) & centrality_subset)]})
			temp_l = list(set(result[connectedness]) & centrality_subset)
			#print  temp_l
			result2.update({connectedness : [meta_map[x] for x in temp_l]})
		result_final.update({i : result2})

		for connectedness in result2 :
			print("conn = %d : len = %d" %(connectedness, len(result2[connectedness])))


	#print result2

	#f.write(result)
	#f.close()
	with open('output_connected.txt', 'w') as outfile:
		json.dump(result_final, outfile, indent = 2)


def main() :
	global centrality

	create_file.mode()
	centrality = read_file('myfile.csv')
	print sub_community()	

if __name__ == "__main__":
	main()
