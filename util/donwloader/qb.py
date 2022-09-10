from util.config import Config
from qbittorrent import Client


def add(link:str) -> bool:
    qb = __get_qb()
    qb.download_from_link(link)
    qb.logout()
    return True

def __get_qb():
    config = Config()
    qb = Client(config['qbittorrent']['URL'])
    qb.login(username=config['qbittorrent']['USERNAME'], password=config['qbittorrent']['PASSWORD'])
    return qb

if __name__ == '__main__':
    print(add('magnet:?xt=urn:btih:9fb9254c1f93c02bd5c62cbf4ce13cdb0d77071b&tr=http%3a%2f%2ft.nyaatracker.com%2fannounce&tr=http%3a%2f%2ftracker.kamigami.org%3a2710%2fannounce&tr=http%3a%2f%2fshare.camoe.cn%3a8080%2fannounce&tr=http%3a%2f%2fopentracker.acgnx.se%2fannounce&tr=http%3a%2f%2fanidex.moe%3a6969%2fannounce&tr=http%3a%2f%2ft.acg.rip%3a6699%2fannounce&tr=https%3a%2f%2ftr.bangumi.moe%3a9696%2fannounce&tr=udp%3a%2f%2ftr.bangumi.moe%3a6969%2fannounce&tr=http%3a%2f%2fopen.acgtracker.com%3a1096%2fannounce&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce'))