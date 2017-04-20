import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB

def mode():
	db = DB('../db/play.db')
	f = open('myfile.txt', 'w')
	all_meta = db.select_all('metadata')
	
	meta_map = {}
	meta_map_rev = {}
	count = 0
	for meta in all_meta:
		meta_map[count] = meta[0]
		meta_map_rev[meta[0]] = count
		count = count + 1

	f.write("graph\n[\n")
	for key in meta_map.keys():
		f.write("\tnode\n\t[\n\t\tid " + str(key) + "\n\t]\n")
	# f.write("*Arcs\n")
	all_cits = db.select_all('edges')
	for edge in all_cits:
		try:
			f.write("\tedge\n\t\tsource " + str(meta_map_rev[edge[0]]) + '\n\t\ttarget ' + str(meta_map_rev[edge[1]]) + '\n\t\tvalue 1\n\t]\n')
			# f.write(str(cit[0]) + ' ' + str(cit[1]) + '\n')
			# print meta_map_rev[cit[1]]
			# print (str(meta_map_rev[cit[0]]) + ' ' + str(meta_map_rev[cit[1]]) + '\n')
		except Exception:
			pass
	f.write("]")
	f.close()

	print(len(all_cits))

	
if __name__ == "__main__":
	print mode()