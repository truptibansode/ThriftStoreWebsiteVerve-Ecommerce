from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from pymongo import MongoClient, DESCENDING
from flask_mail import Mail, Message
from twilio.rest import Client # FOR SMS CONFIRMATION
import os
from werkzeug.utils import secure_filename
import random
import string
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# mongo db verve_users password afceVxMLenMv4CdT and username truptibansode3
client = MongoClient("mongodb_link_here")

# i have manually created my databases in mongodb ATLAS

# user database
db =  client.get_database('verve_users')
records = db.users #user db

# product database
productsDB = client.get_database('verve_products_db')
productsCollection = productsDB.products #product db

# order details database
orderDetails = client.get_database("orderTrackingDetails")
orders_collection = orderDetails.orderDetailsDb

# Cart details Database
cartCollection = client.get_database("shoppingCartDetails")
cartDB = cartCollection.cartDetailsDb

# Contact Database
contactDatabase = client.get_database("contactFeedbackdb")
feedbackCollection = contactDatabase.feedbackCollection

feedbackCollection.update_many({}, {"$set": {"response_sent": False}})

# admin database
adminDb = client.get_database("adminDb")
adminCreds = adminDb.adminCredsDB

# Response database
adminReplyDb = client.get_database("adminReplytoCustomerDB")
ResponseDb = adminReplyDb.ResponseDb

# Check MongoDB connection
if client:
    print("Connected to MongoDB Atlas successfully.")
else:
    print("Failed to connect to MongoDB Atlas.")

bcrypt = Bcrypt(app) #for password encryption

#SMS Function
# <<<<<<< HEAD
# account_sid = 'your_account_sid'
# auth_token = 'AUTH_TOKEN'
# =======
# account_sid = 'my SID'
# auth_token = 'auth token'
# >>>>>>> c3b34e6 (Initial Commit)
# myclient = Client(account_sid, auth_token)

# def send_sms(phone):
#      # Send SMS confirmation
#     try:
#         message = myclient.messages.create(
# <<<<<<< HEAD
#         from_='PHONE',
# =======
#         from_='number provided',
# >>>>>>> c3b34e6 (Initial Commit)
#         body='You have successfully registered to Verve! Thank you for joining us on this journey! 💕😸',
#         to=phone
#         )

#         print(message.sid)
#         return "SMS sent successfully!"
#     except Exception as e:
#         return f"Error sending SMS: {e}"

# MAIL SECTIONS
# VERVE GMAIL ACC PASSWORD uosk cixc xdjy ymgh

app.config ['SECRET_KEY'] = "MY_SECRET_KEY_HERE" 
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"] = "MY_EMAIL"
app.config["MAIL_PASSWORD"] = "EMAIL_PASSWORD"

mail = Mail(app)


# Generate OTP for verification
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# MAIL SENDING FUNCTION

def confirmation_mail(email):
    msg_title = "Successful Registration Confirmation E-mail"
    sender = "verveinc@noreply.in"
    msg = Message(msg_title, sender=sender,recipients=[email])
    msg_body = "This email is sent to inform you that you have successfully registered on Verve. We are thrilled to have you onboard our journey! Please keep supporting and loving us!"
    data = {
        'app_name': "Verve Inc",
        'title': msg_title, 
        'body': msg_body
    }

    msg.html = render_template("email_register.html", data=data)
    try:
        mail.send(msg)
        print("email sent successfully!")
        return "email sent successfully...."
    except Exception as e:
        print(e)
        print("error sending email. please try again later. ")
        return "email not sent...."
  
def getUserEmail(username):
    myuser = records.find_one({"username":username})
    if myuser:
        print (myuser["email"])
        return myuser["email"]
    else:
        print("email not found")
        return None

  
#INDEX page route
@app.route("/")
def index():
    title="Verve: Sustainably styled stories."
    return render_template("index.html", title=title)
    
