# import MySQLdb
import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb.cursors
from connection_parameters import *


def makesql(sql):
    db = MySQLdb.connect(host=DBHOST,
                         user=DBUSER,
                         passwd=DBPASW,
                         db=DBNAME,
                         cursorclass=MySQLdb.cursors.DictCursor)

    c = db.cursor()
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
    # print(sql)
    t = makesql(sql)
    # print(t)
    if not t:
        return ""
    return t[0]["id"]


def getUserIdByChannelMsgId(user_id, channel):
    sql = """select id 
			 from users
			 where user_id = '{}'
			 and channel = '{}'
			""".format(user_id, channel)
    # print(sql)
    t = makesql(sql)
    # print(t)
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
   

    # SAVE NEW
    info = issue.getInfo()
    info.update(issue.getInfo()["position"])
    info['category'] = issue.getCategory()
    info['status'] = 0
    info['classification_dict'] = issue.getClassificationDict()

    db_user_id = getUserIdByChannelMsgId(issue.getUserId(), issue.getInfo("channel"))
    if not db_user_id:
        sql = """insert into users(user_id, channel, phone_number, username,first_name,last_name) 
                values( "{}", "{}", "{}", "{}","{}","{}")""".format(issue.getUserId(),
                                                          issue.getInfo("channel"),
                                                          issue.getInfo("phone_number"),
                                                          issue.getInfo("username"),
                                                          issue.getInfo("firstname"),
                                                          issue.getInfo("lastname"))

        makesql(sql)
        db_user_id = getUserIdByChannelMsgId(issue.getUserId(), issue.getInfo("channel"))


    sql = """insert into issues( datetime, 
                                user_id, msg_id,
                                latitude, longitude,
                                channel, text,
                                category, status,
                                classification_dict)
                values("{}", "{}", "{}", "{}","{}", "{}", "{}", "{}","{}", "{}")""".format(issue.getInfo("datetime"),db_user_id,issue.getInfo("msg_id"), issue.getInfo("latitude"),issue.getInfo("longitude"),issue.getInfo("channel"),
                                                issue.getInfo("text"),issue.getInfo("category"),issue.getInfo("status"),issue.getInfo("classification_dict"))

    makesql(sql)
    

    db_issue_id = getIssueIdByUserIdMsgId(db_user_id, issue.getMsgId())

    # SAVE ALL ISSUE IMAGES
    #sql = "delete from images where issue_id = '{}'".format(db_issue_id)
    #makesql(sql)
    for i in issue.getImages():
        sql = """insert into images(issue_id,filename, category, classification_dict)
                    values("{}", "{}", "{}", "{}")""".format(db_issue_id,
                                                             i.getFilename(),
                                                             i.getCategory(),
                                                             str(i.getClassificationDict()))
        makesql(sql)

    # save user info


