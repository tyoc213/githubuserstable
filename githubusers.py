# From https://docs.github.com/en/rest/reference/users#list-users
# example: https://api.github.com/users?per_page=10&since=0

import requests

def get_github_users(per_page, since):
    '''Return a dict of id:user with specific keys from github users'''
    r = requests.get('https://api.github.com/users?per_page=%d&since=%d'%(per_page, since))
    if r.status_code == 200:
        return {r['id']:{
            'user': r['login'],
            'id': r['id'],
            "image_url": r['avatar_url'],
            "profile": r['html_url'],
            "typ3": r['type']
            } for r in r.json()}
    else:
        return {}