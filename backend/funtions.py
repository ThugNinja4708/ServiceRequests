import requests
import json
headers = {
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiYzNLZVZqcjFNTXQ2UGVxQTcwbnhkdyIsInN1YiI6ImI3MjUwZWE0LTZmMzAtNDliOC1iZWRlLTYwYTQ0M2EzMDg2NyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3JrYW50aGFAY3liZXJhcmsuY29tIiwibm9uY2UiOiJPZzJtXzdUaEtLUG1OWC1Ya3NpMVBnSkM2cmYxWXh3TVZ5dXRua3FTNHVuZU9paEFObTg0Zm9MZ2pMeFBaSk5IdHRDWWYzaUdtYnVnb2NhTmxmeXB6MVltMXdjZGR4Zm9UbFpGQkhWT2VmV0g2YnhUS1pjRDhHM2xzTjBUSnljZ0pMX2lrdU1hdm9FcHYxc1RDN3RVcFYtLVNsVTlqUHRsOXhIdnVVaktxMVEiLCJhdWQiOiI2cXFucGxvNWJjZmFraDRjamZwOGhtb3RucCIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6InJrYW50aGFAY3liZXJhcmsuY29tIiwicHJvdmlkZXJOYW1lIjoiY3liZXJhcmstaWRlbnRpdHkiLCJwcm92aWRlclR5cGUiOiJTQU1MIiwiaXNzdWVyIjoiaHR0cHM6XC9cL2FhZTQyMjIubXkuaWRhcHRpdmUuYXBwXC8xNzZjNDA5Yi0wNTRhLTQ4ZjQtOWRjMi1jOWU3MjM4ZDhkOWEiLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTY3Mjg0MzMwMDQzNSJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NzkzODgxODEsImN1c3RvbTpVU0VSX0dST1VQUyI6InBDbG91ZENvbnNvbGVPcHNQUkQiLCJleHAiOjE2Nzk0MDI1ODEsImlhdCI6MTY3OTM4ODE4MX0.KhkCu3i1Hp-OqJWrx0dzlvZkUZc9MpyFt4FJ5mZbeM4ccIeYe2DuoeRldL4DdxQOJhWOHNEDnZ9Yzz14ZdAZnHFbHf-oXVjkMFQGPGMYod1TNVpK65q4H4-PiKT6agh62aGrT_V4DqSCtH9TW8jH1Zso9Z1-3cd2bdhCNN5Cdf1dqYTYA0dRNO60ZzVUx_fTIVQ-toFlPdsFwoZyTNOwkrFNr_x75EVwMHFfloHZXJCPFcAJ9O5YInhMluc1GzM_EwelvgQkkwhYH3aQsYb4iiTw9VXmZAY1NKGCDIqoJu4vRE3ZXybsXn-NugqkpXWZEbrFIcT3XYUlQeBaofPs0g',
}


def getALLTenants():
    headers['Content-Type'] = 'application/json'
    url = f'https://console.privilegecloud.cyberark.com/tenants/v1/lean'
    response = requests.get(url, headers=headers)
    return response.json()


def getTenantsByRegion(region):
    headers['Content-Type'] = 'application/json'
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1?region={region}"
    response = requests.get(url, headers=headers)
    return response.json()


def getTenantByCustomerId(customerId):
    headers['Content-Type'] = 'application/json'
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1/{customerId}"
    response = requests.get(url, headers=headers)
    return response.json()


def getPublicIPs(customerId):
    res = getTenantByCustomerId(customerId)
    # print(res['customerPublicIPs'])
    return res['customerPublicIPs'] if (res['customerPublicIPs'] != 'null') and res['customerPublicIPs'] != [] and res['customerPublicIPs'] != None else []


def updatePublicIPs(customerId, IPsToBeAdded):
    customerPublicIPs = getPublicIPs(customerId)
    # print("customerPublicIPs: ", customerPublicIPs)
    # print("IP: ",IPsToBeAdded)
    for i in IPsToBeAdded:
        customerPublicIPs.append(i)
    # print(customerPublicIPs)
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1/{customerId}/config"
    headers['Content-Type'] = 'application/json'
    payload = json.dumps({"customerPublicIPs": customerPublicIPs, })
    # print(payload['public_ips'])

    response = requests.patch(url, headers=headers, data=payload)
    
    return response.json()


def deployFeature_H5GW(customerId):
    payload = json.dumps({})
    headers['Content-Type'] = 'application/json'
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1/{customerId}/features/html5gw"
    response = requests.post(url, headers=headers, data=payload)
    # return response.json()["svcMessage"]
    return response.json()


def installPSMCertificate(customerId, psm_files):
    payload = {'description': 'this is file description'}
    files = []
    path = "database_files"
    for file_name in psm_files:
        fileName = file_name[file_name.index("_")+1:]
        # print("fileName: " , fileName)
        # print("path: " , path + "\\" + file_name)
        files.append(('files', (fileName, open(path + "\\" + file_name, 'rb'), 'application/octet-stream')))

    url = f"https://console.privilegecloud.cyberark.com/files/v1/installPsmCertificate/{customerId}"
    
    # headers.pop('Content-Type') # so that we can send multipart/form-data (files)

    response = requests.post(url, headers=headers, data=payload, files=files)
    
    return response.json()


def installLDAPCertificate(customerId, ldap_files):
    payload = {'description': 'this is file description'}
    files = []
    path = "database_files"
    for file_name in ldap_files:
        fileName = file_name[file_name.index("_")+1:]
        # print("fileName: " , fileName)
        # print("path: " , path + "\\" + file_name)
        files.append(('files', (fileName, open(path + "\\" + file_name, 'rb'), 'application/octet-stream')))

    url = f"https://console.privilegecloud.cyberark.com/files/v1/installCertificate/{customerId}"
    
    # headers.pop('Content-Type') # so that we can send multipart/form-data (files)

    response = requests.post(url, headers=headers, data=payload, files=files)
    
    return response.json()

def getTaskStatus(customerId):
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1/tasks?mainObjectId=" + customerId
    response = requests.request("GET", url, headers=headers)
    response = response.json()
    # print(response)
    return response

def getCustomerName(customerId):
    res = getTenantByCustomerId(customerId)
    return res["customerName"]
if __name__ == "__main__":

    pass
