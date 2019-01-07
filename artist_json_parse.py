import json
import requests
import urllib3
import os
import time
import ssl
import threadpool
from artist_html_parse import ArtistZJHtmlParse , ArtistHtmlParse

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

music_host = "https://music.163.com"
music_parent_path = "music/artist/"
base_zj_host = 'https://music.163.com/artist/album?limit=1000&offset=0&id='
zj_host = "https://music.163.com/album?id="


pool = threadpool.ThreadPool(20)

headers = {'Accept': 'text/html', 'Host': 'music.163.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


class ArtistJsonParse:

    def load_data(self):
        with open("artist.json","rb") as f:
            load_dict = json.load(f)
        return load_dict


def load_html(url):
    r = requests.get(url, headers=headers)
    return r.text


def load_music_mp3(music_id, name,save_path):

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Host': 'music.163.com',
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Upgrade-Insecure-Requests": "1",
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    url = "https://music.163.com/song/media/outer/url?id="+music_id+".mp3"
    print(url)
    path = save_path + name + ".mp3"
    if os.path.exists(path):
        print(name+".mp3 已存在")
        return
    count = 0
    while count < 3:
        try:
            r = requests.get(url, headers=headers, timeout=30)
            url = r.url
            print(url)
            if url.startswith("https://music.163.com/404"):
                return
            break
        except Exception as e:
            print("获取下载地址失败，3秒后重试")
            time.sleep(3)
        count += 1

    a ="<a href='"+url+"' download='"+name+"'>"+name+"</a><br/>\r\n"

    with open(save_path + "downMusic.html", "ab+") as f:
        f.write(a.encode())
    down_file(url, name,path)


def down_file(url, name, path):
    if os.path.exists(path):
        return

    print("开始下载："+name+".mp3")
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Upgrade-Insecure-Requests": "1",
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    count = 0
    while count < 3:
        try:

            r = requests.get(url, headers=headers, stream=True, timeout=60)
            # print(r.status_code)
            if(r.status_code == 200):
                with open(path, "wb+") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                print("完成下载：" + name + ".mp3")
                break
        except Exception as e:
            print(e)
            print("下载出错：" + name + ".mp3，3秒后重试")
            if os.path.exists(path):
                os.remove(path)

            time.sleep(3)
        count += 1

    pass


def load_zj(url,save_path):
    html_parse = ArtistZJHtmlParse()
    html = ''
    html = load_html(url)
    html_parse.feed(html)
    # print(html_parse.musics_zj_id)
    # print(html_parse.musics_zj_name)
    for i in range(0, len(html_parse.musics_zj_id)):
        load_zj_music_uri(zj_host + html_parse.musics_zj_id[i], save_path+html_parse.musics_zj_name[i]+"/")


#创建存储目录
def make_save_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


#抓取歌曲下载路劲
def load_zj_music_uri(url,save_path):
    make_save_path(save_path)

    html_parse = ArtistHtmlParse()
    html = ''
    html = load_html(url)
    html_parse.feed(html)
    # print(html_parse.musics_id)
    # print(html_parse.musics_name)
    params = []
    for i in range(0, len(html_parse.musics_id)):
        name = html_parse.musics_name[i]
        name = name.replace("|", " ")
        name = name.replace("/", " ")
        name = name.replace("\\", " ")
        name = name.replace(":", " ")
        name = name.replace("*", " ")
        name = name.replace("?", " ")
        name = name.replace('"', " ")
        name = name.replace('<', " ")
        name = name.replace('>', " ")
        id_name_path = {'music_id': html_parse.musics_id[i], 'name': name, "save_path": save_path}
        params.append((None, id_name_path))

    thread_pool_requests = threadpool.makeRequests(load_music_mp3, params)
    [pool.putRequest(req) for req in thread_pool_requests]
    pool.wait()

    return


if __name__ == "__main__":
    json_parse = ArtistJsonParse()
    load_dict = json_parse.load_data()

    urls = []
    for i in range(0,len(load_dict)):
        for j in range(0, len(load_dict[i]['artists'])):
            # print(load_dict[i]['artists'][j]["id"])
            # print(load_dict[i]['artists'][j]["name"])
            # urls.append(base_host+str(load_dict[i]['artists'][j]["id"]))
            load_zj(base_zj_host+str(load_dict[i]['artists'][j]["id"]), music_parent_path + load_dict[i]['artists'][j]["name"]+"/")



