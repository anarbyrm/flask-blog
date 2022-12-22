from flask import redirect, render_template, request, flash, url_for

from flask_login import login_user, current_user, logout_user, login_required
from flask_bcrypt import check_password_hash, generate_password_hash

from sqlalchemy import desc

from blog import app, db
from blog.models import Post, User
from blog.forms import LoginForm, RegistrationForm, PostForm


@app.route("/")
def home():
    posts = Post.query.order_by(desc('date_created')).all()
    return render_template('home.html', posts=posts)


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
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


@app.route('/posts/<int:post_id>/delete/')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.username == post.user.username:
        db.session.delete(post)
        db.session.commit()
        flash('Your post deleted!')
        return redirect(url_for('home'))
    else:
        flash('Deletion is forbidden for this post!')
        return redirect(url_for('home'))


@app.route('/posts/<int:post_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)

    if current_user.username == post.user.username:
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.add(post)
            db.session.commit()

            flash('Your post updated!')

            return redirect(url_for('post_detail', post_id=post.id))

    elif current_user.username != post.user.username:
        flash('Editing is forbidden for the post!')

    return render_template('post-form.html', form=form)


@app.route('/posts/create/', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user = current_user

        post = Post(title=title, content=content, user=user)
        db.session.add(post)
        db.session.commit()

        flash('Your post created!')
        return redirect(url_for('post_detail', post_id=post.id))
    else:
        flash('Form is not valid. Please try again!')

    return render_template('post-form.html', form=form)
