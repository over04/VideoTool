from flask import Flask, redirect, url_for, render_template
from util import init
from blueprint import *

init.config()
init.service()
init.sql()
app = Flask(__name__)
app.register_blueprint(syn_bl)
app.register_blueprint(api_bl)
app.register_blueprint(service_bl)


@app.route('/test')
def test():
    return render_template('Base.html')


# @app.route('/')
# def index():
#    return redirect(url_for('filemanager.index'))


if __name__ == '__main__':
    app.run()
