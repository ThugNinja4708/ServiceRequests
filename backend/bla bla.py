import psycopg2
import psycopg2.pool
try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host="database-2.cuzyvnhw6wmo.ap-south-1.rds.amazonaws.com",
        database="service_request",
        user="dbManager",
        password="12345678",
        port=5432
    )

    with conn_pool.getconn() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
    task_Id SERIAL PRIMARY KEY NOT NULL,
    customer_id VARCHAR(100) NOT NULL,
    support_id  INT REFERENCES users(support_id),
    task INT NOT NULL,
    body BYTEA , --varchar(200) NOT NULL,
    description varchar(100) ,

    status VARCHAR(100) NOT NULL,
    error_message VARCHAR(100),
    create_date DATE NOT NULL,
    approval_date DATE,
    complete_date DATE
);''')
except(Exception, psycopg2.Error)as error:
    print(error)
