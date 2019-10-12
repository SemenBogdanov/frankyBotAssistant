import os
import psycopg2

DATABASE_URL = 'DATABASE_URL'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

sql = 'SELECT * FROM memo'
 
try:
    cur = conn.cursor()
    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # by column name
    cur.execute(sql)
    data = cur.fetchall()
except psycopg2.Error as err:
    print("Query error: {}".format(err))
    
print(data)

