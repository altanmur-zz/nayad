"""
Flask Module Docs:  http://flask.pocoo.org/docs/api/#flask.Module

This file is used for both the routing and logic of your
application.
"""

from google.appengine.api import mail
from google.appengine.api import users
from flask import Blueprint, url_for, render_template, request, redirect
from models import Todo
from forms import TodoForm, EmailForm
import urllib, hashlib

views = Blueprint('views', __name__)


@views.route('/')
def index():
    """Render website's index page."""
    user = users.get_current_user()
    logout_url, login_url = None, None

    if user:
        logout_url = users.create_logout_url("/")
    else:
        login_url = users.create_login_url("/")
    return render_template('index.html', login_url=login_url, user=user, logout_url=logout_url)

@views.route('/user_profile', methods=['GET'])
def user_profile():
    user = users.get_current_user()
    email = user.email().lower()
    gravatar_url = "http://www.gravatar.com/avatar/%s?d=retro&s=64" % hashlib.md5(email).hexdigest()

    return render_template('user/profile.html', user=user, gravatar_url=gravatar_url)

@views.after_request
def add_header(response):
    """Add header to force latest IE rendering engine and Chrome Frame."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    return response


@views.app_errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
