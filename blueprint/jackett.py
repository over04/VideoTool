from flask import Blueprint, render_template, request, url_for, redirect

bl = Blueprint('jackett', __name__, url_prefix='/jackett')


@bl.route('/')
def index():
    return render_template('jackett.html')