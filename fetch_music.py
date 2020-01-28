# -*- coding:utf8 -*-
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'app_data.settings'
django.setup()

from app_data.models.entity import Music, Singer, Link

import settings
import requests
import time
import json

base_url = "http://www.kuwo.cn/api/www/artist/artistMusic?artistid={singer_id}&pn={page}&rn={page_size}"

cookie = "__root_domain_v=.kuwo.cn; _qddaz=QD.jep4o0.nsle0h.k0mhkgdo; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1577888492; _ga=GA1.2.156973536.1577888492; _gid=GA1.2.1543256353.1577888492; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1577890191; _gat=1; kw_token=83FFQT2QSLF"
csrf = "83FFQT2QSLF"
def batch_save(audios):
    try:
        Music.objects.bulk_create(audios)
    except Exception as e:
        print "[save] error:%s" % str(e)
        for audio in audios:
            try:
                Music.objects.update_or_create(
                    rid = audio.rid,
                    sid = audio.sid,
                    defaults = dict(
                        artist = audio.artist,
                        album_name = audio.album_name,
                        album_id = audio.album_id,
                        music_name = audio.music_name,
                        duration = audio.duration,
                        pub_date = audio.pub_date
                    )
                )
            except Exception as e:
                print "[batch_save] error:%s" % str(e)

def batch_save_link(links):
    try:
        Link.objects.bulk_create(links)
    except Exception as e:
        print "[batch_save_link] error:%s" % str(e)
        for link in links:
            try:
                Link.objects.update_or_create(
                    rid = link.rid,
                    default = dict(
                        sid = link.sid,
                        mp3_url = link.mp3_url
                    )
                )
            except Exception as e:
                print "[batch_save_link] error:%s" % str(e)

def fetch_html(url, headers = {}, retry=10, timeout=300):
    while retry > 0:
        try:
            rsp = requests.get(url, timeout=timeout, headers=headers)
            if rsp.status_code == 200:
                return rsp.text
            retry -= 1
            time.sleep(0.5)
        except Exception as e:
            print str(e)
            print "retrying.... remain:%s" % retry
            retry -= 1
            time.sleep(5)
    return ""

def convert_to_audios(html, sid):
    audios = []
    json_data = json.loads(html)
    audio_list = json_data.get("data", dict()).get("list", [])
    for item in audio_list:
        audio = Music()
        audio.sid = sid
        audio.rid = item.get("rid", 0)
        audio.artist = item.get("artist", 0)
        audio.album_name = item.get("album", 0)
        audio.music_name = item.get("name", 0)
        audio.album_id = item.get("albumid", 0)
        audio.duration = item.get("duration", 0)
        audio.pub_date = item.get("releaseDate", "")
        audios.append(audio)
    return audios

def get_sid_list():
    singers = Singer.objects.all()
    return [singer.singer_id for singer in singers]

def process_singer(sid):
    page = 1
    page_size = 15000
    url = base_url.format(singer_id=sid, page=page, page_size=page_size)
    html = fetch_html(url=url, headers={"cookie":cookie, "csrf":csrf})
    audios = convert_to_audios(html, sid)
    print "[process_singer] sid:%s fetch count:%s" % (sid, len(audios))
    batch_save(audios)

def process_music_url():
    music_url = "http://www.kuwo.cn/url?format=mp3&rid={rid}&response=url&type=convert_url3&br=128kmp393"
    start = 0
    batch_size = 1000
    total = Music.objects.count()
    count = 0
    audios = Music.objects.all()
    print "[process_music_url] start total:%s" % total
    while True:
        links = []
        batch_audios = audios[start: start+batch_size]
        if not batch_audios:
            break
        for audio in batch_audios:
            count += 1
            if count % 10 == 0:
                print "[process_music_url] process %s | %s" % (count, total)
            if not audio.rid:
                continue
            url = music_url.format(rid = audio.rid)
            html = fetch_html(url, retry=3)
            if not html:
                continue
            try:
                mp3_url = json.loads(html).get("url", "")
            except Exception as e:
                continue
            link = Link()
            link.rid = audio.rid
            link.sid = audio.sid
            link.mp3_url = mp3_url
            links.append(link)
        batch_save_link(links)
        start += batch_size

def process():
    sids = get_sid_list()[80:]
    count = 0
    for sid in sids:
        if count % 5 == 0:
            print "[process] %s | %s" % (count, len(sids))

        count += 1
        process_singer(sid)

if __name__ == "__main__":
    process()