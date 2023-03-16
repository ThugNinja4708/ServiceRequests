import React from "react";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import "./LoginPage.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
const LoginPage = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  
  const handleKeypress = (e) => {
    if (e.keyCode === 13) {
      this.btn.click();
    }
  };
  const isValidInput = (user_name) => {
    const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
    if (usernameRegex.test(user_name)) {
      return true;
    }
    return false;
  };
  const handleOnChange = async () => {
    console.log(userName, password);
    setUserName(userName.trim());

    if (isValidInput(userName)) {
      console.log("Yes");
      const data = {
        user_name: userName,
        password: password,
      };

      const response = await fetch("/verifyLogin", {
        method: "POST",
        body: JSON.stringify(data), // string or object
        headers: {
          "Content-Type": "application/json",
        },
      });

      const res = await response.json();
      console.log(res["isFound"]);
    } else {
      alert("User_name must be 3-20 character and only alphabets and numeric");
    }

    setUserName("");
    setPassword("");
  };

  return (
    <React.Fragment>
      <div className="page">
        <div className="cover">
          <div className="content" style={{ padding: "10%" }}>
            <h3
              style={{
                fontWeight: "500",
                fontFamily: "Fira Sans",
                paddingLeft: "130px",
              }}
            >
              Sign In
            </h3>
            <div
              className="mb-3"
              style={{
                fontFamily: "Fira Sans",
                fontWeight: "500",
                fontSize: "18px",
                paddingTop: "25px",
              }}
            >
              Enter Username
            </div>
            <input
              value={userName}
              className="user-credentials"
              type="text"
              placeholder="Enter Username"
              style={{ width: "24em" }}
              pattern="/^[a-zA-Z0-9_]{3,20}$/"
              onChange={(e) => setUserName(e.target.value)}
            />
            <div
              className="mb-3"
              style={{
                fontFamily: "Fira Sans",
                fontWeight: "500",
                fontSize: "18px",
                paddingTop: "15px",
              }}
            >
              Enter Password
            </div>
            <input
              className="user-credentials"
              type="password"
              placeholder="Enter Password"
              value={password}
              style={{ width: "24em" }}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div
              className="login-btn"
              style={{ paddingTop: "30px", fontSize: "20px", width: "100%" }}
            >
              <button
                type="submit"
                className="btn btn-primary"
                style={{ width: "360px" }}
                onClick={handleOnChange}
                onKeyPress={handleKeypress}
              >
                Sign In
              </button>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
};
export default LoginPage;
