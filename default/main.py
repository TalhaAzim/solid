from flask import Flask
import json
from immutables import Map

app = Flask(__name__)

class Model(object):

    from google.cloud import firestore as fs
    db = fs.Client()

class Post(Model):

    collection = "posts"
    
    @classmethod
    def get_published(cls, limit=10):
        return cls.db.collection(cls.collection)\
            .where("published", "==", True)\
            .order_by("date_published", direction=cls.fs.Query.DESCENDING)\
            .limit(limit)\
            .stream()


@app.route("/api/published_posts")
def published_posts():
    posts = Post.get_published()
    return json.dumps(
        [ {'id': post.id, **post.to_dict()} for post in posts],
        default=str
    )

@app.route("/")
def index():
    posts = Post.get_published()
    return "".join([
        "<html>",
        "<head>",
        "<title>Solid Blog Simulation</title>",
        "<script src=\"https://cdn.jsdelivr.net/npm/vue@2/dist/vue.min.js\"></script>"
        "</head>",
        "<body>",
        "<header><h1>Solid Blog Simulation</h1></header>",
        "<div id=\"app\">",
        "<article v-bind:id=\"post.id\" v-for=\"post of posts\">",
        "<header><h1>{{ post.title }} by {{ post.author.name }}</h1></header>",
        "<div v-html=\"post.body\"></div>",
        "</article>",
        "</div>",
        "<script type=\"text/javascript\">",
        f'var app = new Vue({{'
        f'el: "#app",'
        f'data: {{ posts: {json.dumps([{"id": post.id, **post.to_dict()} for post in posts], default=str)}}}'
        f'}})',
        "</script>",
        "</body>",
        "</html>"
    ])

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)