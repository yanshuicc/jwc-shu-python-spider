#!/usr/bin/env python
#-*- coding:utf-8 -*-

#PIL图像库
import Image,ImageDraw

#网络库
import urllib2,requests
import re,json,cookielib
import html2text
from bs4 import BeautifulSoup
#辅助
import os,sys,time,random,termcolor

#图像识别
sys.path.append("")
from pytesser import *





#上海大学教务处验证码处理识别 返回识别文本
def yzm():
    #############保存验证码
    url="http://cj.shu.edu.cn/User/GetValidateCode"
    r=requests.get(url,params={"r":random.random()})
    if r.status_code == 200:
        print u"获取验证码成功"
        postfix = r.headers['content-type'].split("/")[1]
        image_name = u"verify."+ postfix
        open(image_name, "wb").write(r.content)
        im = Image.open(image_name)
        im.show()
    else:
        print u"获取验证码失败"
        exit()

######################图像识别
#    im = Image.open(image_name)
#    #转换灰度
#    imgry = im.convert('L')
#    #去噪
#    threshold = 140
#    table = []
#    for i in range(256):
#        if i < threshold :
#            table.append(0)
#        else:
#            table.append(1)
#    out = imgry.point(table,'1')
#    #out.save('imgry1.jepg')
#    #print out.size
#
#    #去单独的像素点
#    for y in range(out.size[1]):
#        for x in range(out.size[0]):
#            #print out.getpixel((x,y)),
#            if x>0 and x<out.size[0]-1 and y>0 and y<out.size[1]-1:
#                if out.getpixel((x-1,y))==1 and out.getpixel((x+1,y)) == 1 \
#               and out.getpixel((x,y-1)) == 1 and out.getpixel((x,y+1)) == 1 :
#                    out.putpixel((x,y),1)
#        #print ""
#    out.save('imgry.jpeg')
#    #识别
#    text = image_to_string(out)
#    #print text
#    return text


######################################main####################
##############测试连接教务处网站
requests = requests.Session()
requests.cokkies = cookielib.LWPCookieJar('cookies')
url="http://cj.shu.edu.cn"
r=requests.get(url)
if r.status_code == 200:
    print u"连接教务处成功"
else:
    print u"连接失败"
    exit()

form = {'url':'','txtUserNo':'','txtPassword':'','txtValidateCode':'','btnCheckLogin':'true'}
headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
    }
form['txtValidateCode']=yzm()
#print data['txtValidateCode'],
form['txtValidateCode']=raw_input("输入验证码:")
r=requests.post('http://cj.shu.edu.cn/',data=form,headers=headers)
print r.status_code
if r.status_code != 200:
    print u"上传表单失败"
    exit()
soup = BeautifulSoup(r.content) 
#print r.content
error = soup.find(id="divLoginAlert")


if error != None:
    print u"登陆失败"
    print error
else:
    print u"登陆成功"
    #requests.cookies.save()



