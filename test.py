import json

from urllib3 import encode_multipart_formdata

import requests

target_url = "" # 你的服务器地址
data = {
    "status": "111",
    "timestamp": "",
    "ipv4": "",
    "ipv6": "",
}

# 发送表单数据
res = requests.post(target_url, data=json.dumps(data))
print(res.text)