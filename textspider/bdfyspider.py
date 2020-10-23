import requests

if __name__ == '__main__':
    target = "http://fanyi.baidu.com/"
    req = requests.get(url=target)  #通过requests请求地址
    req.encoding = 'utf-8'      #获取页面信息
    print(req.text)
