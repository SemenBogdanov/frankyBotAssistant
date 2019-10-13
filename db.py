import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

def checkUser(chatId):
	sql="select username from usersbot as u where u.messagechatid='" + str(chatId) + "'"
	try:
	    cur = conn.cursor()
	    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # by column name
	    cur.execute(sql)
	    data = cur.fetchall()
	    return data
	    
	except psycopg2.Error as err:
	    print("Query error: {}".format(err))

def addUser(ans):
	print(ans.chat.id)
	sql="insert into usersbot (username, messagechatid, tlgusername) \
	values ('" + ans.text + "','" + str(ans.chat.id) + "','" + str(ans.chat.username) + "')"
	print(sql)
	try:
	    cur = conn.cursor()
	    # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) # by column name
	    cur.execute(sql)
	    conn.commit()
	    return True
	except psycopg2.Error as err:
	    print("Query error: {}".format(err))
		

