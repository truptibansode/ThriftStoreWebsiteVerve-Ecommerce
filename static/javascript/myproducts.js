var cart = [];
var categories; // Define categories in the global scope

// function addtocart(a) {
//     const product_id = categories[a].product_id; // Assuming there's a product_id field in your data
//     fetch("/add-to-cart", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({
//             product_id: product_id
//         })
//     })
//         .then(response => {
//             if (response.ok) {
//                 // Handle success (e.g., show a success message)
//                 console.log("Product added to cart successfully");
//                 // After adding the product to the cart, you can update the UI if needed
//                 cart.push({ ...categories[a] });
//                 displaycart();
//             } else {
//                 // Handle error response
//                 console.error("Failed to add product to cart");
//             }
//         })
//         .catch(error => {
//             console.error("Error adding product to cart:", error);
//         });
// }

function addtocart(a) {
    const product_id = categories[a].product_id;
    fetch("/add-to-cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_id: product_id
        })
    })
        .then(response => {
            if (response.ok) {
                console.log("Product added to cart successfully");
                cart.push({ ...categories[a] });
                displaycart(product_id); // Pass product_id to displaycart()
            } else {
                console.error("Failed to add product to cart");
            }
        })
        .catch(error => {
            console.error("Error adding product to cart:", error);
        });
}

function delElement(index) {
    const deletedItem = cart.splice(index, 1)[0]; // Remove the item from the cart array
    displaycart(); // Update the cart display

    // Send request to backend to delete the item from the database
    fetch("/delete-from-cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product_id: deletedItem.product_id
        })
    })
        .then(response => {
            if (response.ok) {
                console.log("Product deleted from cart successfully");
            } else {
                console.error("Failed to delete product from cart");
            }
        })
        .catch(error => {
            console.error("Error deleting product from cart:", error);
        });
}


function displaycart() {
    let total = 0;
    const cartItemElement = document.getElementById("cartItem");
    const countElement = document.getElementById("count"); // Get the count element
    const buyNowDiv = document.getElementById("buyNowDiv"); // Get the Buy Now div

    if (cart.length === 0) {
        cartItemElement.innerHTML = "Your cart is empty";
        countElement.innerText = "0"; // Set count to 0 when cart is empty
        document.getElementById("total").innerHTML = "₹ " + total.toFixed(2); // Display total without formatting
        buyNowDiv.innerHTML = ""; // Clear the Buy Now div
    } else {
        total = cart.reduce((acc, item) => acc + parseFloat(item.price), 0); // Calculate total using reduce
        countElement.innerText = cart.length; // Update the count
        cartItemElement.innerHTML = cart.map((items, index) => {
            var { image_path, productname, price } = items;
            return (
                `<div class='cart-item'>
                <div class='row-img'>
                <img class='rowimg' src=${image_path}>
            </div>
                <p style='font-size:12px;'>${productname}</p>
                <h2 style='font-size: 15px;'>₹ ${price}.00</h2>
                </div>`
                // <button class="delete-btn" style="background: transparent; border: none;" onclick='delElement(${index})'><i class="fa-solid fa-trash"></i></button> <!-- Add delete button -->
            );
        }).join('');
        // Add Buy Now button
        buyNowDiv.innerHTML = `<button class="buy-now-btn" onclick="buyNow()">Buy Now</button>`;
        document.getElementById("total").innerHTML = "₹ " + total.toFixed(2); // Display total with two decimal places
    }
}




// Fetch product data from the server
fetch('/get-myproducts')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(products => {
        console.log('Products:', products); // Debugging statement
        categories = products; // Assign the fetched products to categories
        let i = 0;
        document.getElementById('root').innerHTML = categories.map((item, i) => {
            const { image_path, productname, price, addedBy } = item;
            return (
                `<div class='box'>
                    <div class='img-box'>
                        <img class='images' src='${image_path}'></img>
                        <p style="font-size: 13px; color: gray;">product posted by ${addedBy}</p>
                    </div>
                    <div class='bottom'>
                        <p>${productname}</p>
                        <h2 style="margin: 0;">₹ ${price}.00</h2>
                    </div>
                </div>`
                // <button class="atcbtn" onclick='addtocart(${i})'>Add to cart</button> <!-- Use i directly -->
            );
        }).join('');

    })
    .catch(error => console.error('Error fetching products:', error));


// ANOTHER CODE 
document.addEventListener("DOMContentLoaded", function () {
    const cartButton = document.querySelector(".nav-item.cart"); // Select the cart button
    const sidebar = document.getElementById("sidebar"); // Select the sidebar
    const root = document.getElementById("root"); // Select the root element

    // Hide the sidebar initially
    sidebar.style.display = "none";

    // Add click event listener to the cart button
    cartButton.addEventListener("click", function () {
        // Toggle the visibility of the sidebar
        sidebar.style.display = sidebar.style.display === "none" ? "block" : "none";
        // Update the width of the root element
        root.style.width = sidebar.style.display === "none" ? "100%" : "70%";

        // Update the grid template columns of the root element
        root.style.gridTemplateColumns = sidebar.style.display === "none" ? "repeat(3, 1fr)" : "repeat(2, 1fr)";

        // Scroll to the sidebar when it is opened
        if (sidebar.style.display === "block") {
            sidebar.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    });
});

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const root = document.getElementById('root');

    // Hide the sidebar
    sidebar.style.display = 'none';
    // Update the width of the root element
    root.style.width = '100%';
}

// ORDER FUNCTIONALITY
function buyNow() {
    // Extract product IDs from the cart array
    const productIds = cart.map(item => item.product_id);
    
    // Send a POST request to the backend to create the order
    fetch('/create-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_ids: productIds
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to create order');
        }
    })
    .then(data => {
        // Display the order ID received from the backend
        alert('Order has been created! Your Order ID is: ' + data.order_id);
        // Optionally, clear the cart after successful order creation
        cart = [];
        displaycart();
    })
    .catch(error => {
        console.error('Error creating order:', error);
        alert('Failed to create order. Please try again later.');
    });
}

