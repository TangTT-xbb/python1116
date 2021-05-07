import os
pid = os.fork()
# pid 是当前进程的子PID
if pid == 0:
    print("子进程")
    print(f"子进程号：{pid}猜猜我会出现几次   当前进程号：{os.getpid()}  父进程：{os.getppid()}")

else:
    print("父进程")
    print(f"子进程号：{pid}猜猜我会出现几次   当前进程号：{os.getpid()}  父进程：{os.getppid()}")
