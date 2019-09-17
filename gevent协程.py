import gevent
from gevent import monkey
monkey.patch_time()
from time import sleep

def fun(a, b):
    print('run fun..', a, b)
    sleep(3)
    print('结束fun')


def fun1():
    print('run fun1..')
    sleep(2)
    print('结束fun1')


f = gevent.spawn(fun, 1, 2)
f2 = gevent.spawn(fun1)
gevent.joinall([f,f2])#阻塞