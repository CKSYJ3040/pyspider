import requests
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

def get_content(target):
    '''
    获取章节内容
    :param target: target下载链接
    :return: texts章节内容
    '''
    req = requests.get(url = target)
    req.encoding = 'utf-8'
    html = req.text
    bf = BeautifulSoup(html,'lxml')
    texts = bf.find('div',id='content')     #找到章节内容对应的div
    content = texts.text.strip().split('\xa0'*4)        #通过.text方法提取文字，使用strip()方法去除回车，最后使用split方法切分数据
    return content

if __name__ == '__main__':
    server = 'https://www.xsbiquge.com'
    book_name = '诡秘之主.txt'
    target = 'https://www.xsbiquge.com/15_15338'
    req = requests.get(url=target)
    req.encoding = 'utf-8'
    html = req.text
    chapter_bs = BeautifulSoup(html,'lxml')
    chapters = chapter_bs.find('div',id='list')     #找到章节名对应的div
    chapters = chapters.find_all('a')
    for chapter in tqdm(chapters):      #使用tqdm显示下载进度
        chapter_name = chapter.string
        url = server + chapter.get('href')      #get方法提取href属性，进而拼接出每一章节的url
        content = get_content(url)
        with open(book_name,'a',encoding='utf-8') as f:     #将爬取文章内容写入文件
            f.write(chapter_name)
            f.write('\n')
            f.write('\n'.join(content))
            f.write('\n')



























