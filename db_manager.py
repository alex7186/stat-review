from sqlite3 import connect as sqlite3_connect, Error
from datetime import datetime

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3_connect(db_file, check_same_thread=False)
        # print(sqlite3.version)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)

    except Error as e:
        print(e)
    return cursor

def connect(
    db_file='./downloads.db'):
    
    sql_create_table = """ 
    CREATE TABLE IF NOT EXISTS downloads 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variant text,
        distr_type text,
        download_date text
    );"""



    connection = create_connection(db_file)

    if connection is not None:
        cursor = create_table(connection, sql_create_table)
        connection.commit()


    return connection, cursor


def add_log(
    connection, cursor, variant, distr_type):
    
        download_date = datetime.now().strftime('%Y.%m.%d %H:%M')

        sql_command = f"""INSERT INTO downloads (variant, distr_type, download_date)
            VALUES 
            (
            "{variant}", "{distr_type}", "{download_date}"
            )
        """
    
        cursor.execute(sql_command)
        connection.commit()

def get_latest_log(
    connection, cursor):

    sql_command = "select variant, download_date from downloads order by download_date limit 5"

    return cursor.execute(sql_command).fetchall()

connection, cursor = connect()