#register page route
@app.route("/register", methods=["GET", "POST"])
def register():
    title = "Welcome To Verve: Sustainably styled stories."
    print("Inside /register route")
    
    if request.method == "POST":
        # Retrieve form data
        data = request.form.to_dict()
        print("Form data:", data)
        
        # Handle file upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file.filename != '':
                # Save the file to a folder
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                print("Profile picture saved to:", file_path)
                # Optionally, you can store the file path in your database
                data['profile_pic'] = file_path
            else:
                data['profile_pic'] = "/static/images/defaultpfp.jpeg"
        
        existing_user = records.find_one({"username": data["username"]})
        if existing_user:
            myvar = "user already exists. please try again."
            print("user already exists. please try again.")
            return render_template("register.html", myvar=myvar)
        # "User exists already. Cannot create account. Please try again later.", 
        else:
            print("New User Registration. Welcome to Verve.")
            # return "New User Registration. Welcome to Verve."
            myalerter = "User Successfully Created!! Please log in to access Home page."

            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            data["password"] = hashed_password
            
            # Inserting the form data into MongoDB
            result= records.insert_one(data)
            print("Insertion result:", result)
            # confirmation_mail(data["email"])
            # send_sms(str(data["phone"]))
            return render_template("login.html", title=title, myalerter=myalerter)

    return render_template("register.html", title=title)

#login page route
@app.route("/login", methods=["GET", "POST"])
def login():
    title="Welcome Back To Verve: Sustainably styled stories."
    if is_user_authenticated():
        username = session.get("username")
        return redirect(url_for("home"))
    if request.method == "POST": 
        #retrieving the info from form
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        user = records.find_one({"username":username})
        if user:
            if bcrypt.check_password_hash(user["password"], password):
                print("user identified. access granted. redirecting to home page...")
                session["username"] = username
                return redirect(url_for("home"))
            else:
                print("Incorrect password. Access denied. Redirecting to login page....")
                return redirect(url_for("login"))
        else:
            print("user not identified. access denied. redirecting to registration page....")
            return redirect(url_for("register"))
   
    return render_template("login.html", title=title)     
 
@app.route("/logout", methods=["GET","POST"])
def logout():
    # Clear any session data related to the user's authentication
    session.clear()
    print("logged out successfully. redirecting user to sign-in page.....")
    return redirect(url_for("login"))

def is_user_authenticated():
    username = session.get("username")
    print (username)
    return username is not None

# FORGOT PASSWORD FUNCTIONALITY
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        # Generate OTP
        otp = generate_otp()
        # Send OTP via email
        msg_title = "Password Reset Request - OTP"
        sender = "verveinc@noreply.in"
        msg = Message(msg_title, sender=sender, recipients=[email])
        msg.body = f'Your OTP is: {otp}'
        mail.send(msg)
        # Store OTP, email, and username in session
        session['otp'] = otp
        session['reset_email'] = email
        session['reset_username'] = username
        return redirect(url_for('verify_otp'))
    return render_template('forgot_password.html')

# Verify OTP Route
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        # Verify OTP
        if entered_otp == session['otp']:
            # OTP is correct, proceed to reset password
            return redirect(url_for('reset_password'))
        else:
            # Invalid OTP, display error message
            return "Invalid OTP"
    return render_template('verify_otp.html')

# Reset Password Route
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        # Check if new password and confirm password match
        if new_password == confirm_password:
            # Update password in the database for the user with the reset_email
            reset_email = session.get('reset_email')
            reset_username = session.get('reset_username')
            if reset_email and reset_username:
                user = records.find_one({"email": reset_email, "username": reset_username})
                if user:
                    # Hash the new password
                    hashed_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
                    # Update the user's password in the database
                    records.update_one({"email": reset_email, "username": reset_username}, {"$set": {"password": hashed_password}})
                    # Clear the session data
                    session.pop('otp', None)
                    session.pop('reset_email', None)
                    session.pop('reset_username', None)
                    myalerter = "Password reset successfully"
                    return render_template("login.html", myalerter = myalerter)
                else:
                    return "User not found"
            else:
                return "Session data missing"
        else:
            return "Passwords do not match"
    return render_template('reset_password.html')

#home page
# @app.route("/home/<username>")    
@app.route("/home") 
def home():
    title="Verve: Sustainably styled stories."
    products = productsCollection.find() #to fetch uploaded data
    accessories = list(productsCollection.find({"keywords": "accessory"}))
    apparel = list(productsCollection.find({"keywords": "apparel"}))
    # shoes = productsCollection.find({"keywords": "shoes"})

    if products:
        print ("product db connected")
    if is_user_authenticated():
        username = session.get("username")
        print(session)
        return render_template("home.html", title=title, username=username, products=products, accessories=accessories, apparel = apparel)
    else:
        myalerter = "You're not logged in. Please log in to access Home page."
        return render_template("login.html", myalerter=myalerter)
    
    # return render_template("home.html", title=title)
    
