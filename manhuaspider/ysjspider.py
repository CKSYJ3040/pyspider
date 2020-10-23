import requests
import os
import re
from bs4 import BeautifulSoup
from contextlib import closing
from tqdm import tqdm
import time

'''
思路：
    拿到所有章节名和章节链接
    根据章节链接章节里的所有漫画图片
    根据章节名，分类保存漫画
'''

# 创建保存目录
save_dir = '妖神记'
if save_dir not in os.listdir('./'):    #os.listdir()方法用于返回指定的文件夹包含的文件或文件夹的名字的列表
    os.mkdir(save_dir)

target_url = 'https://www.dmzj.com/info/yaoshenji.html'

#获取动漫章节链接和章节名
r = requests.get(url=target_url)        #通过request请求地址，获取响应对象
bs = BeautifulSoup(r.text,'lxml')
list_con_li = bs.find('ul',class_='list_con_li')    #匹配距离章节名和章节链接最近的ul
cartoon_list = list_con_li.find_all('a')        #匹配所有出现a标签的地方提取出章节名和章节链接
chapter_names = []
chapter_urls = []
for cartoon in cartoon_list:        #将章节名和章节链接存入列表
    href = cartoon.get('href')
    name = cartoon.text
    chapter_names.insert(0, name)
    chapter_urls.insert(0,href)

#下载漫画
for i,url in enumerate(tqdm(chapter_urls)):
    #header保存对应url的Referer来路
    download_header = {
        'Referer':url
    }
    name = chapter_names[i]
    # 去掉.
    while '.' in name:
        name = name.replace('.','')
    chapter_save_dir = os.path.join(save_dir, name)     #连接连个参数路径名
    if name not in os.listdir(save_dir):
        os.mkdir(chapter_save_dir)
        r = requests.get(url=url)
        html = BeautifulSoup(r.text,'lxml')
        script_info = html.script
        pics = re.findall('\d{13,14}',str(script_info))     #返回第二个参数中所有与第一个正则表达式相匹配的全部字串，返回形式为数组
        for j,pic in enumerate(pics):
            if len(pic) == 13:                      #“赌”13位的都是通过补0来正确排序
                pics[j] = pic + '0'
        pics = sorted(pics,key=lambda x:int(x))     #通过lambda表达式来将真正的pics排序，int(x)表示从小到大排序
        chapterpic_hou = re.findall('\|(\d{5})\|',str(script_info))[0]
        chapterpic_qian = re.findall('\|(\d{4})\|',str(script_info))[0]
        for idx, pic in enumerate(pics):
            if pic[-1] == '0':
                url = 'https://images.dmzj.com/img/chapterpic/'+chapterpic_qian+'/'+chapterpic_hou+'/'+pic[:-1]+'.jpg'
            else:
                url = 'https://images.dmzj.com/img/chapterpic/'+chapterpic_qian+'/'+chapterpic_hou+'/'+pic+'.jpg'
            pic_name = '%03d.jpg' % (idx + 1)
            pic_save_path = os.path.join(chapter_save_dir,pic_name)
            with closing(requests.get(url,headers = download_header,stream = True)) as response:
                chunk_size = 1024
                content_size = int(response.headers['content-length'])
                if response.status_code == 200:
                    with open(pic_save_path,'wb') as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                else:
                    print('链接异常')
            time.sleep(10)





