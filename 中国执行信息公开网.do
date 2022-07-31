*一、图片预处理
*下载验证码原图
clear
cd "C:\Users\XueYuan\Desktop\验证码"
forvalues i = 1/100 {
	copy "http://zxgk.court.gov.cn/zhzxgk/captcha.do?captchaId=742526ef8a104ba89980bac3e02286e6" `i'.png, replace
}
*灰度处理


*1.PNG转tiff
*2.使用jTessBoxEditor对多个tiff进行merge，命名为eng.fontzxgk.exp0.tif
*3.创建对应的box文件
tesseract eng.fontzxgk.exp0.tif eng.fontzxgk.exp0 -l eng -psm 7 batch.nochop makebox
*4.进入box修正
*5.对修正后的box进行训练
tesseract eng.fontzxgk.exp0.tif eng.fontzxgk.exp0 -l eng -psm 7 nobatch box.train
*6.运行.\cmd.bat进行批处理
*7.测试效果
tesseract grey15.tif output_1 -l eng -psm 7
tesseract grey15.tif output_2 -l fontzxgk -psm 7

*采坑总结
**3.02.02版本在本机上无法使用
**3.05.02版本使用命令行逐行输入也无法成功，但直接使用批处理却能够成功生成traineddata文件
**训练后识别效果特别差，现考虑在训练前对图片进行预处理
****（1）调整图片尺寸，至少300dpi
****（2）二值化
****（3）降噪处理
****（4）对年代久远的文本，可以做Dilation and Erosion
****（5）Rotation / Deskewing
****（6）处理扫描边框Borders
****（7）PNG有alpha（透明度选项），使用tesseract之前应该删除alpha channel,tesseract 4有专门的的函数可以处理
****（8）分隔页面
****（9）使用/禁用Dictionaries, word lists, and patterns
**处理过程
***更新tesseract至5.0alpha版本
***预处理图片：二值化；更改至最佳分辨率
***