#ACCESSORIES ROUTE
@app.route("/accessory")
def accessory():
    title="Accessory | Verve: Sustainably styled stories."
    if is_user_authenticated():
        products = productsCollection.find({'keywords': 'accessory'})
        return render_template("accessory.html", title=title, accessory_products=products)
    else:
        return render_template("login.html", title=title)
    
     
# MYACCOUNT ROUTE  
@app.route("/myaccount")
def myAccount():
    title="Accessory | Verve: Sustainably styled stories."
    myusers = db.users.find({"username": {"$regex": session.get("username"), "$options": "i"}})
    mydetails = [(user["username"], user["fullname"], user["phone"], user["email"], user["profile_pic"]) for user in myusers]
    
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    # Check if username exists in productsCollection
    user_products = list(productsCollection.find({"addedBy": username}))
    username_exists_in_db = bool(user_products)
   
    return render_template("userprofile.html",title=title, mydetails=mydetails, username_exists_in_db=username_exists_in_db)

# Initialize the counter variable with the maximum product_id value in the database
max_product_id_doc = productsCollection.find_one(sort=[("product_id", -1)])
if max_product_id_doc and 'product_id' in max_product_id_doc:
    product_id_counter = int(max_product_id_doc['product_id']) + 1
else:
    # If no products exist or 'product_id' field is not present, initialize the counter with 0
    product_id_counter = 0
@app.route("/add-product", methods=["GET", "POST"])
def add_product():
    title = "Add Product | Verve: Sustainably styled stories."
    global product_id_counter
    print("Inside /add_product route")

    if request.method == "POST":
        # Retrieve form data
        data = {
            "addedBy": session.get("username"),
            "product_id": str(product_id_counter),
            "productname": request.form.get("productname"),
            "price": request.form.get("price"),
            "description": request.form.get("description"),
            "keywords": request.form.get("keywords")
        }

        # Handle file upload
        if 'product_image' in request.files:
            image = request.files['product_image']
            if image.filename != '':
                # Save the image to a folder
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                print("Product image saved to:", image_path)
                # Optionally, you can store the file path in your database
                data['image_path'] = image_path
                
                # MAIL SENDING FUNCTION

        # Inserting the form data into MongoDB
        productsCollection.insert_one(data)
        product_id_counter += 1
        print("Product data inserted into MongoDB")
        
        def productConfirmation(email):
            msg_title = "Product added to Verve successfully."
            sender = "verveinc@noreply.in"
            msg = Message(msg_title, sender=sender,recipients=[email])
            msg_body = f"Your product has been uploaded to Verve successfully. We will keep you notified on further activities regarding your product. product details: product id : {data['product_id']}, product name : {data['productname']}, product price : {data['price']}"
            mydata = {
                'app_name': "Verve Inc",
                'title': msg_title, 
                'body': msg_body
            }

            msg.html = render_template("emailtwo.html", mydata=mydata)
            try:
                mail.send(msg)
                print("product confirmation email sent successfully!")
                return "email sent successfully...."
            except Exception as e:
                print(e)
                print("error sending email. please try again later. ")
                return "email not sent...."
        
        email = getUserEmail(session.get("username"))
        if email:
            productConfirmation(email)
        else:
            print("Email not found for the username:", session.get("username"))

        # Redirect to the add-product page after adding the product
        return redirect(url_for("myAccount"))

    return render_template("addproduct.html", title=title)

@app.route("/get-products")
def get_products():
    products = list(productsCollection.find({}, {"_id": 0})) # Exclude _id field
    return jsonify(products)

from bson.json_util import dumps

@app.route("/get-accessory")
def get_accessory():
    products = list(productsCollection.find({"keywords": "accessory"}))
    # Convert ObjectId to string for each product
    for product in products:
        product['_id'] = str(product['_id'])
    return dumps(products)  # Convert the list of dictionaries to JSON


@app.route("/get-myproducts")
def get_myproducts():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))
    
    user_products = list(productsCollection.find({"addedBy": username}))
    
    # Convert ObjectId to string for each document in the list
    for product in user_products:
        product['_id'] = str(product['_id'])

    return jsonify(user_products)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json
    product_id = data.get("product_id")
    customer_name = session.get("username")  # Get the username from the session

    # Assuming you have a collection named 'products' in your database
    product = productsCollection.find_one({"product_id": product_id})

    if product:
        # If product exists, extract relevant details
        product_details = {
            "product_id": product.get("product_id"),
            "productImage": product.get("image_path"),
            "productname": product.get("productname"),
            "description": product.get("description"),
            "price": product.get("price")
        }

        # Insert into the 'cartDB' collection
        cartDB.insert_one({
            "product_id": product_id,
            "product_details": product_details,
            "customer_name": customer_name
        })

        return jsonify({"message": "Product added to cart successfully"}), 200
    else:
        return jsonify({"error": "Product not found"}), 404

