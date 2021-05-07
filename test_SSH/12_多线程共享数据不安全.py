from threading import Thread,Lock

num = 0
# 定义两个函数

def add1():
    global num
    # 上锁   理论：锁住最小的单元
    lock.acquire()
    for i in range(1000000):

        num += 1
        # 第一步： num
        # 第二步： temp = num + 1
        # 第三步： num = temp
    # 解锁
    lock.release()
    print(f"add1：{num}")
def add2():
    global num
    # 上锁
    lock.acquire()

    for i in range(1000000):
        num += 1
    # 解锁
    lock.release()
    print(f"add2：{num}")

# 创建一把锁
lock = Lock()

# 创建线程
t1 = Thread(target=add1)
t2 = Thread(target=add2)
# 启动线程
t1.start()
t2.start()
t1.join()
t2.join()
print(f"num: {num}")

# 当这个进程任务多的时候，CPU分配的时间越少，，一个任务还没有执行完，第二个就开始了，，

# 加锁解决
