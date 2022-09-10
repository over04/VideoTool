import re
from typing import List, Dict, Tuple
from util.metabase.themoviedb import *
from fuzzywuzzy import fuzz



class SearchResponse:
    def __init__(self):
        self.__name: str = ''
        self.__show_name: str = ''
        self.__origin_name: str = ''
        self.__overview: str = ''
        self.__id: str = ''
        self.__first_air_date: str = ''
        self.__season: list = []
        self.__media_type: str = 'tv'

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
            r'([-\[【_\](（]{1}|\s{1,})(第[\d一二三四五六七八九]季|OAD|[sS]\d{0,1}\d|\s(IV|III|II|V|VI|I)|\dnd Season|新章|\s.{1,3}篇|剧场)([-\]\[】_\[(（]{1}|\s{1,})',
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
        r'([-\[【_\](（]{1}|\s{1,})(Mini|[Mm][Ee][Nn][Uu]|[Ii][Vv]|[Cc][Mm]|[Oo][Vv][Aa]|[Pp][Vv]|[Ss][Pp]|[Tt]railer|[Pp]review|([Nn][Cc]){0,1}([Oo][Pp]|[Ee][Dd]))([-\]\[】_\[(（]{1}|\s{1,})',
        name)
    if __re1:
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
    elif __re3:
        season_number = False
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
        r'([0-9-\[【_\](（]{1}|\s{1,})(([第eE]{0,1}[pP]{0,1})0{0,1}[1-9话]\d话{0,1}([vV]2){0,1}[^\da-zA-Z]{0,}|([eE第]{0,1}[pP]{0,1}0{1,2}\d话{0,1}([vV]2){0,1}))([-\]\[】_\[(（]{1}|\s{1,}){0,}',
        name)
    __re2 = re.search(r'([-\[【_\](（]{1}|\s{1,})第\d\d-\d\d话|[Ee]\d\d-[Ee]{0,1}\d\d([-\]\[】_\[(（]{1}|\s{1,})', name)
    if __re2:
        __re2 = re.sub(
            r'[Vv]2|[^0-9一二三四五六七八九十]',
            '', __re2.group()).strip()
        __re2 = tuple(map(int, __re2.split()))
        episode_number = __re2[:2]
    elif __re1:
        __re1 = re.sub(
            r'[Vv]2|[^0-9一二三四五六七八九十]',
            '', __re1.group()).strip()  # 多余字符
        episode_number = (int(__re1), int(__re1))
    return episode_number


def search(name: str) -> Tuple[str, List[Dict[str, str]]]:
    """

    :param name: 搜索的字符
    :return: 返回元组时第一个是搜索名,第二个是所有搜索结果
    """
    name = name.split()
    for head in range(len(name) // 2 + 1):
        for tail in range(len(name), head, -1):
            now_search_name = ' '.join(name[head:tail])
            response = search_from_string(now_search_name)
            if response:
                return now_search_name, response
    return ' '.join(name), []


def search_tv(tv_id):
    return get_tv_detail(tv_id)


def search_season(tv_id, season_number):
    return get_season_detail(tv_id, season_number)


def get_suggest_search(search_response: Tuple[str, List[Dict[str, str]]]):
    search_name, response = search_response
    if len(response) == 0:
        return search_name, response
    return search_name, sorted(response,
                               key=lambda each_media: fuzz.ratio(search_name.lower(), each_media['name'].lower()),
                               reverse=True)


# a = get_name('[Airota&VCB-Studio] Kimi no Suizou o Tabetai [Trailer01][Ma10p_1080p][x265_flac].mkv', 2)
# print(a)
# print(get_season(
#    '[NC-Raws] 欢迎来到实力至上主义的教室 第二季 - 03 (B-Global 1920x1080 HEVC AAC MKV) [52A31B35].mkv'))
#


if __name__ == '__main__':
    pass
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
    # a = search('PSYCHO PASS Preview10')
    # print(get_suggeest_search(a))
