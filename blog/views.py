from blog import app
from flask import redirect, render_template, request, flash, url_for


@app.route("/")
def home():
    return render_template('home.html')


@app.route("posts/<id>")
def post_detail(id):
    return render_template('post-detail.html')