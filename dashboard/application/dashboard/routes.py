import requests
from . import forms
from . import bp
from .api.authClient import authClient
from .. import login_manager
from flask import render_template, session, redirect, url_for, flash, request

from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    return None


@bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('dashboard.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            # Search for existing user
            user = authClient.does_exist(username)
            if user:
                # Existing user found
                flash('Please try another username', 'error')
                return render_template('register.html', form=form)
            else:
                # Attempt to create new user
                user = authClient.post_user_create(form)
                if user:
                    flash('Thanks for registering, please login', 'success')
                    return redirect(url_for('dashboard.login'))

        else:
            flash('Errors found', 'error')

    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            api_key = authClient.post_login(form)
            if api_key:
                session['user_api_key'] = api_key
                user = authClient.get_user()
                session['user'] = user['result']

                flash('Welcome back, ' + user['result']['username'], 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('Cannot login', 'error')
        else:
            flash('Errors found', 'error')
    return render_template('login.html', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('dashboard.login'))
