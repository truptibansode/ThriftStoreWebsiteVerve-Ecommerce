 // Handle form submission
 document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Serialize form data
    var formData = new FormData(this);
    
    // Send AJAX request to Flask server
    fetch("/login", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display alert popup based on response
        alert(data.message);
        if (data.redirect) {
            window.location.href = data.redirect; // Redirect to the specified page
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while processing your request.");
    });
});

