import MySQLdb
#import pymysql
#pymysql.install_as_MySQLdb()
import MySQLdb.cursors
from connection_parameters import *

def makesql(sql):
	db=MySQLdb.connect(host=DBHOST, 
					user=DBUSER, 
					passwd=DBPASW, 
					db=DBNAME, 
					cursorclass=MySQLdb.cursors.DictCursor)

	c=db.cursor()
	c.execute(sql)
	rows = c.fetchall()
	db.commit()
	return rows

def getIssueIdByUserIdMsgId(user_id, msg_id):
	sql = """select id 
			 from issues
			 where user_id = '{}'
			 and msg_id = '{}'
			""".format(user_id, msg_id)
	#print(sql)
	t = makesql(sql)
	#print(t)
	if not t:
		return ""
	return t[0]["id"]

def getUserIdByChannelMsgId(user_id, channel):
	sql = """select id 
			 from users
			 where user_id = '{}'
			 and channel = '{}'
			""".format(user_id, channel)
	#print(sql)
	t = makesql(sql)
	#print(t)
	if not t:
		return ""
	return t[0]["id"]

def getLastInsertedId(table):
	t = makesql("select max(id) as last_insert_id from {}".format(table))
	if not t:
		return None
	else:
		return t[0]["last_insert_id"]

def saveIssue(issue):
#	print("SAVE", issue.getInfo(), issue.getImages(), issue.getClassificationDict())
	db_issue_id = getIssueIdByUserIdMsgId(issue.getUserId(), issue.getMsgId())
#	print("db_issue_id=", db_issue_id)
	
	# SAVE NEW
	info = issue.getInfo()
	info.update(issue.getInfo()["position"])
	info['category'] = issue.getCategory()
	info['status'] = "NEW"
	info['classification_dict'] = issue.getClassificationDict()
	sql = """replace into issues(id, day, time, 
								user_id, msg_id,
								latitude, longitude,
								channel, text,
								category, status,
								classification_dict)
				values("%%(db_issue_id)s", "%(date)s", "%(time)s",
						"%(user_id)s", "%(msg_id)s", 
						"%(latitude)s", "%(longitude)s", 
						"%(channel)s", "%(text)s", 
						"%(category)s", "%(status)s", 
						"%(classification_dict)s"
						)
			""" % info % vars()
#	print(sql)
	makesql(sql)
	
	if not db_issue_id:
		# recupera ultimo id 
		db_issue_id = getLastInsertedId("issues")
#		print("ID ISSUE : ", db_issue_id)
	else:
#		print("EXISTING ISSUE")
		pass
	# SAVE ALL ISSUE IMAGES 
	sql = "delete from images where issue_id = '{}'".format(db_issue_id)
	makesql(sql)
	for i in issue.getImages():
#		print(i.getFilename())
#		print(i.getClassificationDict())
#		print(i.getCategory())
#		print(i.getConfidence())
		
		sql = """insert into images(issue_id, filename, category, classification_dict)
					values("{}", "{}", "{}", "{}")""".format(db_issue_id, 
															i.getFilename(),
															i.getCategory(),
															i.getClassificationDict())
		makesql(sql)

	# save user info
	
	db_user_id = getUserIdByChannelMsgId(issue.getUserId(), issue.getInfo("channel"))
	
	sql = """replace into users(id, user_id, channel, phone_number, description) 
			values("{}", "{}", "{}", "{}", "{}")""".format(db_user_id,
															issue.getUserId(), 
															issue.getInfo("channel"),
															issue.getInfo("phone_number"),
															issue.getInfo("firstname") + " " + issue.getInfo("lastname"))
#	print(sql)
	makesql(sql)
