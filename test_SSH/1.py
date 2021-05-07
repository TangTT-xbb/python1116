import os
import time


def sing():
    for x in range(5):
        print("正在唱歌")
        time.sleep(1)


def dance():
    for x in range(5):
        print("正在跳舞")
        time.sleep(1)

# pid 子进程
pid = os.fork()
if pid == 0:
    sing()
else:
    dance()

print("ok")
