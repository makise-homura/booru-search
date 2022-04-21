#!/usr/bin/env python3

from http import cookiejar
from urllib import parse, request
from json import loads
from http.cookies import SimpleCookie
from pybooru import Danbooru

# Example:
#  tags = [ 'kirisame_marisa', 'flandre_scarlet', 'kiss', '2girls' ]
#  tags = [ 'kageharu', 'kagiyama_hina', 'smile' ]

# A Danbooru mirror not banned in Russia, you may use any other supported by pybooru
booru = 'https://hijiribe.donmai.us'

if not 'tags' in locals() or not tags:
    print("Add tags variable according to README to the source file")
    quit()

db = Danbooru(site_url = booru)
req = tags.pop(0) + ' ' + tags.pop(0)
page = 1
found = []

class Rentry:
    """Simple HTTP Session Client, keeps cookies."""

    def __init__(self):
        self.cookie_jar = cookiejar.CookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookie_jar))
        request.install_opener(self.opener)

    def get_cookie(self):
        req = request.Request('https://rentry.co', headers={})
        return vars(self._request(req))['headers']['Set-Cookie']

    def post_snippet(self, data=None):
        postdata = parse.urlencode(data).encode()
        req = request.Request('https://rentry.co/api/new', postdata, {"Referer": 'https://rentry.co'})
        return self._request(req).data

    def _request(self, request):
        response = self.opener.open(request)
        response.status_code = response.getcode()
        response.data = response.read().decode('utf-8')
        return response

if tags:
    while True:
        print("Scanning page", page)
        posts = db.post_list(tags = req, page = page)
        if not posts:
            break
        for post in posts:
            post_tags = post['tag_string'].split()
            for tag in tags:
                if tag not in post_tags:
                    break
            else:
                print('Found post', post['id'])
                found.append(post)
        page += 1

    if found:
        print(len(found), 'posts total.')
        data = ''
        for post in found:
            data += '1. [![{0}]({1} "{2}")]({3}/posts/{0})\n'.format(post['id'], post['preview_file_url'], post['tag_string'], booru)
        rentry, cookie = Rentry(), SimpleCookie()
        cookie.load(rentry.get_cookie())
        csrftoken = cookie['csrftoken'].value
        payload = {'csrfmiddlewaretoken': csrftoken, 'url': '', 'edit_code': '', 'text': data}
        response = loads(rentry.post_snippet(payload))
        if response['status'] == '200':
            print('Your list is here:', response['url'])
        else:
            print('Upload error: {}'.format(response['content']))
    else:
        print('No such posts.')
else:
    print('You specified only 2 tags. Why not use booru directly?')
