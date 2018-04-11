#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import MySQLdb
    import MySQLdb.cursors
except ImportError:
    print("Database: MySQLdb module not installed")
    exit()

try:
    from config import *
except ImportError:
    print("Database: configuration file not found")
    exit()


class Database:
    """Singleton class representing database connection"""

    __cursor = None

    def __connect():
        try:
            db = MySQLdb.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASW,
                db=DB_NAME,
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
