//making trail effect
const coords = { x: 0, y: 0 };
const circles = document.querySelectorAll(".circle");

const colors = [
    "#ffb56b",
    "#fdaf69",
    "#f89d63",
    "#f59761",
    "#ef865e",
    "#ec805d",
    "#e36e5c",
    "#df685c",
    "#d5585c",
    "#d1525c",
    "#c5415d",
    "#c03b5d",
    "#b22c5e",
    "#ac265e",
    "#9c155f",
    "#950f5f",
    "#830060",
    "#7c0060",
    "#680060",
    "#60005f",
    "#48005f",
    "#3d005e"
];

circles.forEach(function (circle, index) {
    circle.x = 0;
    circle.y = 0;
    circle.style.backgroundColor = colors[index % colors.length];
});

window.addEventListener("mousemove", function (e) {
    coords.x = e.clientX;
    coords.y = e.clientY;

});

function animateCircles() {

    let x = coords.x;
    let y = coords.y;

    circles.forEach(function (circle, index) {
        circle.style.left = x - 12 + "px";
        circle.style.top = y - 12 + "px";

        circle.style.scale = (circles.length - index) / circles.length;

        circle.x = x;
        circle.y = y;

        const nextCircle = circles[index + 1] || circles[0];
        x += (nextCircle.x - x) * 0.3;
        y += (nextCircle.y - y) * 0.3;
    });

    requestAnimationFrame(animateCircles);
}

animateCircles();

// typing effect

const textToType = " where style meets conscience, and every purchase tells a planet-friendly story."; // Change this string as needed
const typewriterElement = document.getElementById('demo');

function typeWriter(text, index) {
    if (index < text.length) {
        if (text.charAt(index) === '\n') {
            typewriterElement.innerHTML += '<br>';
        } else {
            typewriterElement.innerHTML += text.charAt(index);
        }
        index++;
        setTimeout(() => typeWriter(text, index), 70); // Adjust the typing speed (milliseconds)
    }
}

document.addEventListener('DOMContentLoaded', () => {
    typeWriter(textToType, 0);
});



// FAQ

const plus = document.querySelectorAll(".plus")
const minus = document.querySelectorAll(".minus")
const para = document.querySelectorAll(".faqpara")

for (let i = 0; i < plus.length; i++) {
    plus[i].addEventListener('click', function () {
        plus[i].classList.toggle("hidden");
        minus[i].classList.toggle("hidden");
        para[i].classList.toggle("hidden");
    })
}

for (let i = 0; i < minus.length; i++) {
    minus[i].addEventListener('click', function () {
        plus[i].classList.toggle("hidden");
        minus[i].classList.toggle("hidden");
        para[i].classList.toggle("hidden");
    })
}



//slider js
var btn = document.getElementsByClassName('mybtn');
var slide = document.getElementById('slide');


btn[0].onclick = function () {
    slide.style.transform = "translateX(0px)";
    for (i = 0; i < 2; i++) {
        btn[i].classList.remove("active");
    }
    this.classList.add("active");
}
btn[1].onclick = function () {
    slide.style.transform = "translateX(-1320px)";
    for (i = 0; i < 2; i++) {
        btn[i].classList.remove("active");
    }
    this.classList.add("active");
}

var currentIndex = 0;

document.addEventListener('keydown', function (event) {
    if (event.key === 'ArrowLeft') {
        // Move to the previous slide
        currentIndex = Math.max(currentIndex - 1, 0);
        moveSlide(currentIndex);
    } else if (event.key === 'ArrowRight') {
        // Move to the next slide
        currentIndex = Math.min(currentIndex + 1, 1);
        moveSlide(currentIndex);
    }
});

function moveSlide(index) {
    var slide = document.getElementById('slide');
    var btn = document.getElementsByClassName('mybtn');

    // Calculate the new position based on the index
    var newPosition = -index * 1348;

    // Set the new position for the slide
    slide.style.transform = 'translateX(' + newPosition + 'px)';

    // Update the active button
    for (var i = 0; i < 2; i++) {
        btn[i].classList.remove('active');
    }

    btn[index].classList.add('active');
}

// ACTIVE NAV




//animator


document.addEventListener('DOMContentLoaded', function () {
    var boxes = document.querySelectorAll('.box1');

    function animateOnScroll() {
        boxes.forEach(function (box) {
            var boxPosition = box.getBoundingClientRect().top;
            var screenPosition = window.innerHeight / 1.3; // Adjust the division factor for when the animation should trigger

            if (boxPosition < screenPosition) {
                box.style.opacity = '1';
                box.style.transform = 'translateY(0)';
                box.style.transition = 'opacity 1s ease, transform 1s ease';
            }
        });
    }

    // Initial check on page load
    animateOnScroll();

    // Listen for scroll events
    window.addEventListener('scroll', animateOnScroll);
});


// FLIP CARD

document.addEventListener("DOMContentLoaded", function () {
    var cards = document.querySelectorAll('.flip-card');

    cards.forEach(function (card) {
        card.addEventListener('click', function () {
            // Remove 'flipped' class from all cards
            cards.forEach(function (c) {
                if (c !== card) {
                    c.classList.remove('flipped');
                }
            });

            // Toggle 'flipped' class only for the clicked card
            card.classList.toggle('flipped');
        });
    });
});


// logout pop up

// Handle logout button click
document.getElementById("logout-btn").addEventListener("click", function () {
    // Send AJAX request to Flask server for logout
    fetch("/logout", {
        method: "POST"
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



// DEFAULT +91 ADD TO PHONE

document.addEventListener('DOMContentLoaded', function () {
    // Get the phone input element
    var phoneInput = document.getElementById('phone');

    // Add event listener for form submission
    phoneInput.closest('form').addEventListener('submit', function () {
        // Prepend +91 to the phone number if it doesn't already start with it
        if (!phoneInput.value.startsWith('+91')) {
            phoneInput.value = '+91' + phoneInput.value;
        }
    });
});

// ONCLICK FUNCTIONS

// login redirect onclick

function login() {
    window.location.href = "/login";
}
function mycart(){
    window.location.href = "/my-cart"
}
function home(){
    window.location.href = "/home"
}

