import requests
from flask import Flask, render_template

from post import Post

app = Flask(__name__)

url = "https://api.npoint.io/a6bf77d02c04baf8b05d"
response = requests.get(url)
data = response.json()
all_posts = []

for item in data:
    post = Post(
        item["id"],
        item["title"],
        item["subtitle"],
        item["body"],
        item["image_url"]
    )
    all_posts.append(post)


@app.route("/")
def home():
    return render_template("index.html", all_posts=all_posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/post/<int:post_id>")
def show_post(post_id):
    # Find the post with the given id
    requested_post = None
    for post in all_posts:
        if post.post_id == post_id:
            requested_post = post
            break

    if requested_post is None:
        return "Post not found", 404

    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port="5001")
