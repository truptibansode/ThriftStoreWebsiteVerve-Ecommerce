
# MAIL SENDING FUNCTION

@app.route("/send_email/<email>", methods = ["GET"])
def send_email(email):
    msg_title = "this is a test mail"
    sender = "verveinc@noreply.in"
    msg = Message(msg_title, sender=sender,recipients=[email])
    msg_body = "this is email body"
    data = {
        'app_name': "Verve Inc",
        'title': msg_title, 
        'body': msg_body
    }

    msg.html = render_template("emailtwo.html", data=data)
    try:
        mail.send(msg)
        return "email sent successfully...."
    except Exception as e:
        print(e)
        return "email not sent...."
