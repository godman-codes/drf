const contentContainer = document.getElementById("content-container");
const loginForm = document.getElementById("login-form");
const baseEndpoint = "http://127.0.0.1:8000/api";

if (loginForm) {
   loginForm.addEventListener("submit", handleLogin);
}

function handleLogin(event) {
   console.log(event);
   event.preventDefault();
   const loginEndpoint = `${baseEndpoint}/token/`;
   let loginFormData = new FormData(loginForm);
   let loginObjectData = Object.fromEntries(loginFormData);
   console.log(loginObjectData);
   const options = {
      method: "POST",
      headers: {
         "Content-Type": "application/json",
      },
      body: JSON.stringify(loginObjectData),
   };
   fetch(loginEndpoint, options)
      .then((response) => {
         console.log(response);
         return response.json();
      })
      .then((authData) => {
         // console.log(authData);
         handleAuthData(authData, getProductList);
      })
      .catch((err) => {
         console.log("err", err);
      });
}
function handleAuthData(authData, callback) {
   localStorage.setItem("access", authData.access);
   localStorage.setItem("refresh", authData.refresh);
   if (callback) {
      callback();
   }
}

function writeToContainer(data) {
   if (contentContainer) {
      contentContainer.innerHTML = "<pre>" + JSON.stringify(data) + "</pre>";
   }
}

function getFetchOptions(method, jsObject) {
   return {
      method: method || "GET",
      headers: {
         "Content-Type": "application/json",
         Authorization: "Bearer " + localStorage.getItem("access"),
      },
      body: jsObject ? JSON.stringify(jsObject) : null,
   };
}

function isTokenNotValid(jsonData) {
   if (jsonData.code && jsonData.code == "token_not_valid") {
      // return a refresh token fetch
      // alert("please login again");
      return false;
   }
   return true;
}

function refreshToken() {
   console.log("refreshing token");
   const endpoint = `${baseEndpoint}/token/refresh/`;
   body = {
      refresh: localStorage.getItem("refresh"),
   };
   const options = getFetchOptions("POST", body);
   fetch(endpoint, options)
      .then((response) => {
         console.log(response);
         return response.json();
      })
      .then((data) => {
         console.log(data);
         if (data.access == undefined) {
            alert("pls login again");
            localStorage.clear();
         } else {
            localStorage.setItem("access", data.access);
            return true;
         }
      })
      .catch((err) => {
         console.log(error);
      });
}

function validateJwtToken() {
   console.log("validating JWT token");
   const endpoint = `${baseEndpoint}/token/verify/`;
   body = {
      token: localStorage.getItem("access"),
   };
   const options = getFetchOptions("POST", body);
   fetch(endpoint, options)
      .then((response) => {
         console.log(response);
         return response.json();
      })
      .then((data) => {
         console.log(data);
         if (data.code == "token_not_valid") {
            console.log("now validate");
            refreshToken();
         }
      })
      .catch((err) => console.log(err));
}

function getProductList() {
   const endpoint = `${baseEndpoint}/products/`;
   let validate2 = validateJwtToken();
   console.log("moving to fetch");
   const options = getFetchOptions();
   fetch(endpoint, options)
      .then((response) => {
         console.log(response);
         return response.json();
      })
      .then((data) => {
         // console.log(data);
         const validData = isTokenNotValid(data);
         if (validData) {
            writeToContainer(data);
         }
      })
      .catch((err) => console.log("err", err));
}
// validateJwtToken();
// refreshToken();
// getProductList();
