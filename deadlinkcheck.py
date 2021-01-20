# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:28:36 2021

youtube link checker bot proof of concept

https://www.youtube.com/watch?v=EPZP8SqbPSI some random deleted video

@author: mecha#7999
"""

# https://python-forum.io/Thread-How-to-check-if-video-has-been-deleted-or-removed-in-youtube-using-python
import requests

ids = []
api_key = 'x'

for an_id in ids:
    url = f'https://www.googleapis.com/youtube/v3/videos?id={an_id}&key={api_key}&part=status'
    url_data = requests.get(url)
    json = url_data.json()
    if not len(json['items']):
        print('link dead')

