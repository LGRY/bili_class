#coding:utf-8
#python  V3.7
import requests
import sqlite3
import json
import random

#建立一个函数find()
def find():
    #确认访问地址
    url2 = 'http://www.1905.com/api/content/index.php'
    #加一个请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    #确定请求参数
    parmas = {
        'callback': 'reloadList',
        'm': 'converged',
        'a': 'info',
        'type': 'jryp',
        'year': '2018',
        'month': '08',
    }
    #请求地址
    response = requests.get(url2,headers=header,params=parmas)
    #由于返回的是有元组 所以要去一些内容
    result = response.text
    #json字符串转字典格式  //json.dumps 字典格式转json字符串
    result = result.replace( 'reloadList(' , '').replace(')','')
    # 从json格式读取
    result = json.loads(result)
    # print(result)
    for i in result['info']   :
        print (i['url'],i['title'],i['thumb'])
        #读取图片 #使用content返回一个二进制数据
        img = requests.get(i['thumb']).content
        #保存图片 保存用wb write bytes 二进制
        img_name = random.randint(10000,99999)
        with open('img/%s.jpg'%img_name,'wb') as w:
            w.write(img)

#----------------番外篇-------------------#
        #调用save data方法保存数据
        save_data(content=i['title'],img=img_name,link=i['url'])

#创建数据库
def createDB():
    conn = sqlite3.connect('film.db')
    c = conn.cursor() #他就是一个民工干活的
    c.execute('CREATE TABLE filmdata (id INTEGER PRIMARY KEY AUTOINCREMENT, content text,link text,img text)')
    conn.commit()
    conn.close()

#保存爬取的数据
def save_data(content,link,img):
    conn = sqlite3.connect('film.db')
    c = conn.cursor()
    c.execute("INSERT into filmdata(content,link,img) VALUES ('{0}','{1}','{2}')".format(content,link,img))
    conn.commit()
    conn.close()

#查看数据库内容
def showdata():
    conn = sqlite3.connect('film.db')
    c = conn.cursor()
    res = c.execute('SELECT * from filmdata')
    print (res)
    for i in res:
        print (i[1])
    conn.close()

if __name__ =='__main__':
    showdata()
    # # createDB()
    # find()
