"""
POLL步骤：
【1】创建套接字
【2】将套接字register
【3】创建查找字典,并维护
【4】循环监控IO发生
【5】处理发生的IO
"""
from socket import *
from select import *

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 6868))
s.listen(3)

p = poll()#创建poll对象

fdmap = {s.fileno(): s}#将文件描述符与要操作的对象对应

p.register(s, POLLIN | POLLERR)#将对象的事件进行关注

while True:#循环监控IO事件
    events = p.poll()#阻塞等待io事件发生
    for fd, event in events:#遍历发生io事件的列表
        if fd == s.fileno():#如果该事件是连接事件
            c, addr = fdmap[fd].accept()
            print('客户端ip:', addr)
            p.register(c, POLLIN)#将对象的事件进行关注
            fdmap[c.fileno()] = c#
        elif event & POLLIN:
            data = fdmap[fd].recv(1024).decode()
            if not data:
                p.unregister(fd)
                fdmap[fd].close()
                del fdmap[fd]
                continue
            print(data)
            p.register(fd, POLLOUT)
            # fdmap[fd].send(b'OK')
        elif event & POLLOUT:
            fdmap[fd].send(b'OK')
            p.register(fd, POLLIN)
