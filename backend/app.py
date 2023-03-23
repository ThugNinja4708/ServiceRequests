from flask import Flask, render_template, request, redirect, url_for,jsonify
import funtions as f
import json
import psycopg2
import psycopg2.pool
import os
from datetime import datetime
from dbConn import dbConn
import time
app = Flask(__name__)
conn_pool = dbConn.getConnPool()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/getAllTenants', methods=['GET', 'POST'])
def getAllTenants():
    res = f.getALLTenants()
    # print(res)
    return {"list of tenants": res}


@app.route('/updatePublicIPs', methods=['GET', 'POST'])
def updatePublicIPs(job = None):
    req = job or request.get_json()
    # print(req['body'].split(","))
    res = f.updatePublicIPs(req['customer_id'], req['body'].split(","))
    # print("result:", res)
    data = {"message": res.get('svcMessage'), "status": res.get('status')}
    return data


@app.route('/updatePSMcertificates', methods=['GET', 'POST'])
def updatePSMcertificates(job = None):
    response = {}
    customer_id = job["customer_id"]
    files = job["body"].split(",")
    # files = request.files.getlist("psmFiles")
    # data = json.loads(request.form["data"])
    print("files",files)
    res = f.installPSMCertificate(customer_id, files)
    if type(res) == list:
        res = res[0]
        response["status"] = res["status"]

    else:
        response["status"] = res["svcMessage"]

    # print(response)
    return response


@app.route('/installLDAPcertificates', methods=['GET', 'POST'])
def updateLDAPcertificates(job = None):
    response = {}
    # files = request.files.getlist("ldapFiles")
    # data = json.loads(request.form["data"])
    customer_id = job["customer_id"]
    files = job["body"].split(",")
    res = f.installLDAPCertificate(customer_id, files)
    print(res)
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
def getTaskStatus(cust_id = None ):
    req = request.get_json()
    customer_id =  cust_id or req["customerId"] 
    print(customer_id)
    res = f.getTaskStatus(customer_id)
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


######################## Database operations ########################


@app.route("/insertIntoDatabase", methods=['GET', 'POST'])
def add_data():
    # req = request.get_json() # change this
    # req = json.loads(request.form["data"])
    support_id = request.form['support_id']
    customer_id = request.form['customer_id']
    task = request.form['task']
    # description = request.form['description']
    # task_id = request.form['task_id']
    status = request.form['status']
    path = "database_files"
    create_date = str(datetime.now().date())


    if (task == "3" or task == "4"):
        list = []
        files = request.files.getlist('body')
        for file in files:
            fileName =  str(time.time_ns()) +"_"+ file.filename
            list.append(fileName)
            file.save(path +  "\\" + fileName)
        csv_of_files = ",".join(list)
        body = csv_of_files
    else:
        body = ''.join(request.form["body"])
    print(body)


    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                queryToInsertRequest = "INSERT INTO requests (customer_id, support_id, task, body, status, create_date) VALUES ((%s),(%s),(%s),(%s),(%s),(%s));"
                cursor.execute(queryToInsertRequest, (customer_id, support_id,
                               task, body, status, create_date))

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

                rows = cursor.fetchall()
                print("No. of rows", len(rows))
                for i in rows:
                    print(str(i[0], 'utf-8'))

                return "Data added successfully"

    except Exception as error:
        return f"Error while adding data to database: {error}"


@app.route("/verifyLogin", methods=["POST"])
def verifyLogin():
    # print()
    req = request.get_json()
    response = {
        "isFound": False
    }
    user_name = req["user_name"]
    password = req["password"]  # decode the password
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            # cursor = conn.cursor()
            with conn.cursor() as cursor:
                selectQuerToGetUserDetails = f"SELECT user_name, password FROM users WHERE user_name = (%s) AND password = (%s);"
                cursor.execute(selectQuerToGetUserDetails,
                               (user_name, password))
                noOfRows = cursor.rowcount
                print(noOfRows)
                if noOfRows == 1:
                    response["isFound"] = True
                else:
                    response["isFound"] = False

        return response

    except (Exception) as error:
        print(error)
        return str("error" + error)


@app.route("/getRequests", methods=["POST"])
def getRequestsForClient():  # return tha values.
    support_id = request.form['support_id']
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                querytoretrieveRequest = "SELECT customer_id, task, body, status, create_date, complete_date FROM requests WHERE support_id = (%s); "
                cursor.execute(querytoretrieveRequest, (support_id,))
                rows = cursor.fetchall()
                print("No. of rows", len(rows))
                res = []
                for row in rows:
                    l = {}
                    l['customer_id'] = row[0]
                    l['task'] = row[1]
                    l['body'] = row[2]
                    l['status'] = row[3]
                    l['create_date'] = str(row[4])
                    l['complete_date'] = row[5]
                    res.append(l)
                print(res)        
                return jsonify(res)

    except Exception as error:
        return f"Error while adding data to database: {error}"

@app.route('/updateTheStatusOfTasks', methods=['POST'])
def updateTheStatusOfTasks():
    req = request.get_json()
    support_id = req['support_id']
    listOfStatus = []
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                queryToGetCutomerIds = "SELECT customer_id FROM requests WHERE support_id = (%s) AND (status = 'WAITING_FOR_APPROVAL' OR status = 'IN_PROGRESS'); "
                cursor.execute(queryToGetCutomerIds, (support_id,))
                rows = cursor.fetchall()

                for row in rows:
                    listOfStatus.append((getTaskStatus(row[0])['status'],support_id, row[0]))
                    # listOFCustomerIds.append(row[0])

                queryToUpdateStatus = "UPDATE requests SET status = (%s) WHERE (support_id = (%s) AND customer_id = (%s))"
                cursor.executemany(queryToUpdateStatus, listOfStatus)


    except(Exception, psycopg2.Error) as error:
        return 'error occured while updating: ' + error 
    
    return "Updated successfully"

@app.route('/approveRequest', methods=['POST'])
def approveRequest():
    list_task_id = request.form['list_task_id'].split(",")
    # list_task_id = [(x,) for x in list_task_id]
    try:
        with conn_pool.getconn() as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                queryToGetRequest = "SELECT customer_id, task, body FROM requests WHERE task_id IN ({0});".format(','.join(map(str, list_task_id)))
                cursor.execute(queryToGetRequest)
                rows = cursor.fetchall()
                print("No. of rows", len(rows))
                res = []
                for row in rows:
                    l = {}
                    l['customer_id'] = row[0]
                    l['task'] = row[1]
                    l['body'] = row[2]
                    res.append(l)
                # print(res)
            for job in res:
                if(job['task'] == 1):
                    return updatePublicIPs(job)
                if(job['task'] == 2): 
                    #do it later 
                    #remove IP
                    
                    pass
                if(job['task'] == 3):
                    
                    return updatePSMcertificates(job)

                if(job['task'] == 4):
                    return updateLDAPcertificates(job)

    except Exception as error:
        return {"message": str(error)}









# ________________ TESTing ________________

@app.route('/testing', methods=['GET', 'POST'])
def test():
    files = request.files.getlist("files")
    print(files)
    path = "database_files"
    list = []
    for file in files:
        fileName =  str(time.time_ns()) +"_"+ file.filename
        list.append(fileName)
        file.save(path +  "\\" + fileName)
    csv_of_files = ",".join(list)
    print(csv_of_files)

    return "0"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="127.0.0.1")
