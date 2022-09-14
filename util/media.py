import re
from typing import Set, List
import requests
from fuzzywuzzy import fuzz
from util import network
from util.config import Config


class Video:
    def __init__(self, media_type):
        self.language: str or None = None
        self.name: str or None = None
        self.origin_name: str or None = None
        self.overview: str or None = None
        self.id: str or None = None
        self.first_air_date: str or None = None
        self.image: str or None = None
        self.media_type: str = media_type

    @property
    def success(self):
        return all(map(lambda x: x is not None,
                       (self.language, self.name, self.origin_name, self.overview, self.id, self.first_air_date,)))

    @property
    def is_tv(self):
        return self.media_type == 'tv'

    @property
    def is_movie(self):
        return self.media_type == 'movie'

    @property
    def is_episode(self):
        return self.media_type == 'episode'

    @property
    def dic(self):
        return {
            'language': self.language,
            'name': self.name,
            'origin_name': self.origin_name,
            'overview': self.overview,
            'id': self.id,
            'first_air_date': self.first_air_date,
            'image': self.image,
            'media_type': self.media_type
        }

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class Tv(Video):
    def __init__(self):
        super(Tv, self).__init__('tv')
        self.number_of_episodes: None or int = None
        self.season: list = []

    @property
    def success(self):
        return all(map(lambda x: x is not None,
                       (self.language, self.name, self.origin_name, self.overview, self.id, self.first_air_date,
                        self.number_of_episodes)))


class Movie(Video):
    def __init__(self):
        super(Movie, self).__init__('movie')


class Episode(Video):
    def __init__(self):
        super().__init__('episode')
        self.episode_number: None or int = None
        self.season_number: None or int = None

    @property
    def success(self):
        return all(map(lambda x: x is not None,
                       (self.language, self.name, self.origin_name, self.overview, self.id, self.first_air_date,
                        self.episode_number)))


class SearchStringSuggest:
    def __init__(self, search_response):
        self.data = sorted([i for i in search_response.data],
                           key=lambda each_media: fuzz.ratio(search_response.keyword.lower(),
                                                             each_media.name.lower()), reverse=True)

    @property
    def success(self):
        return not len(self.data) == 0

    @property
    def head(self) -> 'Tv' or 'Movie':
        return self.data[0]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


class SearchStringResponse:
    def __init__(self, keyword):
        self.data: Set[Tv or Movie] = set()
        self.keyword = keyword

    def add(self, response: Tv):
        self.data.add(response)

    @property
    def is_empty(self):
        return len(self.data) == 0

    @property
    def success(self):
        return not self.is_empty

    def get_suggest_search(self) -> SearchStringSuggest:
        return SearchStringSuggest(self)
    @property
    def dic(self):
        return [i.dic for i in self.data]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)


def is_video(name: str):
    if re.search(r'\.([mM][kK][vV]|[mM][pP]4)\b', name):
        return True
    return False


