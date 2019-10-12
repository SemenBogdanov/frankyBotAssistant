import os
import psycopg2

DATABASE_URL = 'postgres://ojvgsnmthwqndk:8bb9342a9aab831772134aa786eb8ee1dcd931cb5e80fd4884519c8d553c07c1@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dd4ctr1dopnkc7'

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

