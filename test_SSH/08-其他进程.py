import os
# 创建进程
import time

pid = os.fork()

if pid == 0:
    while True:
        print(f"子进程pid{os.getpid()}  父进程pid{os.getppid()}")
        time.sleep(1)
else:
    print(f"父进程pid{os.getpid()}  爷爷进程pid{os.getppid()}")
    time.sleep(3)