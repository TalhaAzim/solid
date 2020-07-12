from flask import Flask
import json
from google.cloud import firestore

app = Flask(__name__)

def get_published_posts():
    db = firestore.Client()
    posts = db.collection("posts").where("published", "==", True).order_by("date_published", direction=firestore.Query.DESCENDING).limit(10).stream()
    return [post.to_dict() for post in posts]

def render_post(post):
    return "".join([
        "<article>",
        f'<header><h1>{post["title"]} by {post["author"]["name"]}</h1></header>',
        f'<div>{post["body"]}</div>',
        "</article>"
    ])

@app.route("/")
def index():
    posts = get_published_posts()
    return "".join([
        "<html>",
        "<head>",
        "<title>Solid Blog Simulation</title>",
        "<script type=\"text/javascript\">",
        f'var posts={json.dumps(posts, default=str)}'
        "</script>"
        "</head>",
        "<body>",
        "<header><h1>Solid Blog Simulation</h1></header>",
        "".join([render_post(post) for post in posts]),
        "</body>",
        "</html>"
    ])

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)