from flask import Flask, render_template, request, redirect, url_for
import funtions as f
import json
import psycopg2
from datetime import datetime
app = Flask(__name__)


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


@app.route("/inserIntoDatabase", methods=['GET', 'POST'])
def add_data():
    req = request.get_json()
    support_id = req['support_id']
    customer_id = req['customer_id']
    # task_id = req['task-id']
    task = req['task']
    body = req['body']
    description = req['description']
    task_id = req['task_id']
    status = req['status']
    create_date = str(datetime.now().date())
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="service_request",
            user="postgres",
            password="12345678",
            port = 8080
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(
            f"INSERT INTO requests (task_id, customer_id, support_id, task, body, description, status, create_date) VALUES ('{task_id}','{customer_id}', {support_id},'{task}', '{body} ','{description}','{status}', '{create_date}');",
        )
        # cursor.execute("SELECT * FROM requests;")
        # rows = cursor.fetchall()
        # print(len(rows))
        # for i in rows:
        #     print(i)
        return "Data added successfully"
    
    except Exception as error:
        return f"Error while adding data to database: {error}"
    finally:
        cursor.close()
        conn.close()

        
@app.route("/getDataFromDatabase")
def getDataFromDatabase():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="service_request",
            user="postgres",
            password="12345678",
            port = 8080
        )
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM requests;")
        rows = cursor.fetchall()
        print(len(rows))
        for i in rows:
            print(i)
        
        return "Data added successfully"
    
    except Exception as error:
        return f"Error while adding data to database: {error}"
    finally:
        cursor.close()
        conn.close()
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
