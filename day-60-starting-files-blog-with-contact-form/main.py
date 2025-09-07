import os
import smtplib
from dotenv import load_dotenv
import requests
from flask import Flask, render_template, request

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
app = Flask(__name__)

load_dotenv()
# Email configuration (replace with your details)
SMTP_SERVER = "smtp.gmail.com"  # For Gmail
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL")  # Your email
EMAIL_PASSWORD = os.getenv("PASSWORD")  # Your app password


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        send_email(name, email, phone, message)
        return "<h1>Message Sent!</h1>"


def send_email(name, email, phone, message):
    try:
        email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            connection.sendmail(
                from_addr=EMAIL_ADDRESS,
                to_addrs=EMAIL_ADDRESS,  # send to yourself
                msg=email_message
            )
            print("Email send successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
