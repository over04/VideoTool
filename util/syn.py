from util.config import Config
from util import sqlite, media
from util.file import parse, Path, Action
import time


def auto_parse():  # 自动解析，但是不会管电影
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    cur.execute('SELECT id, source_path FROM SynPath')
    fetch = cur.fetchall()
    if fetch is None:
        return False
    for i in fetch:
        auto_parse_from_path(syn_id=i['id'], path=i['source_path'])


def auto_parse_from_path(syn_id: str, path: str):  # 自动解析，但是不会管电影
    parse_result = parse(path)
    if parse_result.isfile:
        return
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    for each_file in parse_result.listall().file:
        if each_file.is_video:
            season = media.get_season(each_file.file_name)
            if season:
                episode = media.get_episode(each_file.file_name)
                name = media.get_name(each_file.file_name)
                cur.execute("INSERT OR IGNORE INTO Parse(syn_id, file_path,id,name,season,episode) VALUES(?,?,?,?,?,?)", (
                    syn_id, each_file.path, each_file.hash_path, name, season, episode[0]
                ))


def auto_search():
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    cur.execute('DELETE FROM Parse WHERE tmdb_id="0"')
    cur.execute('SELECT * FROM Parse WHERE tmdb_id is null')
    fetch = cur.fetchall()
    while len(fetch) != 0:
        suggest = media.get_suggest_search(media.search(fetch[0]['name']))
        if len(suggest[1]) == 0:  # 搜不到东西
            cur.execute("UPDATE Parse SET tmdb_id = '0' WHERE id = ?", (fetch[0]['id'],))
        else:
            suggest = suggest[1][0]
            cur.execute("UPDATE Parse SET tmdb_id=?, media_type=? WHERE name=?",
                        (suggest['id'], suggest['media_type'], fetch[0]['name']))  # 默认讲第一个搜索到的作为搜索到的id
            if suggest['media_type'] == 'tv':
                cur.execute("INSERT INTO TmdbTvTemp(tv_id, name, origin_name, first_air_date) VALUES (?,?,?,?)",
                            (suggest['id'], suggest['name'], suggest['origin_name'],
                             time.mktime(time.strptime(suggest['first_air_date'], '%Y-%m-%d')))
                            )
        cur.execute('SELECT * FROM Parse WHERE tmdb_id is null')
        fetch = cur.fetchall()


def auto_get_tv_lost_meida():
    """
    1.用于为Parse中有id但是tvtemp里没有的下载元数据
    2.为缺少数据的数据库填充数据
    :return:
    """
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    cur.execute('SELECT tmdb_id FROM Parse WHERE tmdb_id not in (SELECT tmdb_id FROM TmdbTvTemp)')
    fetch = cur.fetchall()
    if fetch is None:
        fetch = []
    cur.execute(
        'SELECT tv_id FROM TmdbTvTemp WHERE show_name is null or overview is null or first_air_date is null or '
        'number_of_episodes is null')
    temp = cur.fetchall()
    if temp is None:
        temp = []
    fetch.extend(temp)
    for i in {i['tv_id'] for i in fetch}:
        response = media.search_tv(i)
        if response:  # 有查询结果
            cur.execute(
                'INSERT or REPLACE INTO TmdbTvTemp(tv_id, name, origin_name, show_name, overview, first_air_date, '
                'number_of_episodes) VALUES(?,?,?,?,?,?,?)',
                (response['id'], response['name'], response['origin_name'], response['show_name'], response['overview'],
                 response['first_air_date'], response['number_of_episodes'])
            )


