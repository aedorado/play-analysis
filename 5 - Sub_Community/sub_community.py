from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
s=set(stopwords.words('english'))
import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB
import re

#filter(lambda w: not w in s,txt.split())

def sub_community():
	db = DB('../db/play.db')
	f = open('myfile', 'w')
	all_meta = db.select_all('metadata')
	p = re.compile("(([A-Za-z])\w+)")
	
	#print all_meta
	#stemmer = SnowballStemmer("english")
	stemmer =  LancasterStemmer()
	
	meta_map = {}
	meta_map_rev = {}
	meta_map_genre_id = {}
	meta_map_id_name = {}
	meta_map_genre_name = {}
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
		
		count = count + 1


	for genre in meta_map_genre_id :
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
				result += result_inline + meta_map[app_id] + '\n'


	f.write(result)
	f.close()

	
if __name__ == "__main__":
	print sub_community()
