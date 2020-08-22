from flask import Flask, jsonify, render_template
import os
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


@app.route("/api/posts")
def posts():
    posts = Post.get_published()
    return jsonify([{'id': post.id, **post.to_dict()} for post in posts])


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)