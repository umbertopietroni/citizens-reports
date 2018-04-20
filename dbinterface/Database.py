#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    #import MySQLdb
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb.cursors
except ImportError:
    print("Database: MySQLdb module not installed")
    exit()

try:
    from connection_parameters import *
except ImportError:
    print("Database: configuration file not found")
    exit()

from classes import *


class Database:
    """Singleton class representing database connection"""

    __cursor = None

    def __connect():
        try:
            db = MySQLdb.connect(
                host=DBHOST,
                user=DBUSER,
                passwd=DBPASW,
                db=DBNAME,
                cursorclass=MySQLdb.cursors.DictCursor
            )
            return db.cursor()
        except MySQLdb.Error as e:
            print("Database connection failed: " + str(e))
            exit()

    @staticmethod
    def getCursor():
        if Database.__cursor is None:
            Database.__cursor = Database.__connect()
        return Database.__cursor



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

        c = Database.getCursor()
        c.execute(sql)
        db_user_id = getUserIdByChannelMsgId(issue.getUserId(), issue.getInfo("channel"))


    sql = """insert into issues( datetime, 
                                user_id, msg_id,
                                latitude, longitude,
                                channel, text,
                                category, status,
                                classification_dict)
                values("{}", "{}", "{}", "{}","{}", "{}", "{}", "{}","{}", "{}")""".format(issue.getInfo("datetime"),db_user_id,issue.getInfo("msg_id"), issue.getInfo("latitude"),issue.getInfo("longitude"),issue.getInfo("channel"),
                                                issue.getInfo("text"),issue.getInfo("category"),issue.getInfo("status"),issue.getInfo("classification_dict"))

    c = Database.getCursor()
    c.execute(sql)
    

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
        c = Database.getCursor()
        c.execute(sql)

    # save user info

def getUserIdByChannelMsgId(user_id, channel):
    sql = """select id 
			 from users
			 where user_id = '{}'
			 and channel = '{}'
			""".format(user_id, channel)
    # print(sql)
    c = Database.getCursor()
    c.execute(sql)
    rows = c.fetchall()
    # print(t)
    if not rows:
        return ""
    return rows[0]["id"]

def getIssueIdByUserIdMsgId(user_id, msg_id):
    sql = """select id 
			 from issues
			 where user_id = '{}'
			 and msg_id = '{}'
			""".format(user_id, msg_id)
    # print(sql)
    c = Database.getCursor()
    c.execute(sql)
    rows = c.fetchall()
    # print(t)
    if not rows:
        return ""
    return rows[0]["id"]

   
