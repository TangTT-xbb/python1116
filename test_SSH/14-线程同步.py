import time
from threading import Thread, Lock


def f1():
    while True:
        if lock1.acquire():
            print("1")
            time.sleep(1)
            lock2.release()


def f2():
    while True:
        if lock2.acquire():
            print("2")
            time.sleep(1)
            lock3.release()


def f3():
    while True:
        if lock3.acquire():
            print("3")
            time.sleep(1)
            lock1.release()


# 创建进程
t1 = Thread(target=f1)
t2 = Thread(target=f2)
t3 = Thread(target=f3)

# 创锁
lock1 = Lock()
# 锁住2号
lock2 = Lock()
lock2.acquire()
# 锁住3号
lock3 = Lock()
lock3.acquire()
t1.start()
t2.start()
t3.start()
