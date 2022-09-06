const loginForm = document.getElementById("login-form");
const baseEndpoint = "http://localhost:8000/api";

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
         "content-type": "application/json",
      },
      body: JSON.stringify(loginObjectData),
   };
   fetch(loginEndpoint, options)
      .then((response) => {
         console.log(response);
         return response.json();
      })
      .then((x) => {
         console.log(x);
      })
      .catch((err) => {
         console.log(err);
      });
}
