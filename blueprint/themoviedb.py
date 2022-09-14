from flask import Blueprint, render_template, request, url_for, redirect

bl = Blueprint('themoviedb', __name__, url_prefix='/themoviedb')


@bl.route('/')
def index():
    return render_template('themoviedb.html')