def get_name(name: str, count: int = 1) -> str:
    '''

    :param name: 原名
    :param count: 正则匹配的次数
    :return: 匹配到到名字
    '''
    for i in range(count):
        name = re.sub(
            r'([-\[【_\](（]{1}|\s{0,})((.*?([Rr][Aa][Ww][Ss]|(字幕|发布|压制|汉化)[组社]|[Ss][Uu][Bb]|工作室))|Airota|喵萌奶茶屋|4hun|Nekomoe kissaten|LoliHouse|Kamigami|XKsub|orion origin|VCB[-\s]Studio|CASO|澄空学园|MagicStar|ANi|汉化组|合成)([-\]\[】_\[(（]{1}|\s{1,})',
            ' ', name)  # 除去字幕组
        name = re.sub(
            r'([-\[【_\](（]{1}|\s{1,})((1080|720|480)[pP]{0,1}|1920[xX]1080|1920[xX]816|1280[xX]720|4[kK]|1024[Xx]576)([-\]\[】_\[(（]{1}|\s{1,})',
            '',
            name)  # 去除分辨率
        name = re.sub(
            r'([-\[【_\](（]{1}|\s{1,})((([第eE]{0,1}[pP]{0,1})0{0,1}[1-9话]\d话{0,1}([vV]2){0,1}[^\da-zA-Z]{0,}|([eE第]{0,1}[pP]{0,1}0{1,2}\d话{0,1}([vV]2){0,1}|[Ss][Pp]))(\+小剧场){0,1}|(0\d|\d\d)-(0\d|\d\d)|([Mm][Ee][Nn][Uu]|Remix|[Oo][Vv][Aa]|[Cc][Mm]|[Ss][Pp]|[Pp][Vv]|(NC){0,1}([Ee][Dd]|[Oo][Pp]))\d{0,1}\d{0,1})([-\]\[】_\[(（]{1}|\s{1,})',
            ' ', name)  # 去除集数 (-[\]】_\[(（]{1}|\s{1,})
        name = re.sub(
            r'([-\[【_\](（]{1}|\s{1,})(第[\d一二三四五六七八九]季|OAD|[sS]\d{0,1}\d|\s(IV|III|II|V|VI|I)|\dnd Season|新章|\s.{1,3}篇|剧场|特典(映像){0,1})([-\]\[】_\[(（]{1}|\s{1,})',
            ' ', name)
        name = re.sub(r'([-\[【_\](（]{1}|\s{1,})MKV|mkv|MP4|mp4', ' ', name)  # 去除文件格式
        name = re.sub(
            r'([-\[【_\](（]{1}|\s{1,})(([Aa][Vv][Cc]|\d{0,1}[Aa][Aa][Cc]|CR|SRT|MUSE|\d{0,1}[Ff][Ll][Aa][Cc]|[Aa][Cc]3|[Aa][Ss]{2})(x2){0,1}|\dAudio)([-\]\[】_\[(（]{1}|\s{1,})',
            ' ', name)  # 去除内封
        name = re.sub(
            r'[XxHh]\.{0,1}(264|265)|10\s{0,1}bit|8\s{0,1}bit|[Hh][Ee][Vv][Cc]|([Hh][Ii]|[Mm][Aa])10[Pp]|OPUS', ' ',
            name)  # 去除编码
        name = re.sub(
            r'[Bb][Ii][Ll][Ii]|WEB-{0,1}DL|bangumi\.online|ViuTV|电影|YOUTUBE|Baha(mut){0,1}|B-Global|[Ww][Ee][Bb]([Rr][Ii][Pp]){0,1}|([Tt][Vv]|[Hh][Dd]|[Bb][Dd]|[Dd][Vv][Dd])([Rr][Ii][Pp]){0,1}|[Bb][Dd][Rr][Ee][Mm][Uu][Xx]|无修正{0,1}|(百度|阿里|115){0,1}(网盘|云盘)',
            ' ', name)  # 去除视频来源和特性非字幕组如bd、网盘 、修正
        name = re.sub(
            r'[\[【\s_]{1,}(((简体|中文|简繁|简日双语|简日|粤日|繁体|简中|日语|双语|简繁日)(字幕|内嵌|外挂|内封){0,2})|BIG5|GB|繁中|CHT|CHS|JAP|JP|[aA][sS][sS])[\]】_\s]{1,}',
            ' ', name)  # 去除语言和字幕
        name = re.sub(
            r'[\\&『』「」【】\[\]+★|.（）()/_-]\s{0,}|-\s|[01]{0,1}\d月新{0,1}番|正式版本|招募翻译校对|END|合集|repack|检索|招募|后期|仅限港澳台地区|字幕社招人内详|[Vv]er\.|\d\d\d\d年|volume',
            ' ', name)  # 多余字符
    return name.strip()


