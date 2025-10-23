import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",      # change if you have another user
        password="microsoft@900",      # add your MySQL password
        database="my_db")
