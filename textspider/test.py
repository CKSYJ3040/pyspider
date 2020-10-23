# import requests
# from bs4 import BeautifulSoup
#
# target_rurl = 'https://www.dmzj.com/info/yaoshenji.html'
# r = requests.get(url=target_rurl)
# bs = BeautifulSoup(r.text,'lxml')
# list_con_li = bs.find('ul',class_='list_con_li')
# comic_list = list_con_li.find_all('a')
# chapter_names=[]
# chapter_urls=[]
# for comic in comic_list:
#     href = comic.get('href')
#     name = comic.text
#     chapter_names.insert(0,name)
#     chapter_urls.insert(0,href)
#
# print(chapter_names)
# print(chapter_urls)


# import requests
# from bs4 import BeautifulSoup
# import re
#
# url = 'https://www.dmzj.com/view/yaoshenji/41917.html'
# r = requests.get(url=url)
# html = BeautifulSoup(r.text, 'lxml')
# script_info = html.script
# pics = re.findall('\d{13,14}', str(script_info))
# chapterpic_hou = re.findall('\|(\d{5})\|', str(script_info))[0]
# chapterpic_qian = re.findall('\|(\d{4})\|', str(script_info))[0]
# for pic in pics:
#     url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic + '.jpg'
#     print(url)

# import requests
# from bs4 import BeautifulSoup
# import re
#
# url = 'https://www.dmzj.com/view/yaoshenji/41917.html'
# r = requests.get(url=url)
# html = BeautifulSoup(r.text, 'lxml')
# script_info = html.script
# pics = re.findall('\d{13,14}', str(script_info))        #返回第二个参数中所有与第一个正则表达式相匹配的全部字串，返回形式为数组
# for idx, pic in enumerate(pics):
#     if len(pic) == 13:
#         pics[idx] = pic + '0'                           #“赌”13位的都是末尾补零的结果
# pics = sorted(pics, key=lambda x:int(x))
# chapterpic_hou = re.findall('\|(\d{5})\|', str(script_info))[0]
# chapterpic_qian = re.findall('\|(\d{4})\|', str(script_info))[0]
# for pic in pics:
#     if pic[-1] == '0':
#         url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic[:-1] + '.jpg'
#     else:
#         url = 'https://images.dmzj.com/img/chapterpic/' + chapterpic_qian + '/' + chapterpic_hou + '/' + pic + '.jpg'
#     print(url)


# import requests
# from contextlib import closing
# #直接爬取返回错误代码403，表示资源不可用
# #Referer可以理解为来路，先打开章节URL链接，在打开图片链接，这样就能通过反扒虫手段
# # header保存了Referer来路
# download_header = {
#     'Referer':'https://www.dmzj.com/view/yaoshenji/41917.html'
# }
#
# dn_url = 'https://images.dmzj.com/img/chapterpic/3059/14237/14395217739069.jpg'
# with closing(requests.get(dn_url,headers=download_header,stream=True)) as response:
#     chunk_size = 1024
#     content_size = int(response.headers['content-length'])
#     if response.status_code == 200:
#         print('文件大小：%0.2f KB'%(content_size / chunk_size))
#         with open('1.jpg','wb') as file:
#             for data in response.iter_content(chunk_size=chunk_size):
#                 file.write(data)
#     else:
#         print('链接异常')
# print('下载完成！')




import requests
from bs4 import BeautifulSoup
#
# search_ketword = '越狱第一季'
# search_url = 'http://www.jisudhw.com/index.php'
# search_params = {
#     'm':'vod-search'
# }
# #填写Headers信息防反爬虫
# search_headers={
#     'User-Agent':'Mozilla/5.0(Macintosh; Intel Mac  OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
#     'Referer':'http://www.jisudhw.com/',
#     'Origin':'http://www.jisudhw.com',
#     'Host':'www.jisudhw.com'
# }
# #根据浏览器抓包结果填写data
# search_datas = {
#     'wd':search_ketword,
#     'submit':'search'
# }
# #网站解析后发现搜索是一个post请求
# r = requests.post(url=search_url,params = search_params, headers=search_headers,data=search_datas)
# r.encoding = 'utf-8'
# server = 'http://www.jisudhw.com'
# search_html = BeautifulSoup(r.text,'lxml')
# search_spans = search_html.find_all('span',class_='xing_vb4')       #找到搜索结果对应的标签和属性
# for span in search_spans:
#     yyurl = server + span.a.get('href')
#     name = span.a.string
#     print(name)
#     print(yyurl)

# detail_url = 'http://www.jisudhw.com/?m=vod-detail-id-15409.html'
# r = requests.get(url=detail_url)            #网站解析后发现是get请求
# r.encoding = 'utf-8'
# detail_bf = BeautifulSoup(r.text, 'lxml')
# num = 1
# search_res = {}
# for each_url in detail_bf.find_all('input'):
#     if 'm3u8' in each_url.get('value'):         #url存放在value属性中，筛选出播放类型是ckm3u8的视频
#         url = each_url.get('value')
#         if url not in search_res.keys():
#             search_res[url]=num                 #将结果存放于字典中，方便集数和链接一一对应
#         print('第%03d集：'% num)
#         print(url)
#         num += 1
