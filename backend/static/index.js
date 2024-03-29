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
               
async function sendData(){
  // const task_id = 2;
  const formData = new FormData();
  const customer_id = document.getElementById("customerId").value;
  const input = document.getElementById("ldap-certificates")
  const support_id = 1; // should come from session storage

  const task = "4" // ip_white_list
  // const body = 
  for (var i = 0; i < input.files.length; i++) {
    if(isValidFileFormat(input.files[i].name)) {
      formData.append('body', input.files[i]);
    }else{
      console.info("Invalid file type");
      return false;
    }
  }
  const description = "temp descriptions";
  const status = "WAITING_FOR_APPROVAL";
  // var data = {
  //   customer_id: customer_id,
  //   support_id: support_id,
  //   description: description,
  //   body: body,
  //   task: task,
  //   status: status,
  //   task_id: task_id,
  //   typeOfBody: "files",
  // };


  formData.set('customer_id', customer_id);
  formData.set('support_id', support_id);
  formData.set('description', description);
  // formData.set('body', body);
  formData.set('task', task);
  formData.set('status', status);
  // formData.set('task_id', task_id);
  // formData.set('type_of_Body', typeOfBody);


  const response = await fetch("/insertIntoDatabase", {
    method: "POST",
    body: formData,
  });
 console.info(await response.text());
 
}


async function getData() {
  data = {};
  const response = await fetch("/getDataFromDatabase", {
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });

}
async function getCustomerName(){
  const customer_id = document.getElementById("customerId").value;
  data = {
    customer_id: customer_id,
  };
  const response = await fetch("/getCustomerName", {
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });
  console.log(await response.text());
}

async function updateTheStatusOfTasks(){
  const customer_id = document.getElementById("customerId").value;
  support_id = 1
  data = {
    support_id: support_id,
  };
  const response = await fetch("/updateTheStatusOfTasks", {
    method: "POST",
    body: JSON.stringify(data),
    headers: myHeaders,
  });
  console.log(await response.text());
}



async function test() {
  const formData = new FormData();
  const customerId = document.getElementById("customerId").value;
  const list_task_id = [2];
  // const
  var data = {
    customerId: customerId,
  };
  formData.set('list_task_id', list_task_id)
  // formData.set('support_id', 1)
  // // formData.set()
  const input = document.getElementById("ldap-certificates")
  // formData.append('data', JSON.stringify(data));
  // console.log(input.files)                        
  for (var i = 0; i < input.files.length; i++) {
    if(isValidFileFormat(input.files[i].name)) {
      formData.append('files', input.files[i]);
    }else{
      console.info("Invalid file type");
      return false;
    }
  }

  const response = await fetch("/approveRequest", {
    method: "POST",
    body: formData,
  });
  console.info(await response.json())
}