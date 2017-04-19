import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB

def mode(genre):
	db = DB('../db/play.db')
	f = open(genre + '.txt', 'w')
	all_meta = db.qry('SELECT * FROM metadata WHERE genre = \'' + genre + '\'')
	
	meta_map = {}
	meta_map_rev = {}
	count = 0
	for meta in all_meta:
		meta_map[count] = meta[0]
		meta_map_rev[meta[0]] = count
		count = count + 1

	f.write("*Vertices " + str(len(all_meta)) + "\n")
	for key in meta_map.keys():
		f.write(str(key) + " " + "\"" + meta_map[key] + "\"\n")

	f.write("*Arcs\n")
	all_cits = db.select_all('edges')
	for edge in all_cits:
		try:
			if (edge[0] in meta_map_rev) and (edge[1] in meta_map_rev):
				f.write(str(meta_map_rev[edge[0]]) + ' ' + str(meta_map_rev[edge[1]]) + '\n')
			# f.write(str(cit[0]) + ' ' + str(cit[1]) + '\n')
			# print meta_map_rev[cit[1]]
			# print (str(meta_map_rev[cit[0]]) + ' ' + str(meta_map_rev[cit[1]]) + '\n')
		except Exception:
			pass
	f.close()

	
if __name__ == "__main__":
	print mode(sys.argv[1])