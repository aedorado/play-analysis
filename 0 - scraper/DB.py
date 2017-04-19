import sqlite3 as db
from URL import URL

class DB:

    def __init__(self, db_name):
        self.conn = db.connect(db_name)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
        
    def create_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS link(id varchar(256)  primary key, url varchar(256), processed boolean)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS metadata(id VARCHAR(256) primary key, name VARCHAR(64), org VARCHAR(64), genre VARCHAR(64), installs VARCHAR(64))')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS rating(id VARCHAR(256) primary key, one INTEGER, two INTEGER, three INTEGER, four INTEGER, five INTEGER)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS edges(id_f VARCHAR(256), id_t VARCHAR(256), PRIMARY KEY(id_f, id_t))')
        
    def add_seeds(self, seed_file):
        with open(seed_file) as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            url = URL(line)
            app_id = url.get_qs('id')
            if not self.exists('link', url.get_qs('id')):
                self.insert("link", {
                            "id": url.get_qs('id'),
                            "url": line,
                            "processed": 0
                })

    def insert(self, tablename, data):
        if (tablename == 'link'):
            query = 'INSERT INTO link VALUES (?, ?, 0)'
            self.cursor.execute(query, (data['id'], data['url']))
            self.conn.commit()
        elif (tablename == 'metadata'):
            query = 'INSERT INTO metadata VALUES (?, ?, ?, ?, ?)'
            self.cursor.execute(query, (data['id'], data['name'], data['org'], data['genre'], data['installs']))
            self.conn.commit()
        elif (tablename == 'rating'):
            query = 'INSERT INTO rating VALUES (?, ?, ?, ?, ?, ?)'
            self.cursor.execute(query, (data['id'], data[1], data[2], data[3], data[4], data[5]))
            self.conn.commit()
        elif (tablename == 'edges'):
            query = 'INSERT INTO edges VALUES (?, ?)'
            self.cursor.execute(query, (data['id_f'], data['id_t']))
            self.conn.commit()
            
    def exists(self, tablename, key):
        if (tablename == 'link'):
            query = 'SELECT id FROM link WHERE id=?'
            self.cursor.execute(query, (key, ))
            allrows = self.cursor.fetchall()
            return (len(allrows) == 1)
        elif (tablename == 'metadata'):
            query = 'SELECT id FROM metadata WHERE id=?'
            self.cursor.execute(query, (key, ))
            allrows = self.cursor.fetchall()
            return (len(allrows) == 1)
        elif (tablename == 'citations'):
            query = 'SELECT COUNT(*) FROM citations WHERE doi_f = ? AND doi_t = ?'
            self.cursor.execute(query, (key['doi_f'], key['doi_t']))
            count = self.cursor.fetchall()[0][0]
            return (count == 1)
    
    def update_link(self, aid, status):
        query = 'UPDATE link SET processed = ? WHERE id = ?'
        self.cursor.execute(query, (status, aid, ))
        self.conn.commit()
        
    def count_unpr(self):
        query = 'SELECT COUNT(*) FROM link WHERE processed = 0'
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]
    
    def get_unpr(self):
        query = 'SELECT * FROM link where processed = 0 LIMIT 0,1'
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][1]
        
    def select_all(self, table):
        self.cursor.execute('SELECT * FROM ' + table)
        return self.cursor.fetchall()