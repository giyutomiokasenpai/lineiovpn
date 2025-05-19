import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname='giyu',
        user='giyu',
        password='giyu',
        host='localhost',
        port='5432'
    )

async def create_connection():
    connect = connect_db()
    cursor = connect.cursor()
    return connect, cursor

async def close_connection(connect, cursor):
    connect.close()
    cursor.close()