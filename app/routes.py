from app import app_flask
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm


@app_flask.route('/')
@app_flask.route('/index')
def index():
    user = {'username': 'andrew'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title="Home", user=user, posts=posts)


@app_flask.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
