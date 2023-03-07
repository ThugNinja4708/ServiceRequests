from flask import Flask, render_template, request, redirect, url_for
import funtions as f
import json
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
    res = {"status": latestTask.get("status"), "flowProgress" : latestTask.get("params").get("flowProgress")}
    return res

if __name__ == '__main__':
    app.run(debug=True,port=5000)