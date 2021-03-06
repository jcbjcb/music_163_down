import requests
import urllib3
import os
import time
import ssl
import threadpool
from music_html_parse import MusicHtmlParse
from music_column_html_parse import MusicColumnHtmlParse
from page_html_parse import PageHtmlParse

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

music_host = "https://music.163.com"
music_parent_path = "music/"
artist_path = "music/artist"

pool = threadpool.ThreadPool(20)

headers = {'Accept': 'text/html', 'Host': 'music.163.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


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


def down_file(url,name,path):
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


#加载歌单列表url 并创建本地目录
def load_all_column(url):
    music_column_html_parse = MusicColumnHtmlParse()
    html = ''
    html = load_html(url)
    music_column_html_parse.feed(html)
    print(music_column_html_parse.musics_path_url)
    print(music_column_html_parse.musics_path_name)
    for i in range(0, len(music_column_html_parse.musics_path_url)):
        file_name = music_column_html_parse.musics_path_name[i]
        file_name = file_name.replace("|", " ")
        file_name = file_name.replace("/", " ")
        file_name = file_name.replace("\\", " ")
        file_name = file_name.replace(":", " ")
        file_name = file_name.replace("*", " ")
        file_name = file_name.replace("?", " ")
        file_name = file_name.replace('"', " ")
        file_name = file_name.replace('<', " ")
        file_name = file_name.replace('>', " ")
        music_save_path = music_parent_path+file_name+"/"
        make_save_path(music_save_path)
        uri = music_host + music_column_html_parse.musics_path_url[i]
        print(uri)
        print(music_save_path)
        load_music_uri(uri,music_save_path)


#创建存储目录
def make_save_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

#抓取歌曲下载路劲
def load_music_uri(url,save_path):
    html_parse = MusicHtmlParse()
    html = ''
    html = load_html(url)
    html_parse.feed(html)
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

#获取分页页码
def load_page(url):
    page_html_parse = PageHtmlParse()
    html = ''
    html = load_html(url)
    page_html_parse.feed(html)
    result = {
        "params": page_html_parse.params,
        "pages": page_html_parse.pages,
    }
    page_html_parse.close()
    return result


if __name__ == "__main__":

    print("程序开始执行")

    urls = ["https://music.163.com/discover/playlist", "https://music.163.com/discover/toplist"]

    all_urls = []
    print(urls)
    for uri in urls:
        result =load_page(uri)
        if result["pages"] == 0:
            all_urls.append(uri)
        else:
            for i in range(0,result["pages"]):
                url_params = result["params"][0:result["params"].index("offset=")+7]
                all_urls.append(uri+"?"+url_params+str((i*35)))

    print(all_urls)
    for real_uri in all_urls:
        load_all_column(uri)

    # html_parse = MusicHtmlParse()
    # html = load_html('https://music.163.com/discover/toplist?id=3778678')
    # html_parse.feed(html)
    # html_header = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>musics auto down</title></head><body>'
    # with open("top_hot/downMusic.html", "ab+") as f:
    #     f.write(html_header.encode())
    # params = []
    # for i in range(0, len(html_parse.musics_id)):
    #     id_name = {'music_id': html_parse.musics_id[i], 'name': html_parse.musics_name[i]}
    #     params.append((None, id_name))
    #     #单线程下载
    #     # load_music_mp3(html_parse.musics_id[i],html_parse.musics_name[i])
    #     # time.sleep(3)
    #
    # print(params)
    # #多线程下载
    # pool = threadpool.ThreadPool(10)
    # thread_pool_requests = threadpool.makeRequests(load_music_mp3, params)
    # [pool.putRequest(req) for req in thread_pool_requests]
    # pool.wait()

    # scripts="<script>( function(){var a = document.getElementsByTagName('a');for (var i =0;i<a.length ;i++ ){console.log(i);a[i].click();}})()</script>"
    # with open("163/downMusic.html", "ab+") as f:
    #     f.write(scripts.encode())

    # html_footer = '</body></html>'
    # with open("top_hot/downMusic.html", "ab+") as f:
    #     f.write(html_footer.encode())
    # html_parse.close()

    print("程序执行完成")