def get_season(name: str) -> int or bool:
    '''
    获取季
    :param name:
    :return: 季名OVA为0，最终季或最新季为-1,其他为正常 返回None时表示不能识别
    '''
    season_number = 1
    __re1 = re.search(r'([-\[【_\](（]{1}|\s{1,})([Ff]inal|最终季)([-\]\[】_\[(（]{1}|\s{1,})', name)
    __re2 = re.search(r'([-\[【_\](（]{1}|\s{1,})(第[\d一二三四五六七八九]季|[Ss]\d{0,2}\d)([-\]\[】_\[(（]{1}|\s{1,})',
                      name)
    __re3 = re.search(
        r'([-\[【_\](（]{1}|\s{1,})(([Tt]railer|[Pp]review|特典(映像){0,1}|Mini|[Ii][Vv]|Drama|PreView|([Nn][Cc]){0,1}([Oo][Pp]|[Ee][Dd])|[Oo][Vv][Aa]|[Mm][Ee][Nn][Uu]|[Cc][Mm]|[Pp][Vv]|[Ss][Pp])0?[1-9]?([vV][23])?)([E\-\]\[】_\[(（]{1}|\s{1,})',
        name)
    if __re3:
        season_number = False
    elif __re1:
        season_number = -1
    elif __re2:
        temp = re.sub(r'[Vv]2|[^0-9一二三四五六七八九十]', '', __re2.group())
        temp = temp.lstrip('0')
        if '9' > temp > '1':
            season_number = int(temp)
        elif temp == '':
            season_number = 0
        else:
            dic = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
            season_number = dic.get(temp, 1)
    else:
        season_number = 1
    return season_number


def get_episode(name: str) -> tuple or bool:
    '''

    :param name: 查询的字幕
    :return: 获取剧集的集数,左闭右闭
    '''
    episode_number = (1, 1)
    __re1 = re.search(
        r'[-\[【_\](（]([Ee第]?(0?[1-9]|[1-9]\d{1,2})[集话]?([vV][23])?)[-\]\[】_\[(（]',
        name)
    __re2 = re.search(
        r'([0-9-\[【_\](（]{1}|\s{1,})(([第eE]{0,1}[pP]{0,1})0{0,1}[1-9话]\d话{0,1}([vV]2){0,1}[^\da-zA-Z]{0,' \
        r'}|([eE第]{0,1}[pP]{0,1}0{1,2}\d话{0,1}([vV]2){0,1}))([-\]\[】_\[(（]{1}|\s{1,}){0,} ',
        name)
    __re3 = re.search(r'([-\[【_\](（]|\s{1,})(第\d\d-\d\d话|[Ee]\d\d-[Ee]?\d\d)([-\]\[】_\[(（]{1}|\s{1,})', name)
    if __re3:
        __re3 = re.sub(
            r'[Vv]2|[^0-9一二三四五六七八九十]',
            '', __re3.group()).strip()
        __re3 = tuple(map(int, __re3.split()))
        episode_number = __re3[:2]
    elif __re1:
        __re1 = re.sub(
            r'[Vv]2|[^0-9一二三四五六七八九十]',
            '', __re1.group()).strip()  # 多余字符
        episode_number = (int(__re1), int(__re1))
    elif __re2:
        __re2 = re.sub(
            r'[Vv]2|[^0-9一二三四五六七八九十]',
            '', __re2.group()).strip()  # 多余字符
        episode_number = (int(__re2), int(__re2))
    return episode_number


def __search_from_string(search_keyword: str, search_language: str = 'en-us') -> SearchStringResponse:
    """
        从字符串中搜索
        :return: 返回列表 name id first_air_time media_type original_name失败返回False
        """
    response = SearchStringResponse(search_keyword)
    config = Config()
    api_key: str = config['themoviedb']['API_KEY']  # themoviedb的api
    url = config['themoviedb']['URL']
    if not api_key:  # api_key未填写
        return response
    proxies = config['proxies']
    proxies = network.fix_proxies(proxies)
    # 搜索到的返回值
    for i in range(3):
        try:
            search_response = requests.get(f'{url}/search/multi', proxies=proxies,
                                           params={'api_key': api_key, 'query': search_keyword,
                                                   'language': search_language,
                                                   'page': 1}, timeout=5)  # 第一遍获取英文值
            break
        except:
            return response
    if search_response.status_code == 200:
        search_response_json = search_response.json()
        for each_media in search_response_json['results']:
            if each_media['media_type'] == 'tv':
                video = Tv()
            elif each_media['media_type'] == 'movie':
                video = Movie()
            else:
                return response
            video.language = search_language
            video.id = each_media['id']
            video.name = each_media.get('name', each_media.get('title'))
            video.origin_name = each_media.get('original_name', each_media.get('original_title'))
            video.overview = ''
            video.first_air_date = each_media.get('first_air_date', each_media.get('release_date'))
            video.season = []
            video.image = each_media['poster_path']
            video.number_of_episodes = 0
            response.add(video)
    return response