def auto_get_meta():
    """
    自动获取元数据
    :return:
    """
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    cur.execute('SELECT tv_id FROM TmdbTvTemp')  # 获取所有的tv_id,下面是自动获取所有获取tv_id的元数据
    fetch = cur.fetchall()
    if fetch is None:
        fetch = []
    for i in fetch:
        tv_id = i['tv_id']
        response = media.get_tv_detail(tv_id)
        if response:  # 能获取到返回值
            for _ in response['season']:
                temp = media.get_season_detail(tv_id=i['tv_id'], season_number=_['season_number'])
                if temp:
                    for each_episode in temp:
                        cur.execute(
                            'INSERT OR REPLACE INTO TmdbEpisodeTemp(tv_id, id, name, overview, season, episode, '
                            'air_date) VALUES (?,?,?,?,?,?,?)',
                            (tv_id, each_episode['id'], each_episode['name'], each_episode['overview'],
                             each_episode['season_number'], each_episode['episode_number'], each_episode['air_date'])
                        )


def add_syn_path(source_path, target_tv_path, target_movie_path):
    source_path, target_tv_path, target_movie_path = parse(source_path), parse(target_tv_path), parse(target_movie_path)
    if source_path != False and target_tv_path != False and target_movie_path != False:
        if source_path.isdir and target_tv_path.isdir and target_movie_path.isdir:
            config = Config()
            conn = sqlite.connect(config['Sqlite']['Path'])
            cur = conn.cursor()
            cur.execute('INSERT INTO SynPath(id, source_path, target_tv_path, target_movie_path) VALUES(?,?,?,?)',
                        (source_path.hash_path, source_path.path, target_tv_path.path, target_movie_path.path)
                        )
            return True
    return False


def auto_link():
    """

    在config里面可以设置的内容
    1.tv:
        tv_id, tv_name, episode_name,
        eason_number, episode_number,
        year, month, day, time


    :return:
    """
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    tv_config:str = config['Syn']['Tv']
    cur = conn.cursor()
    cur.execute('SELECT syn_id, file_path, media_type, tmdb_id, episode, season  FROM Parse')  # tmdb_id在tv里面对应的是tv_id
    fetch = cur.fetchall()
    if fetch is None:
        fetch = []
    for i in fetch:
        # i['syn_id'], i['media_type'], i['tmdb_id'], i[
        #    'episode'], i['season']
        source_path = parse(i['file_path'])
        if source_path == False:
            continue
        cur.execute("SELECT target_tv_path, target_movie_path FROM SynPath WHERE id = ?", (i['syn_id'],))
        get_target = cur.fetchall()
        if get_target is None:
            continue
        get_target = get_target[0]
        target_tv_path, target_movie_path = get_target['target_tv_path'], get_target['target_movie_path']
        if i['media_type'] == 'tv':
            cur.execute('SELECT * FROM TmdbEpisodeTemp WHERE tv_id = ? and episode = ? and season = ?',
                        (i['tmdb_id'], i['episode'], i['season']))
            episode_info = cur.fetchall()
            if episode_info is None:
                continue
            episode_info = episode_info[0]
            cur.execute("SELECT * FROM TmdbTvTemp WHERE tv_id = ?",(i['tmdb_id'], ))
            tv_info = cur.fetchall()
            if tv_info is None:
                continue
            tv_info = tv_info[0]
            full_time = time.strptime(episode_info['air_date'], '%Y-%m-%d')
            episode = str(episode_info['episode'])
            episode_count = str(tv_info['number_of_episodes'])
            episode = '0' * (len(episode_count) - len(episode)) + episode

            form = {
                'tv_id': episode_info['tv_id'],
                'tv_name': tv_info['name'],
                'episode_name': episode_info['name'],
                'season_number': f"{episode_info['season']}",
                'episode_number': episode,
                'time': episode_info['air_date'],
                'year': full_time.tm_year,
                'month': full_time.tm_mon,
                'day': full_time.tm_mday
            }

            last_name = tv_config.format(**form) # 自动合成的名字(目录)
            full_path = f"{target_tv_path.rstrip('/')}/{last_name}.{source_path.file_type}"
            Action.mkdir_father(full_path)
            Action.link(source_path.path, full_path)



if __name__ == '__main__':
    # auto_parse('/Users/zhangbeiyuan/Movies/Videos')
    # auto_search()
    # auto_get_tv_lost_meida()
    # auto_get_meta()
    auto_link()
