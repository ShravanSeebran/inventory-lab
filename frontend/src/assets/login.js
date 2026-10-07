import { bindForm, request } from "./account.js";

const form = document.getElementById("login-form");
const signedIn = document.getElementById("signed-in");
const status = document.querySelector('[role="status"]');
const alert = document.querySelector('[role="alert"]');

function showUser(user) {
  form.reset();
  form.hidden = true;
  signedIn.hidden = false;
  status.textContent = `Signed in as ${user.first_name} ${user.last_name}`;
  status.hidden = false;
}

bindForm("login-form", async data => {
  showUser(await request("/users/login", "POST", data));
});

document.getElementById("logout").addEventListener("click", async () => {
  alert.hidden = true;
  try {
    await request("/users/logout", "POST");
    signedIn.hidden = true;
    status.hidden = true;
    form.hidden = false;
    form.elements.username.focus();
  } catch (error) {
    alert.textContent = error.message;
    alert.hidden = false;
  }
});

try {
  showUser(await request("/users/me", "GET"));
} catch (error) {
  if (error.status !== 401) {
    alert.textContent = error.message;
    alert.hidden = false;
  }
}
