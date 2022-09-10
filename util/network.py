from typing import Dict


def fix_proxies(proxies) -> Dict[str, str] or None:
    if not proxies['http']:
        proxies.pop('http')
    if not proxies['https']:
        proxies.pop('https')
    if not proxies:
        proxies = None
    return proxies
