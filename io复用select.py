"""
select  tcp 服务
"""
from socket import *
from select import select

sockfd = socket(AF_INET, SOCK_STREAM)
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockfd.bind(('127.0.0.1', 3939))
sockfd.listen(3)

rlist = [sockfd]  # 等待事件   等待客户端连接
wlist = []  # 主动事件
xlist = []  # 异常事件

while True:
    rs, ws, xs = select(rlist, wlist, xlist)
    for i in rs:  # rs是当前就绪的对象
        if i is sockfd:#如果这个对象是连接对象，处理一下事件
            c, addr = rs[0].accept()
            print('客户端：', addr)
            rlist.append(c)
        else:#如果这个对象是消息对象，处理一下事件
            data = i.recv(1024).decode()
            if not data:#如果发送的数据为空  说明客户端退出
                rlist.remove(i)  # 取消对这个IO的关注
                i.close()
                continue
            print('客户端：',data)
            wlist.append(i)

    for w in ws:
        w.send(b'OK')
        wlist.remove(w)#OK 表示收到消息 只发一次  发过后取消关注