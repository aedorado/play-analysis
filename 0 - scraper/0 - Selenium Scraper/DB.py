import sqlite3 as db
from URL import URL

class DB:

    def __init__(self, db_name):
        self.conn = db.connect(db_name)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()

    def truncate_all(self):
        self.cursor.execute('DELETE FROM rating')
        self.cursor.execute('DELETE FROM link')
        self.cursor.execute('DELETE FROM metadata')
        self.cursor.execute('DELETE FROM edges')
        self.conn.commit()
        
    def create_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS link(id varchar(256)  primary key, url varchar(256), processed boolean)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS metadata(id VARCHAR(256) primary key, name VARCHAR(64), org VARCHAR(64), genre VARCHAR(64), description TEXT, installs VARCHAR(64), version VARCHAR(64), address VARCHAR(256), website VARCHAR(256), editors VARCHAR(1), permissions TEXT, tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
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
            query = 'INSERT INTO metadata (id, name, org, genre, description, installs, version, address, website, editors, permissions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            self.cursor.execute(query, (data['id'], data['name'], data['org'], data['genre'], data['description'], data['installs'], data['version'], data['address'], data['website'], data['editors'], data['permissions']))
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
        elif (tablename == 'edges'):
            query = 'SELECT COUNT(*) FROM edges WHERE id_f = ? AND id_t = ?'
            self.cursor.execute(query, (key['id_f'], key['id_t']))
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
        