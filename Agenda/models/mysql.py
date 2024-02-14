import MySQLdb

host = "localhost"
user = "root"
password = "root"
db = "agenda"
port = 3306

con = MySQLdb.connect(host, user, password, db, port)
c = con.cursor()

def select(campos, tables, where=None):
    global c
    consulta = "SELECT " + campos + " FROM " + tables
    if where:
        consulta = consulta + " WHERE " + where
    c.execute(consulta)
    return c.fetchall()

def insert(values, table, campos=None):
    global c, con
    query = "INSERT INTO " + table
    if campos:
        query = query + " (" + campos + ")"
    query = query + " VALUES (" + ",".join(values) + ")"
    c.execute(query)
    con.commit()
def update(sets, table, where=None):
    global c, con
    query = "UPDATE " + table 
    query = query + " SET " + ",".join([field + " = '" + value + "'" for field, value in sets.items()])
    if (where):
        query = query + " WHERE " + where
    c.execute(query)
    con.commit()
    



def delete(table,where):
	global c,con
	query = " DELETE FROM " + table + " WHERE	" + where
	c.execute(query)
	con.commit()
