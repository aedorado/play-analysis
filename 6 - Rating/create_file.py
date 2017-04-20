import sys
import os
sys.path.insert(0, os.path.abspath('../commons'))
from DB import DB

def create():
	db = DB('../db/play.db')
	f = open('rating.txt', 'w')
	all_meta = db.qry('select metadata.id, genre, (one + two * 2 + three * 3 + four * 4 + five * 5.0)/(one + two + three + four + five) as avgr, (one + two + three + four + five) as numr from metadata, rating WHERE metadata.id=rating.id ORDER BY (avgr * numr) DESC;')
	
	count = 0
	for meta in all_meta:
		f.write('"' + meta[0] + '"' + ' "' + meta[1] + '" ' + str(meta[2]) + ' ' + str(meta[3]) + '\n')
		count = count + 1

	f.close()
	
if __name__ == "__main__":
	create()