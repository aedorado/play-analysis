import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB
import pprint
pp = pprint.PrettyPrinter(indent=4)

def genre_wise_mode():
	db = DB('../db/play.db')
	all_rows = db.qry('SELECT * FROM metadata, rating WHERE metadata.id = rating.id')

	mode_map = {}
	for row in all_rows:
		if row[3] in mode_map:
			mode_map[row[3]][1] += row[6]
			mode_map[row[3]][2] += row[7]
			mode_map[row[3]][3] += row[8]
			mode_map[row[3]][4] += row[9]
			mode_map[row[3]][5] += row[10]
		else:
			mode_map[row[3]] = [0, 0, 0, 0, 0, 0]
	pp.pprint(mode_map)

	for genre in mode_map.keys():
		karr = mode_map[genre]
		print genre + "\tMode: " + str(karr.index(max(karr)))

def other_mode():
	db = DB('../db/play.db')
	all_rows = db.qry('SELECT * FROM metadata, rating WHERE metadata.id = rating.id')

	genre_map = {}
	for row in all_rows:
		if row[3] in genre_map:
			row_slice = list(row[6:])
			max_index = row_slice.index(max(row_slice))
			genre_map[row[3]][max_index + 1] = genre_map[row[3]][max_index + 1] + 1
		else:
			genre_map[row[3]] = [0, 0, 0, 0, 0, 0] 

	pp.pprint(genre_map)
	for genre in genre_map.keys():
		karr = genre_map[genre]
		print genre + "\tMode: " + str(karr.index(max(karr)))

if __name__ == "__main__":
	# print genre_wise_mode()
	print other_mode()