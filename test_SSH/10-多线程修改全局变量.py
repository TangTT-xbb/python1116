import time
from threading import Thread

num = 100

def write():
    global num
    num += 1
    print(f"write num: {num}")

def read():
    print(f"read num：{num}")

tw = Thread(target=write)
tr = Thread(target=read)
#  启动线程

tw.start()
time.sleep(2)
tr.start()
print(f"主线程：{num}")
