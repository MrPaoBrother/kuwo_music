# -*- coding:utf8 -*-
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'app_data.settings'
django.setup()

from app_data.models.entity import Singer

import settings
import requests
import time
import json
import datetime

base_url = "http://www.kuwo.cn/api/www/artist/artistInfo?category=0&prefix=&pn={page}&rn={page_size}"

def batch_save(singers):
    try:
        Singer.objects.bulk_create(singers)
    except Exception as e:
        print "[save] error:%s" % str(e)
        for singer in singers:
            Singer.objects.update_or_create(
                singer_id = singer.singer_id,
                platform = singer.platform,
                defaults = dict(
                    singer_name = singer.singer_name,
                    fans_num = singer.fans_num,
                    music_num = singer.music_num,
                    album_num = singer.album_num,
                )
            )

def fetch_html(url, retry=10, timeout=20):
    while retry > 0:
        rsp = requests.get(url, timeout=timeout)
        if rsp.status_code == 200:
            return rsp.text
        retry -= 1
        time.sleep(1)
    return ""

def get_total_singers():
    import pdb;pdb.set_trace()
    url = base_url.format(page=1, page_size=1)
    return json.loads(fetch_html(url=url)).get("data", dict()).get("total", 0)

def convert_to_singers(html):
    singers = []
    json_data = json.loads(html)
    singer_list = json_data.get("data", dict()).get("artistList", [])
    for item in singer_list:
        singer = Singer()
        singer.singer_id = item.get("id", 0)
        singer.singer_name = item.get("name", 0)
        singer.fans_num = item.get("artistFans", 0)
        singer.music_num = item.get("musicNum", 0)
        singer.album_num = item.get("albumNum", 0)
        singers.append(singer)
    return singers

def fetch():
    total_nums = int(get_total_singers())
    page = 1
    page_size = 1000
    while True:
        url = base_url.format(page=page, page_size=page_size)
        html = fetch_html(url=url)
        singers = convert_to_singers(html)
        batch_save(singers)
        if page * page_size > total_nums:
            break
        print "[fetch] current proecss %s | %s" % (page * page_size, total_nums)
        page += 1

if __name__ == "__main__":
    # fetch()
    print get_total_singers()