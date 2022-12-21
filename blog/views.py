from flask import redirect, render_template, request, flash, url_for

from blog import app
from blog.models import Post


@app.route("/")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/posts/<id>")
def post_detail(id):
    try:
        post = Post.query.filter_by(id=id).first()
    except:
        post = None

    return render_template('post-detail.html', post=post)