from flask import Blueprint, render_template, request, url_for, redirect, abort

bl = Blueprint('service', __name__, url_prefix='/service')


@bl.route('/')
def index():
    return render_template('service.html')
