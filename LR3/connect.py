#!/usr/bin/python
import psycopg2
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    global conn
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        print('Database name: ', params["database"])
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
def disconnect():
    if conn is not None:
        conn.close()
        print('Database connection closed.')


if __name__ == '__main__':
    connect()
    disconnect()
