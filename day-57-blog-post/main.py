from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)


url = "https://api.npoint.io/d829924f2f2f9633b1f6"
response = requests.get(url)
data = response.json()
all_posts = []

for item in data:
    post = Post(item["id"], item["title"],
                item["subtitle"], item["body"])

    all_posts.append(post)

@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)

@app.route('/post/<int:index>')
def post_page(index):

    requested_post = None
    for blog_post in all_posts:
        if blog_post.post_id == index:
            requested_post = blog_post
            print(f"Found post: {blog_post.title}")
            break

    if requested_post is None:
        return "Post not found", 404

    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
