(document).ready(function() {
    $('#login_form').on('submit', function(e) {
        e.preventDefault();
        
        var username = $('#username').val();
        var password = $('#password').val();
        
        frappe.call({
            method: "your_app.path.to.custom.login_method",
            args: {
                "username": username,
                "password": password
            },
            callback: function(response) {
                if (response.message === "success") {
                    window.location.href = '/home';  // Redirect on successful login
                } else {
                    alert('Invalid credentials');
                }
            }
        });
    });
});
