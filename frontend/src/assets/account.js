export async function request(path, method, data) {
  const response = await fetch(path, {
    method,
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...(data === undefined ? {} : { body: JSON.stringify(data) }),
  });
  const result = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    const detail = result?.detail;
    const message = Array.isArray(detail)
      ? detail.map(error => `${error.loc.at(-1)}: ${error.msg}`).join(". ")
      : detail || "Something went wrong. Please try again.";
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }
  return result;
}

export function bindForm(id, onSubmit) {
  const form = document.getElementById(id);
  if (!form) return;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const button = form.querySelector("button[type=submit]");
    const alert = document.querySelector('[role="alert"]');
    const status = document.querySelector('[role="status"]');
    alert.hidden = true;
    status.hidden = true;
    button.disabled = true;
    try {
      await onSubmit(Object.fromEntries(new FormData(form)), form, status);
    } catch (error) {
      alert.textContent = error.message;
      alert.hidden = false;
    } finally {
      button.disabled = false;
    }
  });
}

bindForm("register-form", async (data, form, status) => {
  await request("/users/register", "POST", data);
  form.reset();
  status.textContent = "Account created. You can now sign in.";
  status.hidden = false;
});
