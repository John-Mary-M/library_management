
  document.getElementById("login-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const usr = document.getElementById("usr").value;
    const pwd = document.getElementById("pwd").value;

    frappe.call({
      method: "your_app.api.login",
      args: { usr, pwd },
      callback: function(response) {
        if (response.message) {
          // Redirect if a location is provided in the response
          window.location.href = response.message.location || "/desk";
        }
      },
      error: function(err) {
        // Display error message
        document.getElementById("login-error").innerText = err.message || "Login failed";
      }
    });
  });

