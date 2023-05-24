# 解决问题
宿舍电脑频繁下线, 上线后ip地址改变, 导致无法连接远程桌面

此脚本可以**自动重连校园网**并向服务器**发送ip地址**

在任何地方都可收到ip地址, 从而连接远程桌面

# 使用方法
1. 开启无感认证, 填写main.py中dataLogin和dataCheck的字段
2. 有一台服务器, 填写main.py中的target_url
3. 在本地运行main.py
4. 在服务器上运行app.py, 注意有flask和uvicorn的依赖
5. 之后curl http://服务器ip:端口/info 即可获取ip地址