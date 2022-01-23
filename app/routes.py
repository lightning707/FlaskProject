from app import app_flask, render_template, flash, redirect, url_for, request, session, models, db
from werkzeug.security import generate_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app.forms import LoginForm, RegistrationForm, PostForm, UpdatePostForm
from app.models import User, Post


@app_flask.route('/', methods=['GET', 'POST'])
@app_flask.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.text.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        redirect(url_for('index'))
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template("index.html", title='Home Page', posts=posts, form=form)


@app_flask.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app_flask.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app_flask.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app_flask.route('/index/posts/<post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form = UpdatePostForm(post_body=post.body)
    if current_user.is_authenticated:
        if form.validate_on_submit():
            if form.delete.data:
                db.session.delete(post)
            if form.submit.data:
                post.body = form.text.data
            db.session.commit()
            return redirect(url_for('index'))
        else:
            form.text.data = post.body

        if post and post.user_id == current_user.id:
            print('page rendered')
            return render_template('update_post.html', title='Update post',
                                   form=form, post=post)
        else:
            redirect(url_for('index'))
    else:
        redirect(url_for('login'))

