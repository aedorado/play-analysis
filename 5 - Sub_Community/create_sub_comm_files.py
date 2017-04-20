from nltk.stem import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
s=set(stopwords.words('english'))
import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)
#filter(lambda w: not w in s,txt.split())

def sub_community():
	db = DB('../db/play.db')
	# f = open('otherfile', 'w')
	all_meta = db.select_all('metadata')
	all_cit = db.qry("select id_f, GROUP_CONCAT(id_t) from edges GROUP BY id_f")
	p = re.compile("(([A-Za-z])\w+)")
	
	#print all_meta
	#stemmer = SnowballStemmer("english")
	stemmer =  LancasterStemmer()
	cit_map = {}
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

	print 'Building citation map now.'
	for cit in all_cit:
		# pp.pprint(cit[0])
		# pp.pprint(meta_map_rev[cit[0]])
		tolist = list(cit[1].split(','))
		# print tolist
		tolist_mapped = []
		for item in tolist:
			if item in meta_map_rev:
				tolist_mapped.append(meta_map_rev[item])
		# print tolist_mapped
		cit_map[meta_map_rev[cit[0]]] = tolist_mapped
	# pp.pprint(cit_map)
	print 'Finished citation map now.'

	for genre in meta_map_genre_id:
		for app_id in meta_map_genre_id[genre]:
			#app_name = meta_map_genre_name[app_id]
			print genre
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

	print 'Overlap calculated.'
	# pp.pprint(overlap)

	result = ""
	result_inline = ""
	filenames = []

	for genre in overlap:
		print genre
		# result += genre + ' : \n'
		for wrd in overlap[genre]:
			if len(overlap[genre][wrd]) < 50:
				continue
			print '->\t' + wrd
			newfilename = 'lemma_cat_folder/' + genre + '_' + wrd
			filenames.append(newfilename)
			f = open(newfilename, 'w')
			f.write("*Vertices " + str(len(overlap[genre][wrd])) + "\n")
			for app_id in overlap[genre][wrd]:
				f.write(str(app_id) + " " + "\"" + meta_map[app_id] + "\"\n")
			f.write("*Arcs\n")
			for app_id in overlap[genre][wrd]:
				try:
					for cit in cit_map[app_id]:
						if cit in overlap[genre][wrd]:
							f.write(str(app_id) + ' ' + str(cit) + '\n')
				except Exception:
					print 'Exception for ' + meta_map[app_id]
		# 	#print "yes"
		# 	result_inline = '\t\t'
		# 	result += '\t' + wrd + ' : \n'
		# 	for app_id in overlap[genre][wrd] :
		# 		result += result_inline + meta_map[app_id] + '\n'
			f.close()


	# f.write(result)
	# f.close()
	# print pp.pprint(filenames)

	
if __name__ == "__main__":
	sub_community()
