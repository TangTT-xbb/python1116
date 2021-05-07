# import os
# import time
#
# num = 0
# pid = os.fork()
# if pid == 0:
#     num += 1
#     print("子进程：", num)
# else:
#     num += 1
#     print("父进程：", num)
# pid = os.fork()
#
# if pid == 0:
#     num += 1
#     print("子进程：", num)
# else:
#     num += 1
#     print("父进程：", num)
#
# time.sleep(1)

import time
from multiprocessing import Process

num = 100

def write():
    global num
    num += 1
    print(f"write num: {num}")

def read():
    print(f"read num：{num}")

pw = Process(target=write)
pr = Process(target=read)
#  启动线程

pw.start()
time.sleep(2)
pr.start()
print(f"主线程：{num}")