@app.route("/delete-from-cart", methods=["POST"])
def delete_from_cart():
    data = request.json
    product_id = data.get("product_id")
    customer_name = session.get("username") 
    
     # Assuming you have a collection named 'products' in your database
    product = productsCollection.find_one({"product_id": product_id})

    if product:
        # If product exists, extract relevant details
        product_details = {
            "product_id": product.get("product_id"),
            "productImage": product.get("image_path"),
            "productname": product.get("productname"),
            "description": product.get("description"),
            "price": product.get("price"),
            # Add other relevant details as needed
        }
        
    # Remove the product from the cartDB collection
    cartDB.delete_one({
            "product_id": product_id,
            "product_details": product_details,
            "customer_name": customer_name
        })
    return jsonify({"message": "Product deleted from cart successfully"}), 200


max_order_id_doc = orders_collection.find_one(sort=[("order_id", -1)])
if max_order_id_doc and 'order_id' in max_order_id_doc:
    order_id_counter = int(max_order_id_doc['order_id']) + 1
else:
    order_id_counter = 0
    

      
@app.route("/create-order", methods=["POST"])
def create_order():
    try:
        data = request.json
        print("Received data:", data)  # Debugging statement

        product_ids = data.get("product_ids")  # Product IDs are sent in the request
        print("Product IDs:", product_ids)  # Debugging statement

        # Fetch product details from productsCollection based on product_ids
        products = productsCollection.find({"product_id": {"$in": product_ids}})
        print("Received product IDs:", product_ids)  # Debugging statement
        print("Product IDs found in the database:", [product["product_id"] for product in products])  # Debugging statement

        # Reset cursor to beginning
        products.rewind()

        # Extract relevant product details
        order_details = []
        total_price = 0
        for product in products:
            product_details = {
                "product_id": product["product_id"],
                "productname": product["productname"],
                "price": float(product["price"]),  
                "image_path": product.get("image_path", "")
            }
            order_details.append(product_details)
            total_price += float(product["price"])  # Convert price to float for calculation

            # Send email to the user who added the product
            email = getUserEmail(product["addedBy"])
            if email:
                sendOrderNotificationEmail(email, product["productname"], total_price)

        print("Order details:", order_details)  # Debugging statement

        global order_id_counter
        # Increment the order_id_counter for the new order
        order_id = order_id_counter
        order_id_counter += 1

        # Save the order details to the database
        order_data = {
            "order_id": order_id,
            "orderedBy": session.get("username"),
            "products": order_details,
            "total_price": total_price,
            "status": "pending"
        }
        orders_collection.insert_one(order_data)

        return jsonify({"order_id": order_id}), 201
    except Exception as e:
        print("Error creating order:", e)
        return jsonify({"error": "An error occurred while creating the order"}), 500



def sendOrderNotificationEmail(email, productName, totalPrice):
    username = session.get("username")
    msg_title = "Order Notification: Your product has been purchased"
    sender = "verveinc@noreply.in"
    msg = Message(msg_title, sender=sender, recipients=[email])
    msg_body = f"Congratulations! Your product '{productName}' has been purchased by our customer {username}. Total Price: ${totalPrice}."
    msg.html = render_template("order_notification_email.html", title=msg_title, body=msg_body)
    try:
        mail.send(msg)
        print("Order notification email sent successfully to:", email)
    except Exception as e:
        print("Error sending order notification email:", e)

# ABOUT ROUTE

@app.route("/about")
def about():
    title="Verve: Sustainably styled stories."
    if is_user_authenticated():
        return render_template("about.html", title=title)
    else:
        return redirect(url_for("login"))



def feedbackConfirmation_mail(email):
    msg_title = "Feedback Sent Notification"
    sender = "verveinc@noreply.in"
    msg = Message(msg_title, sender=sender,recipients=[email])
    msg_body = "This email is sent to inform you that your feedback has been successfully sent! Thank you for your valuable time."
    data = {
        'app_name': "Verve Inc",
        'title': msg_title, 
        'body': msg_body
    }

    msg.html = render_template("email_register.html", data=data)
    try:
        mail.send(msg)
        print("email sent successfully!")
        return "email sent successfully...."
    except Exception as e:
        print(e)
        print("error sending email. please try again later. ")
        return "email not sent...."
  

