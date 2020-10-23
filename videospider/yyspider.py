import os
import ffmpy3
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

search_ketword = '越狱第一季'
search_url = 'http://www.jisudhw.com/index.php'
search_params = {
    'm':'vod-search'
}
#填写Headers信息防反爬虫
search_headers={
    'User-Agent':'Mozilla/5.0(Macintosh; Intel Mac  OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'Referer':'http://www.jisudhw.com/',
    'Origin':'http://www.jisudhw.com',
    'Host':'www.jisudhw.com'
}
#根据浏览器抓包结果填写data
search_datas = {
    'wd':search_ketword,
    'submit':'search'
}

video_dir = ''

r = requests.post(url=search_url,params = search_params, headers=search_headers,data=search_datas)
r.encoding = 'utf-8'
server = 'http://www.jisudhw.com'
search_html = BeautifulSoup(r.text,'lxml')
search_spans = search_html.find_all('span',class_='xing_vb4')       #找到搜索结果对应的标签和属性
for span in search_spans:
    url = server + span.a.get('href')
    name = span.a.string
    print(name)
    print(url)
    video_dir = name
    if name not in os.listdir('./'):
        os.mkdir(name)

    detail_url = url
    r = requests.get(url=detail_url)
    r.encoding = 'utf-8'
    detail_bf = BeautifulSoup(r.text,'lxml')
    num = 1
    search_res = {}
    for each_url in detail_bf.find_all('input'):
        if 'm3u8' in each_url.get('value'):        #url存放在value属性中，筛选出播放类型是ckm3u8的视频
            url = each_url.get('value')
            if url not in search_res.keys():
                search_res[url] = num
            print('第%03d集：'%num)
            print(url)
            num+=1

def downVideo(url):
    num = search_res[url]
    name = os.path.join(video_dir,'第%03d集.mp4' % num)
    ffmpy3.FFmpeg(inputs={url:None}, outputs={name:None}).run()     #通过ffmpeg自动整合ts分段视频，并保存为mp4格式的视频

#开4个线程池
pool = ThreadPool(4)
results = pool.map(downVideo, search_res.keys())
pool.close()
pool.join()







