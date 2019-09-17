""""""
import gevent
from gevent import monkey

monkey.patch_all()
from socket import *


def h(c):
    while True:
        data = c.recv(1024).decode()
        if not data:
            return
        print(data)
        c.send(b"OK")


s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 5656))
s.listen(3)

while True:
    c, addr = s.accept()
    print(addr)
    gevent.spawn(h,c)
