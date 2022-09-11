from util.config import Config
from util import network
from typing import List, Dict
import requests


def search_from_string(name: str) -> List[Dict[str, str]] or bool:
    """
    从字符串中搜索
    :return: 返回列表 name id first_air_time media_type original_name失败返回False
    """
    global search_response
    config = Config()
    api_key: str = config['themoviedb']['API_KEY']  # themoviedb的api
    url = config['themoviedb']['URL']
    if not api_key:  # api_key未填写
        return False
    proxies = config['proxies']
    proxies = network.fix_proxies(proxies)
    response = []  # 搜索到的返回值
    for i in range(3):
        try:
            search_response = requests.get(f'{url}/search/multi', proxies=proxies,
                                           params={'api_key': api_key, 'query': name, 'language': 'en-us',
                                                   'page': 1}, timeout=5)  # 第一遍获取英文值
            break
        except:
            return response
    if search_response.status_code == 200:
        search_response_json = search_response.json()
        if len(search_response_json['results']) == 0:
            return False
        for each_media in search_response_json['results']:
            if each_media['media_type'] in ['movie', 'tv']:
                response.append(
                    {
                        'name': each_media.get('name', each_media.get('title')),
                        'show_name': '',
                        'origin_name': each_media.get('original_name', each_media.get('original_title')),
                        'overview': '',
                        'id': each_media['id'],
                        'first_air_date': each_media.get('first_air_date', each_media.get('release_date')),
                        'season': [],
                        'media_type': each_media['media_type']
                    }
                )
        return response
    else:
        return False


def get_tv_detail(tv_id) -> List[Dict[str, str]] or bool:
    config = Config()
    api_key: str = config['themoviedb']['API_KEY']  # themoviedb的api
    url = config['themoviedb']['URL']
    if not api_key:  # api_key未填写
        return False
    proxies = config['proxies']
    proxies = network.fix_proxies(proxies)
    lang = config['themoviedb']['LANG']
    for i in range(3):
        try:
            search_response = requests.get(f'{url}/tv/{tv_id}', proxies=proxies,
                                           params={'api_key': api_key, 'language': lang,
                                                   'append_to_response': 'alternative_titles'}, timeout=5)
            break
        except:
            return False
    if search_response.status_code == 200:
        response_json = search_response.json()
        name = ''
        for i in response_json['alternative_titles']['results']:
            if i['iso_3166_1'] == 'US':
                name = i['title']
        return {
            'name': name,
            'show_name': response_json['name'],
            'origin_name': response_json['original_name'],
            'overview': response_json['overview'],
            'id': response_json['id'],
            'first_air_date': response_json['first_air_date'],
            'season': response_json['seasons'],
            'number_of_episodes': response_json['number_of_episodes'],
            'media_type': 'tv'
        }
    return False


def get_season_detail(tv_id, season_number):
    config = Config()
    api_key: str = config['themoviedb']['API_KEY']  # themoviedb的api
    url = config['themoviedb']['URL']
    if not api_key:  # api_key未填写
        return False
    proxies = config['proxies']
    proxies = network.fix_proxies(proxies)
    lang = config['themoviedb']['LANG']
    response = []
    for i in range(3):
        try:
            season_response = requests.get(f'{url}/tv/{tv_id}/season/{season_number}', proxies=proxies,
                                           params={'api_key': api_key, 'language': lang}, timeout=5)
            break
        except:
            return response

    if season_response.status_code == 200:
        response_json = season_response.json()['episodes']
        for i in response_json:
            response.append(
                {
                    'name': i['name'],
                    'overview': i['overview'],
                    'id': i['id'],
                    'air_date': i['air_date'],
                    'media_type': 'episode',
                    'season_number': int(season_number),
                    'episode_number': int(i['episode_number']),
                }
            )
        return response
    return False


if __name__ == '__main__':
    pass
    #print(get_tv_detail('117933'))
# print(get_season_detail('117933', 1))
# a = search_from_string('夏日重现')
# print(a)
