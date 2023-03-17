import requests
import json
headers = {
    'Authorization': 'eyJraWQiOiJSbENXRENCQ2NRbGdtTGVPcDlCcnMwV2VPQTluS1ZHZUNFTnJFQWJaeGlvPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiSk5aZDdCaEhqbXRJal9kdHZLekNwZyIsInN1YiI6ImI3MjUwZWE0LTZmMzAtNDliOC1iZWRlLTYwYTQ0M2EzMDg2NyIsImNvZ25pdG86Z3JvdXBzIjpbInVzLWVhc3QtMV9kVkdSY2RLUTFfY3liZXJhcmstaWRlbnRpdHkiXSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfZFZHUmNkS1ExIiwiY29nbml0bzp1c2VybmFtZSI6ImN5YmVyYXJrLWlkZW50aXR5X3JrYW50aGFAY3liZXJhcmsuY29tIiwibm9uY2UiOiJ4S0lzdjhSZVN2aFk0aWhxU1Fad09GV0lnbXRGSzZTZ0Y1bDlIRm9WVDd2c1dCNWpuY0FReDJiSEVzaFIyczl2d21lWHgzcTJuQ3UzbTJQMUlYMjh1aFZGWkxvcWxaN2JXZGlHTXNVcTZ4aW1nc2FQUHhlRzZKeU9xM3RBRXItaGdvWDJWVGVqUjA4eDlIOEMxLWlPMzhadUFGYXNQYlhBcS1GVnQzakdsRWsiLCJhdWQiOiI2cXFucGxvNWJjZmFraDRjamZwOGhtb3RucCIsImlkZW50aXRpZXMiOlt7InVzZXJJZCI6InJrYW50aGFAY3liZXJhcmsuY29tIiwicHJvdmlkZXJOYW1lIjoiY3liZXJhcmstaWRlbnRpdHkiLCJwcm92aWRlclR5cGUiOiJTQU1MIiwiaXNzdWVyIjoiaHR0cHM6XC9cL2FhZTQyMjIubXkuaWRhcHRpdmUuYXBwXC8xNzZjNDA5Yi0wNTRhLTQ4ZjQtOWRjMi1jOWU3MjM4ZDhkOWEiLCJwcmltYXJ5IjoidHJ1ZSIsImRhdGVDcmVhdGVkIjoiMTY3Mjg0MzMwMDQzNSJ9XSwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NzkwMzE0MzMsImN1c3RvbTpVU0VSX0dST1VQUyI6InBDbG91ZENvbnNvbGVPcHNQUkQiLCJleHAiOjE2NzkwNDU4MzMsImlhdCI6MTY3OTAzMTQzM30.QbBKnsRox0vKXmSqqiRgkGHWhjTNRKCOME2QabRp3e6ZKWGrvCcJkfMfLusd2T9n2iFg3DnKxfkGNSmGO6ACxEu6F1Y5NscBVKeKkJx8mQ2O7rOIsDmgwByKU4zmPrKxLRIfn8UVmoyw7vqlwcHNmQaP15Yybcy1g1CTsSfsTDNnxj7jR-BQPinLVIAly6uG47iL2yeZWFM-7JO4EiR7s7u5wjcEJgE5D_Aqqw-SbNk4W1vFYzy3oyo1Y-k0PDwI8b7MrSGTrvMu0u03kNDtMm6AE8ng9ZgTAv6BKuF6hguH7Qb1xpiJElteV4txUgvgy4T59fPQNadthVeuNMnqdg',
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
    print(res['customerPublicIPs'])
    return ",".join(res['customerPublicIPs']) if (res['customerPublicIPs'] != 'null') and res['customerPublicIPs'] != [] and res['customerPublicIPs'] != None else "No IPs"


def updatePublicIPs(customerId, IPsToBeAdded):
    # customerPublicIPs = getPublicIPs(customerId)
    # for i in IPsToBeAdded:
    #     customerPublicIPs.append(i)
    url = f"https://console.privilegecloud.cyberark.com/tenants/v1/{customerId}/config"
    headers['Content-Type'] = 'application/json'
    payload = json.dumps({"customerPublicIPs": IPsToBeAdded, })
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
    for i in range(len(psm_files)):
        files.append(('files', (psm_files[i].filename,psm_files[i], 'application/octet-stream')))

    url = f"https://console.privilegecloud.cyberark.com/files/v1/installPsmCertificate/{customerId}"
    
    # headers.pop('Content-Type') # so that we can send multipart/form-data (files)

    response = requests.post(url, headers=headers, data=payload, files=files)
    
    return response.json()


def installLDAPCertificate(customerId, ldap_files):
    payload = {'description': 'this is file description'}
    files = []
    for i in range(len(ldap_files)):
        files.append(('files', (ldap_files[i].filename,ldap_files[i], 'application/octet-stream')))

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
