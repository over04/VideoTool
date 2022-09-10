from flask import Blueprint, render_template, request, url_for, redirect

bl = Blueprint('syn', __name__, url_prefix='/syn')


@bl.route('/parse')
def parse():
    return render_template('syn/parse.html')


@bl.route('/')
def syn_path():
    return render_template('syn/path.html')