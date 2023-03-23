

\c service_request
CREATE TABLE IF NOT EXISTS users(
    support_id INT PRIMARY KEY NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    typeOfUser INT NOT NULL
);
CREATE TABLE IF NOT EXISTS requests (
    task_Id SERIAL PRIMARY KEY NOT NULL,
    customer_id VARCHAR(100) NOT NULL,
    support_id  INT REFERENCES users(support_id),
    task INT NOT NULL,
    body text , --varchar(200) NOT NULL,
    -- description varchar(100) ,
    status VARCHAR(100) NOT NULL,
    error_message VARCHAR(100),
    create_date DATE NOT NULL,
    approval_date DATE,
    complete_date DATE
);