def __get_tv_detail(tv_id, language: str = 'en-US') -> Tv:
    config = Config()
    response = Tv()
    api_key: str = config['themoviedb']['API_KEY']  # themoviedb的api
    url = config['themoviedb']['URL']
    if not api_key:  # api_key未填写
        return response
    proxies = config['proxies']
    proxies = network.fix_proxies(proxies)
    for i in range(3):
        try:
            search_response = requests.get(f'{url}/tv/{tv_id}', proxies=proxies,
                                           params={'api_key': api_key, 'language': language,
                                                   'append_to_response': 'alternative_titles'}, timeout=5)
            break
        except:
            return response
    if search_response.status_code == 200:
        response_json = search_response.json()
        response.language = language
        response.name = response_json['name']
        response.origin_name = response_json['original_name']
        response.overview = response_json['overview']
        response.id = response_json['id']
        response.first_air_date = response_json['first_air_date']
        response.number_of_episodes = response_json['number_of_episodes']
        response.image = response_json['poster_path']
        response.season = response_json['seasons']
    return response


def __get_season_detail(tv_id, season_number, language: str = 'en-US'):
    config = Config()
    response = []
    api_key: str = config['themoviedb']['API_KEY']  # themoviedb的api
    url = config['themoviedb']['URL']
    if not api_key:  # api_key未填写
        return response
    proxies = config['proxies']
    proxies = network.fix_proxies(proxies)
    for i in range(3):
        try:
            season_response = requests.get(f'{url}/tv/{tv_id}/season/{season_number}', proxies=proxies,
                                           params={'api_key': api_key, 'language': language}, timeout=5)
            break
        except:
            return response

    if season_response.status_code == 200:
        response_json = season_response.json()['episodes']
        for i in response_json:
            episode = Episode()
            episode.name = i['name']
            episode.overview = i['overview']
            episode.id = i['id']
            episode.first_air_date = i['air_date']
            episode.season_number = int(season_number)
            episode.episode_number = int(i['episode_number'])
            response.append(episode)
    return response


def search(search_keyword: str, search_language: str = 'en-us') -> SearchStringResponse:
    """

    :param search_language: 搜索的语言
    :param search_keyword: 搜索的字符
    :return: 返回元组时第一个是搜索名,第二个是所有搜索结果
    """
    response = SearchStringResponse(search_keyword)
    search_keyword = search_keyword.split()
    for head in range(len(search_keyword) // 2 + 1):
        for tail in range(len(search_keyword), head, -1):
            now_search_name = ' '.join(search_keyword[head:tail])
            response = __search_from_string(now_search_name, search_language)
            if response.success:
                return response
    return response


def search_tv(tv_id, language: str = 'en-US') -> Tv:
    return __get_tv_detail(tv_id, language)


def search_season(tv_id, season_number, language: str = 'en-US') -> List[Episode]:
    return __get_season_detail(tv_id, season_number, language)


# a = get_name('[Airota&VCB-Studio] Kimi no Suizou o Tabetai [Trailer01][Ma10p_1080p][x265_flac].mkv', 2)
# print(a)
# print(get_season(
#    '[NC-Raws] 欢迎来到实力至上主义的教室 第二季 - 03 (B-Global 1920x1080 HEVC AAC MKV) [52A31B35].mkv'))
#


if __name__ == '__main__':
    pass
    # name = r'[Kamigami] Summer Time Rendering - 01 [1080p x265 Ma10p AAC]'
    # print(get_episode(name))
    # print(get_season(name))
    # for root, dirs, files in os.walk('/Volumes/download/qb'):
    #    for each_file in files:
    #        if is_video(each_file):
    #            season_number = get_season(each_file)
    #            if season_number is not None:
    #                name = get_name(each_file, 2)
    #                suggest = get_suggeest_search(search(name))
    #                print(each_file, '--->', name, season_number, get_episode(each_file), '--->', suggest[0], '--->',
    #                      suggest[1][0]['name'])
    #            else:
    #                print(each_file)
    #            print()
    # a = search('奥特曼', 'zh-CN')
    # for i in a.data:
    #    print(i.success)
    # print(a)
    # print(a.data)
    # print(a.get_suggest_search())
    b = search_season(117933, 1, 'zh-CN')
    print(b)
