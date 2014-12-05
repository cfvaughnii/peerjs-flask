import os
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from app import app, lm
from .forms import LoginForm
from .models import User

if not os.path.exists("tmp"):
    os.makedirs("tmp")

@lm.user_loader
def load_user(id):
    return User(id=id)

@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('user.html',
                           title='Steris WebRTC',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = remember_me = form.remember_me.data
        user = User(nickname=form.nickname.data)
        login_user(user, remember=remember_me)
        return render_template('user.html',
                           title='Steris WebRTC',
                           user=User(nickname=form.nickname.data))
    return render_template('login.html',
                           title='Sign In',
                           form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User(nickname=nickname)
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    login_user(user)
    return render_template('user.html',
                           title='Steris WebRTC',
                           user=user)
