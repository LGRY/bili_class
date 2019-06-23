#coding:utf-8

import requests
import re
from time import sleep
#确认访问地址
url = 'http://www.1905.com/mtalk/?fr=homepc_menu_cmt'
#确认查找规则-正则表达式
pattern = '<figcaption class="list-title"><a href="(.*?)" target="_blank">(.*?)</a></figcaption>'
#加一个请求头
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
#请求地址
response = requests.get(url,headers=header)
#注意编码按照页面编码制定
response.encoding = 'utf8'

#打印输出
print (response.text)

#匹配我要的东西
result = re.findall(string=response.text,pattern=pattern,flags=re.S)

#保存文件到txt
for i in result:
    print (i[1],i[0])
    with open('film.txt','a') as w:
        w.write(i[1]+i[0]+'\n')



