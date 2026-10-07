import { bindForm, request } from "./account.js";

const form = document.getElementById("profile-form");
const status = document.querySelector('[role="status"]');
const alert = document.querySelector('[role="alert"]');

function populate(user) {
  for (const field of ["first_name", "last_name", "username", "email"]) {
    form.elements[field].value = user[field];
  }
}

async function profileRequest(method, data) {
  try {
    return await request("/users/me", method, data);
  } catch (error) {
    if (error.status === 401) {
      form.hidden = true;
      location.replace("/login");
    }
    throw error;
  }
}

bindForm("profile-form", async data => {
  populate(await profileRequest("PATCH", data));
  status.textContent = "Profile saved.";
  status.hidden = false;
});

try {
  populate(await profileRequest("GET"));
  status.hidden = true;
  form.hidden = false;
} catch (error) {
  status.hidden = true;
  alert.textContent = error.message;
  alert.hidden = false;
}
