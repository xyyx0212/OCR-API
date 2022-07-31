# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 23:45:04 2021

@author: XueYuan
"""
import requests
from lxml import etree
import time
import os
import pytesseract
from PIL import Image
import re
import pandas as pd

def Getid(file):
    '''从excel获得“姓名”和“身份证号”'''
    df = pd.read_excel(file)
    name_list = df['姓名'].values.tolist()
    id_list = df['身份证号'].values.tolist()
    return name_list, id_list

def GetSession():
    session = requests.session()
    return session

def GetHTML(session):
    url = "http://zxgk.court.gov.cn/zhzxgk/"
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"zxgk.court.gov.cn",
        "Referer":"http://zxgk.court.gov.cn/",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }
    sourcecode = True
    while sourcecode:
        try:
            html = session.get(url, headers = headers)
            if html.status_code == 200:
                sourcecode = False
            else:
                time.sleep(5)
        except:
            time.sleep(5)
    return html.text, session

def GetCaptcha(html):
    tree = etree.HTML(html)
    img_xpath = "//img[@id='captchaImg']/@src"
    captchaid_xpath = "//input[@id='captchaId']/@value"   
    img_url = 'http://zxgk.court.gov.cn/zhzxgk/' + tree.xpath(img_xpath)[0]
    '''img_url似乎没用，即使地址一样，每次请求获得图片都不一样'''
    '''img_url有用，每次请求后服务器会记录该次请求的图片，input后点击查询，能够对用户输入的验证码进行判别'''
    '''http://zxgk.court.gov.cn/zhzxgk/captcha.do?captchaId=2a2f859ac91244e3ad88e99f4b925e66''''
    captchaid = tree.xpath(captchaid_xpath)[0]
    return img_url, captchaid

def DownloadImg(session, img_url):
    url_headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"zxgk.court.gov.cn",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"
        }
    img = True
    while img:
        try:
            img_html = session.get(img_url, headers = url_headers)
            if img_html.status_code == 200:
                img = False
            else:
                time.sleep(5)
        except:
            time.sleep(5)
    open('yzm.png', 'wb').write(img_html.content)
    return session

def Imgocr(img):
    png = Image.open(img)
    code = pytesseract.image_to_string(png, lang='langzxgk')
    code = re.sub('\s', '', code)
    return code
    
def Checkyzm(session, captchaid, code):
    check_url = "http://zxgk.court.gov.cn/zhzxgk/checkyzm?captchaId=%s&pCode=%s" % (captchaid, code)
    check_headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Host":"zxgk.court.gov.cn",
        "Referer":"http://zxgk.court.gov.cn/zhzxgk/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
        }
    check = True
    while check:
        try:
            check_html = session.get(check_url, headers = check_headers)
            if check_html.status_code == 200:
                check = False
            else:
                time.sleep(5)
        except:
            time.sleep(5)
    result = int(check_html.text)
    return session, result

def GetItem(session, captchaid, code, id):
    item_url = "http://zxgk.court.gov.cn/zhzxgk/searchZhcx.do"
    item_headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Host":"zxgk.court.gov.cn",
        "Origin":"http://zxgk.court.gov.cn",
        "Referer":"http://zxgk.court.gov.cn/zhzxgk/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "X-Requested-With":"XMLHttpRequest"
        }
    data = {
        "pName":"",
        "pCardNum":id,
        "selectCourtId":"0",
        "pCode":code,
        "captchaId":captchaid,
        "searchCourtName":"全国法院（包含地方各级法院）",
        "selectCourtArrange":"1",
        "currentPage":"1"
        }
    json = True
    while json:
        try:
            json_html = session.post(item_url, headers = item_headers, data = data)
            if json_html.status_code == 200:
                json = False
            else:
                time.sleep(5)
        except:
            time.sleep(5)
    true = True
    false = False
    jsondict = eval(json_html.text)
    size = jsondict[0]["totalSize"]
    return session, size

def OutputData(select_name, select_id):
    df = pd.DataFrame(data = [select_name, select_id]).T
    df.columns = ["姓名", "身份证号"]
    df.to_excel("被执行人.xlsx", index = None)

if __name__ == '__main__':
    os.chdir(r'E:\爬虫\中国执行信息公开网')
    name_list, id_list = Getid("名单.xlsx")
    select_name = []
    select_id = []
    session = GetSession()
    for name, id in zip(name_list, id_list):
        html, session = GetHTML(session)
        img_url, captchaid = GetCaptcha(html)
        result = 0
        while not result:
            session = DownloadImg(session, img_url)
            code = Imgocr('yzm.png')
            session, result = Checkyzm(session, captchaid, code)
        session, size = GetItem(session, captchaid, code, id)
        if size != 0:
            select_name.append(name)
            select_id.append(id)
    OutputData(select_name, select_id)
