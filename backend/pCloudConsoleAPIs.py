import requests
import json
import http.client
headers = {
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoieVZMbUpiV0hWcVhPbUJ5dnlpaVlLZyIsInN1YiI6ImI3MjUwZWE0LTZmMzAtNDliOC1iZWRlLTYwYTQ0M2EzMDg2NyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3JrYW50aGFAY3liZXJhcmsuY29tIiwiYXVkIjoiNnFxbnBsbzViY2Zha2g0Y2pmcDhobW90bnAiLCJpZGVudGl0aWVzIjpbeyJ1c2VySWQiOiJya2FudGhhQGN5YmVyYXJrLmNvbSIsInByb3ZpZGVyTmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5IiwicHJvdmlkZXJUeXBlIjoiU0FNTCIsImlzc3VlciI6Imh0dHBzOlwvXC9hYWU0MjIyLm15LmlkYXB0aXZlLmFwcFwvMTc2YzQwOWItMDU0YS00OGY0LTlkYzItYzllNzIzOGQ4ZDlhIiwicHJpbWFyeSI6InRydWUiLCJkYXRlQ3JlYXRlZCI6IjE2NzI4NDMzMDA0MzUifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjc5NTU0NTY1LCJjdXN0b206VVNFUl9HUk9VUFMiOiJwQ2xvdWRDb25zb2xlT3BzUFJEIiwiZXhwIjoxNjc5NTY4OTY1LCJpYXQiOjE2Nzk1NTQ1NjV9.YffQnKEXi1en9L5p4zN7rmYRBhG8aBXczDqIvcruuiDXXcaXC4qYBr9aCfehKXSiI5Axq-RMS80C9GdYRXOo-aa_5-yRMEJMDe97C6ZZ28RzWIf2f3oyd-k5nkCnPbc9p9rH24K1IPXyYL3UeWBwcMKJYmw7ag32hijGhTu42mySmcdMsoDzsarWcdSlrFYD5W-9n830yDk1QaBwGHt8M6RW2D12JbCV5W6_TGE-cyJ2juA-Y1pC-cffo__djnmQ9hVN-LrxmPcKo-jROh9agKamnuocyURD4fun4RdM4LUZfTVZu7BMddcWdswVXrwX_yKS1OifrsIx_-x9kVY01w',
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
    if(response.status_code == 200 and response.status_code < 300):
        return response.json()
    else:
        error_message = f"API call failed with status code {response.status_code} : {http.client.responses[response.status_code]}"
        if response.content:
            error_message += f" and response content: {response.content.decode()}"
        raise Exception(error_message)


def getPublicIPs(customerId):
    res = getTenantByCustomerId(customerId)
    # if "error_message" in res.keys():
    #     return res
    isResposeValid = res['customerPublicIPs'] != 'null' and res['customerPublicIPs'] != [] and res['customerPublicIPs'] != None
    # print(res['customerPublicIPs'])
    return res['customerPublicIPs'] if ( isResposeValid) else []


def updatePublicIPs(customerId, IPsToBeAdded):
    customerPublicIPs = getPublicIPs(customerId)
    # print("customerPublicIPs: ", customerPublicIPs)
    # print("IP: ",IPsToBeAdded)
    for i in IPsToBeAdded:
        customerPublicIPs.append(i)
    # print(customerPublicIPs)
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1/{customerId}/config"
    headers['Content-Type'] = 'application/json'
    payload = json.dumps({"customerPublicIPs": customerPublicIPs })
    # print(payload['public_ips'])

    response = requests.patch(url, headers=headers, data=payload)
    if response.status_code >= 200 and response.status_code < 300:
        return response.json()
    else:
        raise Exception(f"API call failed with status code {response.status_code}")
    
    # return response.json()


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
