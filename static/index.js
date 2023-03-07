const myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
service_global = null;
function display(service){

  // const service = document.getElementById("ListOfServices").value;
  // document.getElementById("customerId-block" ).style.display = "block";
  service_global = service;
  if(service == 1){
    const customerId = document.getElementById("customerId").value;
    var data = {
      customerId: customerId,
    };
    getCustomerPublicIPs(data)
  }

  for(let i = 1; i <=3; i++){
    if(service == i){
    document.getElementById("block" + i ).style.display = "block";
  }else{
    document.getElementById("block" + i ).style.display = "none";
  }

}
}

async function controller() {
  const customerId = document.getElementById("customerId").value;
  var data = {
    customerId: customerId,
  };
  var res = {
    status: "",
    message: "",
  };
  var result = "";


  if (service_global == 1) {
    res = await updateIPs(data) || res;

  } 
  else if (service_global == 2) {
    const fileSelector = document.getElementById("psm-certificates")
    res = await updatePSMcertificates(data, fileSelector) || res;
    // console.info(res);

  }
  else if (service_global == 3) { //ldap
    const fileSelector = document.getElementById("ldap-certificates")
    res = await updateLDAPcertificates(data, fileSelector) || res;
  }


  else if (service_global == 4) {
    result = await getAllTenants(data) || result;
    result = result['list of tenants'] || result;
  }

  document.getElementById("result").innerHTML = result
  document.getElementById("status").innerHTML = res.status;

  document.getElementById("message").innerHTML = res.message;

}

async function updateIPs(data) {
  const IPs = []
  document.getElementById("ListOfUpdatedIPs").value.split(",").forEach(element => {
    IPs.push(element.trim())
  });;

  Object.assign(data, { IPs: IPs });
  const response = await fetch("/updatePublicIPs", {
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });

  res = await response.json();
  console.info(res);
  return res
}

async function getAllTenants(data) {
  Object.assign(data, { tenants: [] });

  const response = await fetch("/getAllTenants",{
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });
  return await response.json();
}

function isValidFileFormat(fileName) {
  
  if (["der", "crt", "cer", "pem"].includes(fileName.split(".").pop())) {
    return true
  }
  return false
}

async function updatePSMcertificates(data, input) {
  const formData = new FormData();
  formData.append('data', JSON.stringify(data));

  for (var i = 0; i < input.files.length; i++) {
    if(isValidFileFormat(input.files[i].name)) {
      formData.append('psmFiles', input.files[i]);
    }else{
      console.info("Invalid file type");
      return false;
    }
  }
  const response = await fetch("/updatePSMcertificates", {
    method: "POST",
    body: formData,
  });
  const res = await response.json()
  return res
  
}

async function updateLDAPcertificates(data, input) {
  const formData = new FormData();
  formData.append('data', JSON.stringify(data));

  for (var i = 0; i < input.files.length; i++) {
    if(isValidFileFormat(input.files[i].name)) {
      formData.append('ldapFiles', input.files[i]);
    }else{
      console.info("Invalid file type");
      return false;
    }
  }
  const response = await fetch("/installLDAPcertificates", {
    method: "POST",
    body: formData,
  });
  const res = await response.json()
  return res

}

async function getCustomerPublicIPs(data){
  const response = await fetch("/getCustomerPublicIPs",{
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });
  res = await response.json()
  document.getElementById("ListOfExisstingIPs").innerHTML = res["list of public IPs"];

}

async function getTaskStatus(){
  var customerId = document.getElementById("customerId").value
  var data = {
    customerId: customerId,
  };
  const response = await fetch("/getTaskStatus", {
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });

  res = await response.json();
  console.info( res ) // {flowProgress: Array(10), status: 'SUCCESS'} call this function every 5 seconds untill successful
  document.getElementById("status").innerHTML = res.status;

}
