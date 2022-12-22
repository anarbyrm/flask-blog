from flask import redirect, render_template, request, flash, url_for

from flask_login import login_user, current_user, logout_user, login_required
from flask_bcrypt import check_password_hash, generate_password_hash

from blog import app, db
from blog.models import Post, User
from blog.forms import LoginForm, RegistrationForm



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


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        if user:
            user = user.first()
            if check_password_hash(user.password, form.password.data):
                login_user(user ,remember=True)

                flash("Logged in successfully!")
                return redirect(url_for('home'))
            else:
                flash('Username or password is incorrect')
        else:
            flash("Log in unsuccessful. Please try again.")

    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # if User.query.filter_by(username=form.username.data) or User.query.filter_by (email=form.email.data):
        #     flash('Registration unsuccessful. User exists with either username or email you entered.')

        # else:
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account created. Now you can sign in to your account.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    username = current_user.username
    return render_template('account.html', username = username)
