from qbittorrent import Client
from util.config import Config


def add(link: str):
    qb = __get_qb()
    log = qb.download_from_link(link)
    qb.logout()
    return 'done.'


def __get_hash(link: str):
    return link[20:60]


def __get_qb():
    config = Config()
    qb = Client(config['qbittorrent']['URL'])
    qb.login(username=config['qbittorrent']['USERNAME'], password=config['qbittorrent']['PASSWORD'])
    return qb


if __name__ == '__main__':
    print(
        add('magnet:?xt=urn:btih:28b45bf02bddf1d3ed0b3fbdd5f5a50cee4621ea&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2ftracker.kamigami.org%3a2710%2fannounce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2fanidex.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=https%3a%2f%2ftr.bangumi.moe%3a9696%2fannounce&tr=udp%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce'))
    # availability为-1时表示下完了，为0时表示没下完
    # for i in qb.torrents():
    #    print(i['hash'],i['name'],i['save_path'])
    #    print('-----------------')
    # print(qb.get_torrent_files('e7debe5b90a0994b0fd23eee387727e47dcbe96f'))
