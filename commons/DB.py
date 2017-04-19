import sqlite3 as db

class DB:

    def __init__(self, db_name):
        self.conn = db.connect(db_name)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
        
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
        
    def select_all(self, table, col=''):
        if col == '':
            q = 'SELECT * FROM ' + table
        else:
            q = 'SELECT ' + col + ' FROM ' + table
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_table_row_col(self, table, cid, col):
        q = 'SELECT ' + col + ' FROM ' + table + ' WHERE id=\'' + cid + '\''
        self.cursor.execute(q)
        return self.cursor.fetchall()[0][0]

    def get_cit_from(self, cid):
        q = 'SELECT * FROM edges WHERE id_f = \'' + cid + '\''
        self.cursor.execute(q)
        return self.cursor.fetchall() 

# DB('../db/play.db').get_table_col('metadata', 'com.whatsapp', 'genre')