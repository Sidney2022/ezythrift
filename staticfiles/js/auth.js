// const msgCloseBtn = document.getElementById("msgCloseBtn")
const msgArea = document.getElementById("msgArea")
const firstNameField = document.getElementById("firstNameField")
const lastNameField = document.getElementById("lastNameField")
const EmailField = document.getElementById("emailField")
const EmailFieldMsg = document.getElementById("emailFieldMsg")
const passwordField = document.getElementById("passwordField")
const passwordFieldMsg = document.getElementById("passwordFieldMsg")
const conFPasswordField = document.getElementById("confPasswordField")
const RegForm = document.getElementById("reg-form")
const RegBtn = document.getElementById("reg-btn")

const LoginEmailField = document.getElementById("loginEmailField")
const LoginMsg = document.getElementById("loginMsg")
const LoginForm = document.getElementById("login-form")
const LoginpasswordField = document.getElementById("loginpasswordField")
const LoginBtn = document.getElementById("login-btn")
const next = document.getElementById("next")



LoginForm.addEventListener("submit" , (event) => {
  event.preventDefault()
 LoginMsg.innerHTML = ''
 LoginpasswordField.classList.remove('is-invalid')
 LoginEmailField.classList.remove("is-invalid")
  fetch("/accounts/signin", {
    body: JSON.stringify({
      email: LoginEmailField.value,
      password:LoginpasswordField.value,
      }),
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
     console.log("data", data);
     if (data.auth_error) {
      LoginEmailField.classList.add('is-invalid')
      LoginpasswordField.classList.add('is-invalid')
      msgArea.setAttribute('style', 'display:block')
      msgArea.innerHTML = `invalid login credentials `
    }
    else {
       LoginEmailField.classList.add('is-valid')
       LoginpasswordField.classList.add('is-valid')
       if (next.value == "None") {
        window.location = '/'
       } else {

         window.location = `${next.value}`
       }
     }

    });
})


RegForm.addEventListener("submit" , (event) => {
  event.preventDefault()
 EmailField.classList.remove('is-invalid')
  passwordField.classList.remove("is-invalid")
  conFPasswordField.classList.remove("is-invalid")
  fetch("/accounts/signup", {
    body: JSON.stringify({
      first_name:firstNameField.value,
      last_name:lastNameField.value,
      email: EmailField.value,
      password:passwordField.value,
      password2:conFPasswordField.value
      }),
    method: "POST",
  })
    .then((res) => res.json())
    .then((data) => {
     console.log("data", data);
     if (data.email_exists) {
      EmailField.classList.add('is-invalid')
      msgArea.setAttribute('style', 'display:block')
      msgArea.innerHTML = `email already in use. if this is your account, please login `
     }
     else if (data.password_strength) {
       conFPasswordField.classList.add("is-invalid")
       passwordField.classList.add("is-invalid")
      msgArea.setAttribute('style', 'display:block')
      msgArea.innerHTML = `${data['password_strength']}`
     }
     else if (data.password_match) {
      passwordFieldMsg.innerHTML = 'passwords do not match'
      conFPasswordField.classList.add("is-invalid")
      passwordField.classList.add("is-invalid")
      msgArea.setAttribute('style', 'display:block')
      msgArea.innerHTML = `passwords do not match `



     }
     else {
      window.location = "/"
     }

    });
})


