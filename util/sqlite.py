import threading
import sqlite3
from util.config import Config

lock = threading.Lock()


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _connect(path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = _dict_factory
    return conn


class Connect:
    def __init__(self, path):
        self.__lock = lock
        self.__path = path
        conn = _connect(path)
        conn.close()

    def execute(self, sql, parameters=None):
        with self.__lock:
            conn = _connect(self.__path)
            if parameters is None:
                conn.execute(sql)
            else:
                conn.execute(sql, parameters)
            conn.commit()

    def executescript(self, sql_script):
        with self.__lock:
            conn = _connect(self.__path)
            conn.executescript(sql_script)
            conn.commit()

    def cursor(self):
        return Cursor(path=self.__path)


class Cursor:
    def __init__(self, path):
        self.__path = path
        self.__lock = lock
        self.__fetch = None

    def execute(self, sql, parameters=None):
        with self.__lock:
            conn = _connect(self.__path)
            cursor = conn.cursor()
            if parameters is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, parameters)
            self.__fetch = cursor.fetchall()
            if isinstance(self.__fetch, list) and len(self.__fetch) == 0:
                self.__fetch = None
            conn.commit()

    def executescript(self, sql_script):
        with self.__lock:
            conn = _connect(self.__path)
            conn.executescript(sql_script)

    def fetchall(self):
        fetch, self.__fetch = self.__fetch, None
        return fetch


def connect(path: str) -> Connect:
    return Connect(path)


if __name__ == '__main__':
    a = Config()
    a = connect(a['Sqlite']['Path'])
    with open('./util/sqlite.sql', 'r', encoding='utf-8') as f:
        a.executescript(f.read())
    cur = a.cursor()
    # cur.execute('SELECT * FROM Parse ')
    # print(cur.fetchall())
