import feedparser
from typing import Dict,List,Tuple
from util.config import Config
from util import media


def search(name: str) -> List[Dict[str, str or Tuple[int,int]]]:
    l = []
    config = Config()
    url = config['Jackett']['URL'].strip(' /\\')
    api_key = config['Jackett']['API_KEY']
    feed = feedparser.parse(f'{url}/api/v2.0/indexers/all/results/torznab/api?apikey={api_key}&t=search&cat=&q={name}')
    for each_entries in feed['entries']:
        temp = each_entries['title']
        l.append(
            {
                'original_name':temp,
                'name':media.get_name(temp,2),
                'episode':media.get_episode(temp),
                'season':media.get_season(temp),
                'url':each_entries['link']
            }
        )
        #l[each_entries['title']] = each_entries[
            #'link']  # dict_keys(['title', 'title_detail', 'id', 'guidislink', 'link', 'jackettindexer', 'type', 'comments', 'published', 'published_parsed', 'size', 'summary', 'summary_detail', 'links', 'tags', 'torznab_attr'])
    return l

if __name__ == '__main__':
    print(search('夏日重现'))
