from decouple import config
from psycopg2 import pool,Error
class dbConn:
    def getConnPool():
        try:
            conn_pool = pool.SimpleConnectionPool(
                minconn=config('MINCONN'),
                maxconn=config('MAXCONN'),
                host=config('HOST'),
                database=config('DATABASE'),
                user=config('USER'),       
                password=config('PASSWORD'),
                port=5432,
                )
            print("connected to DB 👍")
            return conn_pool
        except (Error) as error:
            print(str(error))