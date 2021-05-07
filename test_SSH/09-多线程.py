import time
from threading import Thread


#  创建线程
def work():
    print("当前线程")


def sing(i):
    for x in range(i):
        print(f"当前进程号：{t1.name}    正在唱歌")
        time.sleep(1)


def dance():
    for x in range(5):
        print(f"当前进程号：{t2.name}    正在跳舞")
        time.sleep(1)


t1 = Thread(target=sing, args=(4,))
t2 = Thread(target=dance)
#  启动线程
time_start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
time_end = time.time()
print("运行时间：",time_end-time_start)
