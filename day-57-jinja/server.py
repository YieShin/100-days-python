import datetime

import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    year = datetime.datetime.now().year
    return render_template("index.html",
                           current_year=year,
                           )


# @app.route("/guess/<name>")
# def guess_name(name):
#     gender_response = requests.get(f"https://api.genderize.io?name={name}")
#     gender_data = gender_response.json()
#     gender = gender_data["gender"]
#
#     age_response = requests.get(f"https://api.agify.io?name={name}")
#     age_data = age_response.json()
#     age = age_data["age"]
#
#     return render_template("guess.html",
#                            name=name.capitalize(),
#                            age=age,
#                            gender=gender,
#                            )


@app.route("/blog/<num>")
def get_blog(num):
    url = "https://api.npoint.io/d829924f2f2f9633b1f6"
    response = requests.get(url)
    posts = response.json()
    return render_template("blog.html", posts=posts, num=num)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
