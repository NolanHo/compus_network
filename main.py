import json
from threading import Thread

import requests
import time
import random

header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '955',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #   'Cookie': '',  #一定不要带Cookie，不然短时间重复访问会导致需要验证码
    'Host': '192.168.50.3:8080',
    'Origin': 'http://192.168.50.3:8080',
    'Referer': 'http://192.168.50.3:8080/eportal/index.jsp?wlanuserip=a8bd09ff950541c391e07a3af785fbdc&wlanacname=31e4a47743279bf6ea846721f186502e&ssid=&nasip=bf154bd7033a365bc1f2795dda2e9033&snmpagentip=&mac=14288ac2df86e3447e9caa37f0b684d5&t=wireless-v2&url=709db9dc9ce334aa02a9e1ee58ba6fcf3bc3349e947ead368bdd021b808fdbac30c65edaa96b0727&apmac=&nasid=31e4a47743279bf6ea846721f186502e&vid=976848caab089870&port=2bbe08ebbd4c7aff&nasportid=5b9da5b08a53a540415dbe3ede93ee4dcd170cbaa0ab1367c411c7538a416394',
    # 从请求头中获取
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    # 一般无需修改
}

dataLogin = {
    'userId': '',  # 填写post请求中的账号
    'password': '',
    # 填写post请求中加密过的密码
    'service': '',  # 选择网络接入方式，在post请求中有
    'queryString': '',
    # 从post请求中复制过来即可
    'operatorPwd': '',  # 不用填
    'operatorUserId': '',  # 不用填
    'validcode': '',  # 不用填
    'passwordEncrypt': 'true',  # 不用修改
    'userIndex': ''
    # 填写post请求中的对应字段
}

dataCheck = {
    'userIndex': ''
    # 填写post请求中的对应字段，同上
}

login = 'http://192.168.50.3:8080/eportal/InterFace.do?method=login'  # 登录地址
checkStatus = 'http://192.168.50.3:8080/eportal/InterFace.do?method=getOnlineUserInfo'  # 验证地址

target_url = ""
data = {
    "status": "logout",
    "timestamp": "",
    "ipv4": "",
    "ipv6": "",
}


def work():
    res1 = requests.post(url=checkStatus, headers=header, data=dataCheck)
    res1.encoding = 'utf-8'
    content = str(res1.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode())
    i = content.find('"result":"')
    print(content)
    if content[i + 10:i + 14] == 'wait':
        print(time.asctime(time.localtime(time.time())), "当前处于在线状态。")
        data["status"] = "login"
    else:
        print(time.asctime(time.localtime(time.time())), "当前已经下线，正在尝试登录！")
        data["status"] = "logout"
        res2 = requests.post(url=login, headers=header, data=dataLogin)
        res2.encoding = 'utf-8'
        content2 = str(res2.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode())
        j = content2.find('"result":"')
        #        print(content2)
        if content2[j + 10:j + 17] == 'success':
            print(time.asctime(time.localtime(time.time())), "登录成功！")
            data["status"] = "login"


import core


def post_heartbeat():
    while True:
        ip_info = core.get_ip_address()
        data["ipv4"] = ip_info["ipv4"]
        data["ipv6"] = ip_info["ipv6"]
        # 时间格式: 2020-12-31 23:59:59
        data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(data)
        try:
            res = requests.post(target_url, data=json.dumps(data))
            if res.status_code == 200:
                print("心跳发送成功, time: ", time.asctime(time.localtime(time.time())))
            time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(30)
            continue


Thread(target=post_heartbeat).start()

while (True):
    try:
        work()
    except:
        print(time.asctime(time.localtime(time.time())), "监测出错，请检查网络是否连通。")
        time.sleep(1)
        continue
    time.sleep(random.randint(300, 600))  # 这里间隔20~40秒查询一次状态，切莫太频繁