# CONTACT ROUTE
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    title="Verve: Sustainably styled stories."
    if is_user_authenticated():
        if request.method == 'POST':
            contactUserName = session.get("username")
            contactFullName = request.form.get("contactName")
            contactEmail = request.form.get("contactEmail")
            contactPhone = request.form.get("contactPhone")
            contactMessage = request.form.get("contactMessage")
            current_datetime = datetime.now()
            # Extract date and time components
            submission_date = current_datetime.strftime("%Y-%m-%d")
            submission_time = current_datetime.strftime("%I:%M %p")

            
            contact_data = {
                "posted_by": contactUserName,
                "contacted_user_fullName": contactFullName,
                "contacted_user_email": contactEmail,
                "contacted_user_phone": contactPhone,
                "contacted_user_Feedback": contactMessage,
                "Posted_on_date": submission_date,
                "Posted_on_time": submission_time,
            }
            
            feedbackCollection.insert_one(contact_data)
            feedbackConfirmation_mail(contactEmail)
        return render_template("contact.html", title=title)
    else:
        return render_template("login.html", title=title)
    

# ADMIN SIDE ROUTES



@app.route("/admin-register", methods = ['GET', 'POST'])
def adminRegister():
    title = "Sign Up as an admin | Welcome To Verve: Sustainably styled stories."
    print("Inside /admin register route")
    
    if request.method == "POST":
        # Retrieve form data
        data = request.form.to_dict()
        print("Form data:", data)
        
        existing_user = adminCreds.find_one({"username": data["admin_username"]})
        if existing_user:
            myvar = "user already exists. please try again."
            print("user already exists. please try again.")
            return render_template("admin_register.html", myvar=myvar)
        # "User exists already. Cannot create account. Please try again later.", 
        else:
            print("New User Registration. Welcome to Verve.")
            # return "New User Registration. Welcome to Verve."
            myalerter = "Admin Successfully Created!! Please log in to access Home page."

            # Hash the password before storing it
            hashed_password = bcrypt.generate_password_hash(data["admin_password"]).decode("utf-8")
            data["admin_password"] = hashed_password
            
            # Inserting the form data into MongoDB
            result= adminCreds.insert_one(data)
            print("Insertion result:", result)
            confirmation_mail(data["admin_email"])
            # send_sms(str(data["admin_phone"]))
            return render_template("admin_Login.html", title=title, myalerter=myalerter)

    return render_template("admin_register.html", title=title)
    

@app.route("/admin-login", methods = ["GET", "POST"])
def adminLogin():
     title = "Welcome Admin"
     if request.method == "POST": 
        #retrieving the info from form
        username = request.form.get("admin_username")
        password = request.form.get("admin_password")
        print(username, password)
        user = adminCreds.find_one({"admin_username":username})
        if user:
            if bcrypt.check_password_hash(user["admin_password"], password):
                session['admin_username'] = True
                session['admin_username'] = username  # Store the username in session
                return redirect(url_for("adminHome"))
        else:
                print("Incorrect password. Access denied. Redirecting to login page....")
                return redirect(url_for("adminLogin") );  
     return render_template("admin_Login.html", title = title)


def is_admin_authenticated():
    username = session.get("admin_username")
    print(username)
    return session.get("admin_username")

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_username', None)
    return redirect(url_for('adminLogin'))  # Redirect to the login page after logging out



@app.route("/admin-home")
def adminHome():
    title= "Welcome Admin | Home Page"
    if is_admin_authenticated():
        admin_username = session.get("admin_username")
        print(session["admin_username"])
        userData = records.find()
        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")
        if now.hour < 12:
            greeting = "Good morning"
        elif 12 <= now.hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        return render_template ("admin_Home.html", title = title, username = admin_username, greeting=greeting, current_time = current_time, userData = userData)
    else:
        return redirect(url_for("adminLogin"))

@app.route("/edit-user-admin", methods=["GET", "POST"])
def edit_user():
    title= "Welcome Admin | Home Page"
    username = request.args.get('username')
    user_data = records.find_one({"username": username})
    
    return render_template("editUser.html", title=title, users=user_data)

@app.route("/update-user", methods=["GET", "POST"])
def updateUser():
    if request.method == "POST":
        username = request.form.get("username")
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        print([username, fullname, phone, email])
        records.update_one({"username": username}, {"$set": {"fullname": fullname,"email": email, "phone": phone}})
        return redirect(url_for("adminHome"))
    else:
        return redirect(url_for("edit_user"))


