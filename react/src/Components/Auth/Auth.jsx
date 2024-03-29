import React, {useState} from "react";
import "./Auth.css";

function Auth() {
    const [loginPage, setLoginPage] = useState(true);
    return (
    <div className="container">
      <div className="header">{loginPage ? "Login" : "Sign Up"}</div>
      <div className="fields">
        {loginPage ? (
            <>
            <input type="text" placeholder="Username" />
            <input type="password" placeholder="Password" />  
            </>

        ) : (
            <>
            <input type="text" placeholder="First Name" />
            <input type="text" placeholder="Last Name" />
            <input type="email" placeholder="Email" />
            <input type="text" placeholder="Username" />
            <input type="password" placeholder="Password" />  
            </>
        )}
      </div>
      {loginPage && <div className="forgot-password">Forgot Password?</div>}
      <div className="buttons">
        <button id="login" onClick={() => setLoginPage(true)}>Login</button>
        <button id="signup" onClick={() => setLoginPage(false)}>Sign Up</button>
      </div>
    </div>
  );
}

export default Auth;
