document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL path and remove the leading slash
    var path = window.location.pathname.substring(1);

    // Get all navigation links
    var navLinks = document.querySelectorAll('.nav-link');

    // Loop through each navigation link
    navLinks.forEach(function (link) {
        // Check if the link's href matches the current path
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});


const body = document.querySelector('body'),
    sidebar = body.querySelector('nav'),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");
toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
})
searchBtn.addEventListener("click", () => {
    sidebar.classList.remove("close");
})
modeSwitch.addEventListener("click", () => {
    body.classList.toggle("dark");

    if (body.classList.contains("dark")) {
        modeText.innerText = "Light mode";
    } else {
        modeText.innerText = "Dark mode";

    }
});


function editUser(username) {
    window.location.href = "/edit-user-admin?username=" + username;
}

function homeAdmin(){
    window.location.href="/admin-home";
}

// Function to show/hide dropdown menu when edit icon is clicked
$('.bx-edit-alt').click(function() {
    $(this).siblings('.dropdown-menu').toggle();
});


