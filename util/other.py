import hashlib
import time


def get_id():
    return md5(str(time.time()))


def __hash(string: str, mode: str) -> bool or str:
    _ = {
        'md5': hashlib.md5()
    }.get(mode)
    if _ is None:
        return None
    _.update(string.encode('utf-8'))
    return _.hexdigest()


def md5(string: str) -> str:
    return __hash(string, 'md5')


if __name__ == '__main__':
    print(get_id())