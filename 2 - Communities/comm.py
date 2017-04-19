import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB

def mode():
	db = DB('../db/play.db')
	f = open('myfile', 'w')
	all_meta = db.select_all('metadata')
	
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
			f.write(str(meta_map_rev[edge[0]]) + ' ' + str(meta_map_rev[edge[1]]) + '\n')
			# f.write(str(cit[0]) + ' ' + str(cit[1]) + '\n')
			# print meta_map_rev[cit[1]]
			# print (str(meta_map_rev[cit[0]]) + ' ' + str(meta_map_rev[cit[1]]) + '\n')
		except Exception:
			pass
	f.close()

	
if __name__ == "__main__":
	print mode()