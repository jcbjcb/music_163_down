import requests
from html.parser import HTMLParser
import urllib3
import os
import time
import ssl
import threadpool
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

class MusicHtmlParse(HTMLParser):
    a_text = False
    def __init__(self):
        HTMLParser.__init__(self)
        self.musics_id = [

        ]

        self.musics_name = [

        ]
    def handle_starttag(self, tag, attrs):
        # pass
        if tag == "a":
            for (variable, value) in attrs:
                if variable == "href":
                    # print(value)
                    if not value.startswith('/song?id=${song.id}') and not value.startswith('/song?id=${x.id}') and value.startswith('/song?id='):
                        self.a_text = True
                        # print(str(attrs[1][1]))
                        id = value.replace("/song?id=", '')
                        self.musics_id.append(id)
                    else:
                        self.a_text = False

        # print('<%s>' % tag)

    def handle_endtag(self, tag):
        pass
        # print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass
        # print('<%s/>' % tag)

    def handle_data(self, data):
        if self.a_text:
            self.musics_name.append(data)

        # print(data)

    def handle_comment(self, data):
        pass
        # print('<!--', data, '-->')

    def handle_entityref(self, name):
        pass
        # print('&%s;' % name)

    def handle_charref(self, name):
        pass
        # print('&#%s;' % name)


headers = {'Accept': 'text/html', 'Host': 'music.163.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


def load_html(url):
    r = requests.get(url, headers=headers)
    return r.text

def load_music_mp3(music_id, name):

    print(music_id)
    print(name)

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Host': 'music.163.com',
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Upgrade-Insecure-Requests": "1",
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    url = "https://music.163.com/song/media/outer/url?id="+music_id+".mp3"

    print(url)


    # a ="<a href='"+url+"' download='"+name+"'>"+name+"</a><br/>\r\n"
    #
    # with open("163/downMusic.html", "ab+") as f:
    #     f.write(a.encode())

    path = "top_hot/" + name + ".mp3"
    if os.path.exists(path):
        print(name+".mp3 已存在")
        return
    count = 0
    while count < 3:
        try:
            time.sleep(3)
            r = requests.get(url, headers=headers, timeout=30)
            url = r.url
            print(url)
            if url.startswith("https://music.163.com/404"):
                return
            break
        except Exception as e:
            print(e)
        count += 1

    a ="<a href='"+url+"' download='"+name+"'>"+name+"</a><br/>\r\n"

    with open("top_hot/downMusic.html", "ab+") as f:
        f.write(a.encode())

    down_file(url, name)

    #
    # http = urllib3.PoolManager()
    # r = http.request('GET',
    #                  "https://m10.music.126.net/20190106164130/d396bd20bf010303ef52a3161165d85f/ymusic/065b/0052/000b/11bc8f8d57783c1b3dd37a27113006be.mp3",
    #                  headers=headers,preload_content=False)
    # print(r.data)

    return
    # r = requests.get("https://m10.music.126.net/20190106164130/d396bd20bf010303ef52a3161165d85f/ymusic/065b/0052/000b/11bc8f8d57783c1b3dd37a27113006be.mp3", headers=headers)
    # print(r.content)
    # return
    # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #            'Host': 'm10.music.126.net',
    #            "Accept-Encoding": "gzip, deflate, br",
    #            "Accept-Language": "zh-CN,zh;q=0.9",
    #            "Upgrade-Insecure-Requests": "1",
    #            "range": "bytes=0-3516382",
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    #
    # http = urllib3.PoolManager()
    # r = http.request('GET', "https://m10.music.126.net/20190106164130/d396bd20bf010303ef52a3161165d85f/ymusic/065b/0052/000b/11bc8f8d57783c1b3dd37a27113006be.mp3", headers=headers)
    # print(r.data)
    # try:
    #     r = http.request('GET', url, headers=headers)
    #     print(r.data)
    # except urllib3.exceptions.MaxRetryError as e:
    #     print(e.url)
    #     url = e.url.replace("/music.163.com", "https://m10.music.126.net")
    #     url = url[0:url.index("?wsrid_tag")]
    #     print(url)
    #     r = http.request('GET', url, headers=headers)
    #     with open("163/" + name + ".mp3", "wb") as f:
    #         f.write(r.data)


    # with open("163/" + name + ".mp3", "wb") as f:
    #     f.write(http.request('GET', url, headers=headers))
    pass
def down_file(url,name):
    path = "top_hot/"+name+".mp3"
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
            time.sleep(3)
            r = requests.get(url,headers=headers,stream=True,timeout=60)
            print(r.status_code)
            if(r.status_code == 200):
                with open(path, "wb+") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                print("完成下载：" + name + ".mp3")
                break
        except Exception as e:
            print(e)
            print("下载出错：" + name + ".mp3")
            if os.path.exists(path):
                os.remove(path)
        count += 1

    pass

if __name__ == "__main__":

    print("程序开始执行")

    html_parse = MusicHtmlParse()
    html = load_html('https://music.163.com/discover/toplist?id=3778678')
    # print(html)
    html_parse.feed(html)
    # print(len(html_parse.musics_id))
    # print(html_parse.musics_name[0:100])
    html_header = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>musics auto down</title></head><body>'
    with open("top_hot/downMusic.html", "ab+") as f:
        f.write(html_header.encode())
    params = []
    for i in range(0, len(html_parse.musics_id)):
        id_name = {'music_id': html_parse.musics_id[i], 'name': html_parse.musics_name[i]}
        params.append((None, id_name))
        #单线程下载
        # load_music_mp3(html_parse.musics_id[i],html_parse.musics_name[i])
        # time.sleep(3)

    print(params)
    #多线程下载
    pool = threadpool.ThreadPool(10)
    thread_pool_requests = threadpool.makeRequests(load_music_mp3, params)
    [pool.putRequest(req) for req in thread_pool_requests]
    pool.wait()

    # scripts="<script>( function(){var a = document.getElementsByTagName('a');for (var i =0;i<a.length ;i++ ){console.log(i);a[i].click();}})()</script>"
    # with open("163/downMusic.html", "ab+") as f:
    #     f.write(scripts.encode())

    html_footer = '</body></html>'
    with open("top_hot/downMusic.html", "ab+") as f:
        f.write(html_footer.encode())
    html_parse.close()

    print("程序执行完成")
