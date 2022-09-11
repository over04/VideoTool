import os
import yaml
import sqlite3
from util.config import Config
from util.G import g
from util.file import Action, Path

DEFEAT_CONFIG = {
    'themoviedb': {
        'API_KEY': '',
        'URL': 'https://api.themoviedb.org/3',
        'LANG': 'zh-CN'
    },
    'proxies': {
        'http': '',
        'https': ''
    },
    'Jackett': {
        'API_KEY': '',
        'URL': ''
    },
    'qbittorrent': {
        'URL': '',
        'USERNAME': '',
        'PASSWORD': ''
    },
    'Sqlite': {
        'Path': 'data/data.db'
    },
    'Syn': {
        'Tv': '{tv_name} ({year})/Season {season_number}/{tv_name} - S{season_number}E{episode_number} - {'
              'episode_name}'
    }

}


def config():
    """
    初始化配置文件
    :return: True Or False
    """

    config_path: str = os.getenv('CONFIG_PATH', 'data/config.yaml')  # 获取配置文件地址
    Action.mkdir_father(config_path)
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            yaml.dump(DEFEAT_CONFIG, f)
    # with open(config_path, 'r') as f:
    #    config_data = yaml.load(f, Loader=yaml.FullLoader)


def service():
    temp = {
        'auto_parse': False,
        'auto_search': False,
        'auto_link':False
    }
    g['service'] = temp


def sql():
    """
    初始化sql
    :return:
    """
    database_path: str = Config()['Sqlite']['Path']  # 获取数据库地址
    Action.mkdir_father(database_path)
    conn = sqlite3.connect(database_path)
    with open('util/sqlite.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
