# -*- coding: utf-8 -*-

import requests
import os
import time
os.chdir(r'D:\tempro\executed_person')

# *一、图片预处理
# *下载验证码原图
code_path = "./secu_code"
grey_path = "./secu_code_grey"
resize_path = "./secu_code_resize"
larger_path = "./secu_code_larger"

ImgUrl = "http://zxgk.court.gov.cn/zhzxgk/captcha.do?captchaId=742526ef8a104ba89980bac3e02286e6"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
for i in range(700,1001):
    r = requests.get(ImgUrl,headers = header, timeout=2)
    img = open(code_path + "/" + "%s.png" %i,'wb')
    img.write(r.content)
    
    img.close()
    time.sleep(2)
print("已下载NO.500-NO.1000")


# *PNG转tiff: 使用格式工厂，手工批量转,转换后文件放入tif_path

# *图片二值化
from PIL import Image

for p in range(501,511):
    if os.path.exists(code_path + "/" + "%s.png" %p):
        image = Image.open(code_path + "/" + "%s.png" %p)
        # image.show()
        image = image.convert('L')
        threshold = 250
        table = []
        
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        
        image = image.point(table, "1")
        # image.show()
        image.save(r"./secu_code_grey/test{}.png".format(p))


# *放大，更改dpi
'''pip install opencv-python'''
import cv2
import os
from PIL import Image as ImagePIL, ImageFont, ImageDraw
from PIL import Image

tif_path = r"./secu_code_tif"
# larger_path = r"./secu_code_larger/"
# tif_img_name = os.listdir(tif_path)
# tif_img_path = [tif_path + imgname for imgname in tif_img_name if imgname[0:4] == "test"]
# tif_img_save = [larger_path + imgname for imgname in tif_img_name if imgname[0:4] == "test"]

for p in range(501,511):  
    if os.path.exists(r"./secu_code_tif/test{}.tif".format(p)):
        im = cv2.imread(r"./secu_code_tif/test{}.tif".format(p))   #读取图片rgb 格式<class 'numpy.ndarray'>
        im = cv2.resize(im, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        image = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))  #格式转换，bgr转rgb
        image.save(r"./secu_code_larger/test{}.tif".format(p),quality=95,dpi=(300.0,300.0))    #调整图像的分辨率为300,dpi可以更改

  
# *2.使用jTessBoxEditor对多个tiff进行merge，命名为eng.fontzxgk.exp0.tif
# *3.创建对应的box文件
# tesseract eng.fontzxgk.exp0.tif eng.fontzxgk.exp0 -l eng --psm 7 batch.nochop makebox
# *4.进入box修正
# *5.合并两个tif集，合并修正后的box，注意序号
# *6.运行.\cmd.bat进行批处理
# *7.复制traineddata文件值tesdata
# *7.测试效果
# tesseract grey15.tif output -l eng --psm 7
# tesseract grey2.tif output -l fontzxgk --psm 7 --dpi 96
# tesseract grey2.tif output -l fontzxgk --psm 7 --dpi 300
# .\output.txt
# *采坑总结
# **3.02.02版本在本机上无法使用
# **3.05.02版本使用命令行逐行输入也无法成功，但直接使用批处理却能够成功生成traineddata文件
# **训练后识别效果特别差，现考虑在训练前对图片进行预处理
# ****（1）调整图片尺寸，至少300dpi
# ****（2）二值化
# ****（3）降噪处理
# ****（4）对年代久远的文本，可以做Dilation and Erosion
# ****（5）Rotation / Deskewing
# ****（6）处理扫描边框Borders
# ****（7）PNG有alpha（透明度选项），使用tesseract之前应该删除alpha channel,tesseract 4有专门的的函数可以处理
# ****（8）分隔页面
# ****（9）使用/禁用Dictionaries, word lists, and patterns
# **处理过程
# ***更新tesseract至5.0alpha版本
# ***预处理图片：二值化；更改至最佳分辨率；放大图片
# ***选择OCR引擎模式
# *1 = Neural nets LSTM only
# tesseract grey3.tif u -l eng --dpi 300 --psm 7 --oem 1 
# *3 = Default, based on what is available.
# tesseract grey3.tif u -l eng --dpi 300 --psm 7 --oem 3 


# 图片与处理
# 训练

