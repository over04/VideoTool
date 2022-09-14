from util import media, syn
from util.config import Config
from util import sqlite


def add_follow(tmdb_id: str, media_type: str):
    config = Config()
    conn = sqlite.connect(config['Sqlite']['Path'])
    cur = conn.cursor()
    if media_type == 'tv':
        response = media.search_tv(tmdb_id, config['themoviedb']['LANG'])
        if response.success:
            cur.execute(
                'INSERT OR REPLACE INTO TmdbTvTemp(tv_id, name, origin_name, overview, first_air_date, '
                'number_of_episodes, follow) VALUES (?,?,?,?,?,?,?)',
                (response.id, response.name, response.origin_name, response.overview,
                 response.first_air_date, response.number_of_episodes, 1)
            )
    syn.auto_get_meta()


if __name__ == '__main__':
    add_follow('117933', 'tv')
