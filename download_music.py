# -*- coding:utf8 -*-
import settings
import requests
import time
base_url = "http://www.kuwo.cn/url?format=mp3&rid={rid}&response=url&type=convert_url3&br=128kmp393"

def fetch_html(url, retry=10, timeout=300):
    while retry > 0:
        rsp = requests.get(url, timeout=timeout)
        if rsp.status_code == 200:
            return rsp
        retry -= 1
        time.sleep(1)
    return ""

def download(url, filename):
    rsp = fetch_html(url)
    with open(filename, "wb") as fs:
        fs.write(rsp.content)

def download1(rid):
    url = base_url.format(rid=rid)
    html = fetch_html(url)

if __name__ == "__main__":
    download("https://win-web-ra01-sycdn.kuwo.cn/ff54a2da3684ebb86ba31ad36fc4316c/5d838b38/resource/n3/128/3/11/3233852694.mp3", "./music/1.mp3")