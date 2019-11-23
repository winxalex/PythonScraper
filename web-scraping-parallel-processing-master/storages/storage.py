__author__ = 'alex winx'

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)





#Insert record into table
def data_entry(conn, insert, record):
    try:
        c = conn.cursor()
        c.execute(insert,
                  (record[0], record[1], record[2], record[3]))
        conn.commit()
    except Error as e:
        print(e)


def data_print(conn,table_name):
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM "+table_name)
        rows = c.fetchall()
        for row in rows:
            print(row)

    except Error as e:
        print(e)


