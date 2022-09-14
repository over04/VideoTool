from flask import Blueprint, render_template, request, url_for, redirect, abort
from util.config import Config
from util.G import g
from util import sqlite, syn, media
from util import follow
import threading

bl = Blueprint('api', __name__, url_prefix='/api')


def get_form():
    if request.method == 'POST':
        form = request.form
    elif request.method == 'GET':
        form = request.args
    else:
        form = False
    return form


def _auto_parse():
    syn.auto_parse()
    g['service']['auto_parse'] = False


def _auto_search():
    syn.auto_search()
    syn.auto_get_tv_lost_meida()
    syn.auto_get_meta()
    g['service']['auto_search'] = False


def _auto_link():
    syn.auto_link()
    g['service']['auto_link'] = False



@bl.route('/service/auto_parse_state', methods=['POST', 'GET'])
def auto_parse_state():
    state = g['service']['auto_parse']
    if state:
        if state.is_alive() is False:
            g['service']['auto_parse'] = False
        else:
            return {
                'code': 500,
                'results': 1  # 1表示进行
            }
    return {
        'code': 500,
        'results': 0  # 0表示没有进行
    }


@bl.route('/service/auto_search_state', methods=['POST', 'GET'])
def auto_search_state():
    state = g['service']['auto_search']
    if state:
        if state.is_alive() is False:
            g['service']['auto_parse'] = False
        else:
            return {
                'code': 500,
                'results': 1  # 1表示进行
            }
    return {
        'code': 500,
        'results': 0  # 0表示没有进行
    }


@bl.route('/service/auto_link_state', methods=['POST', 'GET'])
def auto_link_state():
    state = g['service']['auto_link']
    if state:
        if state.is_alive() is False:
            g['service']['auto_link'] = False
        else:
            return {
                'code': 500,
                'results': 1  # 1表示进行
            }
    return {
        'code': 500,
        'results': 0  # 0表示没有进行
    }


@bl.route('/service/start_auto_parse', methods=['POST', 'GET'])
def start_auto_parse():
    state = g['service']['auto_parse']
    if state is not False:  # 已经在执行了
        return {
            'code': 404,
            'results': []
        }
    thread = threading.Thread(target=_auto_parse)  # 创建一个进程来执行
    thread.start()
    g['service']['auto_parse'] = thread
    return {
        'code': 500,
        'results': []
    }


@bl.route('/service/start_auto_search', methods=['POST', 'GET'])
def start_auto_search():
    state = g['service']['auto_search']
    if state is not False:  # 已经在执行了
        return {
            'code': 404,
            'results': []
        }
    thread = threading.Thread(target=_auto_search)  # 创建一个进程来执行
    thread.start()
    g['service']['auto_search'] = thread
    return {
        'code': 500,
        'results': []
    }


@bl.route('/service/start_auto_link', methods=['POST', 'GET'])
def start_auto_link():
    state = g['service']['auto_link']
    if state is not False:  # 已经在执行了
        return {
            'code': 404,
            'results': []
        }
    thread = threading.Thread(target=_auto_link)  # 创建一个进程来执行
    thread.start()
    g['service']['auto_link'] = thread
    return {
        'code': 500,
        'results': []
    }


@bl.route('/syn/path', methods=['POST', 'GET'])  # 获取所有同步的目录
def syn_path():
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    cur.execute('SELECT * FROM SynPath')
    fetch = cur.fetchall()
    if fetch is None:
        fetch = []
    return {
        'code': 500,
        'results': fetch
    }


@bl.route('/syn/parse_file', methods=['POST', 'GET'])
def syn_parse():
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    cur.execute('SELECT * FROM Parse')
    fetch = cur.fetchall()
    if fetch is None:
        fetch = []
    return {
        'code': 500,
        'results': fetch
    }


@bl.route('/syn/add_path', methods=['POST', 'GET'])
def syn_add_path():
    if request.method == 'POST':
        source_path, target_tv_path, target_movie_path = request.form.get('source_path'), request.form.get(
            'target_tv_path'), request.form.get('target_movie_path')
        response = threading.Thread(target=syn.add_syn_path, args=(source_path, target_tv_path, target_movie_path))
        response.start()
    elif request.method == 'GET':
        source_path, target_tv_path, target_movie_path = request.args.get('source_path'), request.args.get(
            'target_tv_path'), request.args.get('target_movie_path')
        response = threading.Thread(target=syn.add_syn_path, args=(source_path, target_tv_path, target_movie_path))
        response.start()
    else:
        response = False
    if response:
        return {
            'code': 500,
            'results': []
        }
    return abort(404)


@bl.route('/themoviedb/search', methods=['POST', 'GET'])
def themoviedb_search():
    form = get_form()
    if form is not False:
        search_keyword = form.get('search_keyword')
        return {
            'code': 500,
            'results': media.search(search_keyword, 'zh-CN').dic
        }
    return abort(404)


@bl.route('/themoviedb/add_follow', methods=['POST', 'GET'])
def themoviedb_add_follow():
    form = get_form()
    if form is not False:
        tmdb_id = form.get('tmdb_id')
        media_type = form.get('media_type')
        threading.Thread(target=follow.add_follow, args=(tmdb_id, media_type)).start()
        return {
            'code': 500,
            'results': 1
        }
    return abort(404)