@app.route("/delete-user", methods = ['POST'])
def deleteUser():
    if request.method == 'POST':
        username = request.form.get("username")
        result = records.delete_one({"username": username})
        if result.deleted_count == 1:
            # User successfully deleted
            flash("User deleted successfully", "success")
        else:
            # User not found or deletion failed
            flash("User not found or deletion failed", "danger")
        
        # Redirect to admin home page or any other appropriate page
        return redirect(url_for("adminHome"))
    else:
        # If not a POST request, redirect to some error page or handle accordingly
        return redirect(url_for("adminHome"))


def get_incomplete_order_count():
    incomplete_orders = orders_collection.count_documents({"status": "Incomplete"})
    return incomplete_orders

def get_complete_order_count():
    complete_orders = orders_collection.count_documents({"status": "Completed"})
    return complete_orders

@app.route("/order-data")
def orderData():
    title= "Welcome Admin | Home Page"
    orderData = list(orders_collection.find().sort("_id", DESCENDING))
    incomplete_count = get_incomplete_order_count()  # Function to get count of incomplete orders from database
    complete_count = get_complete_order_count()
    return render_template("orders.html", orders = orderData, incomplete_count=incomplete_count, complete_count=complete_count, title=title)

@app.route("/order-status/<int:order_id>", methods=['POST'])
def orderComplete(order_id):
    if 'admin_username' in session and session['admin_username']:
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'completed':
                # Update order status to completed in the database
                orders_collection.update_one(
                    {"order_id": order_id},
                    {"$set": {"status": "Completed"}}
                )
                
            elif action == 'Incomplete':
                # Update order status to incomplete in the database
                orders_collection.update_one(
                    {"order_id": order_id},
                    {"$set": {"status": "Incomplete"}}
                )
    # Redirect to some page after processing the form submission
    return redirect(url_for('orderData'))



@app.route("/order-completed-data")
def orderCompData():
    title= "Welcome Admin | Home Page"
    # if 'admin_username' in session and session["admin_username"]:
    completedOrders = orders_collection.find({"status":"Completed"})
    return render_template("orderComplete.html", orders=completedOrders, title=title)

@app.route("/order-incomplete-data")
def orderIncomplete():
    title= "Welcome Admin | Home Page"
    # if 'admin_username' in session and session["admin_username"]:
    IncompleteOrders = orders_collection.find({"status":"Incomplete"})
    return render_template("orderIncomplete.html", orders=IncompleteOrders, title=title)


@app.route("/user-feedback")
def userFeedback():
    title= "Welcome Admin | Home Page"
    if is_admin_authenticated:
        userFeedback = list(feedbackCollection.find().sort("_id", DESCENDING))
    return render_template("feedback.html", feedbacks=userFeedback, title=title)
 
max_response_doc = ResponseDb.find_one(sort=[("response_id", -1)])

if max_response_doc and 'response_id' in max_response_doc:
    response_id_counter = int(max_response_doc['response_id']) + 1
else:
    response_id_counter = 0
    


@app.route("/send-response", methods=["POST"])
def send_response():
    response = request.form.get("response")
    customerFeedback = request.form.get("customerFeedback")
    CustomerName = request.form.get("CustomerName")
    email = request.form.get("email")  # Get customer email from the request
    
    try:
        # Insert responded data into the new database
        ResponseDb.insert_one({
            "response_id": response_id_counter,
            "Customer Name": CustomerName,
            "email": email,  # Store customer email for reference
            "feedback": customerFeedback,
            "response": response,  # Store admin response
            })
        msg = Message('Response from Admin', sender='verveinc@noreply.in', recipients=[email])
        msg.body = f'Your Feedback:{customerFeedback} \n Admin Reply: {response}'
        mail.send(msg)
        
        return jsonify({"message": "Response sent successfully", "response_id": str(response_id_counter)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update-response-sent", methods=["POST"])
def update_response_sent():
    response_id = request.form.get("response_id")
    
    try:
        # Update the response_sent field to True for the specified response_id
        response = ResponseDb.find_one_and_update(
            {"response_id": response_id},
            {"$set": {"response_sent": True}}
        )
        if response is not None:
            return jsonify({"message": "Response sent status updated successfully"}), 200
        else:
            return jsonify({"error": "Response not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5500)