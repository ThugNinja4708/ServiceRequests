from flask import Flask, render_template, request, redirect, url_for
import funtions as f
import json
import psycopg2
import psycopg2.pool

from datetime import datetime
app = Flask(__name__)

conn_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host="localhost",
    database="service_request",
    user="postgres",
    password="12345678",
    port=8080
)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/getAllTenants', methods=['GET', 'POST'])
def getAllTenants():
    res = f.getALLTenants()
    print(res)
    return {"list of tenants": res}


@app.route('/updatePublicIPs', methods=['GET', 'POST'])
def updatePublicIPs():
    req = request.get_json()
    res = f.updatePublicIPs(req['customerId'], req['IPs'])
    print(res)
    data = {"message": res.get('svcMessage'), "status": res.get('status')}
    return data


@app.route('/updatePSMcertificates', methods=['GET', 'POST'])
def updatePSMcertificates():
    response = {}
    files = request.files.getlist("psmFiles")
    data = json.loads(request.form["data"])
    res = f.installPSMCertificate(data["customerId"], files)
    if type(res) == list:
        res = res[0]
        response["status"] = res["status"]

    else:
        response["status"] = res["svcMessage"]

    print(response)
    return response


@app.route('/installLDAPcertificates', methods=['GET', 'POST'])
def updateLDAPcertificates():
    response = {}
    files = request.files.getlist("ldapFiles")
    data = json.loads(request.form["data"])
    res = f.installLDAPCertificate(data["customerId"], files)
    if type(res) == list:
        res = res[0]
        response["status"] = res["status"]

    else:
        response["status"] = res["svcMessage"]
    print(response)
    return response


@app.route("/getCustomerPublicIPs", methods=['GET', 'POST'])
def getIPs():
    req = request.get_json()

    res = f.getPublicIPs(req["customerId"])
    print(res)
    return {"list of public IPs": res}


@app.route("/getTaskStatus", methods=['GET', 'POST'])
def getTaskStatus():
    req = request.get_json()
    res = f.getTaskStatus(req["customerId"])
    latestTask = res[0]
    res = {"status": latestTask.get("status"), "flowProgress": latestTask.get(
        "params").get("flowProgress")}
    return res

@app.route("/getCustomerName", methods=["POST"])
def getCustomerName():
    req = request.get_json()
    customer_id = req["customer_id"]
    customer_name = f.getCustomerName(customer_id)
    return customer_name



### Database operations ###
@app.route("/inserIntoDatabase", methods=['GET', 'POST'])
def add_data():
    req = request.get_json()
    support_id = req['support_id']
    customer_id = req['customer_id']
    # task_id = req['task-id']
    task = req['task']

    body = open("./To-do.txt", "rb").read()
    description = req['description']
    task_id = req['task_id']
    status = req['status']
    create_date = str(datetime.now().date())
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                queryToInsertRequest ="INSERT INTO requests (customer_id, support_id, task, body, description, status, create_date) VALUES ((%s),(%s),(%s), (%s),(%s),(%s),(%s));"
                cursor.execute(queryToInsertRequest, (customer_id, support_id, task, psycopg2.Binary(body), description, status, create_date))

            return "Data added successfully"
    
    except Exception as error:
        return f"Error while adding data to database: {error}"

@app.route("/getDataFromDatabase", methods=["GET", "POST"])
def getDataFromDatabase():
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                querytoretrieveRequest = "SELECT body FROM requests;"
                cursor.execute(querytoretrieveRequest)
                rows = cursor.fetchone()[0]
                # print("No. of rows", len(rows))
                # for i in rows:
                #     print(i[4])
                print(str(rows))
                return "Data added successfully"
        
    except Exception as error:
        return f"Error while adding data to database: {error}"

@app.route("/verifyLogin", methods=["POST"])
def verifyLogin():
    req = request.get_json()
    user_name = req["user_name"]
    password = req["password"] #decode the password
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            # cursor = conn.cursor()
            with conn.cursor() as cursor:
                selectQuerToGetUserDetails = f"SELECT user_name, password FROM users WHERE user_name = {user_name} AND password = {password}"
                cursor.execute(selectQuerToGetUserDetails)
                noOfRows = cursor.rowcount

                if noOfRows == 1:
                    return "found"
                else:
                    return "user not found"
        
        
    except(Exception) as error:
        print(error)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
