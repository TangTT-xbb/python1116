import time
from multiprocessing import Process


def sing(i):
    for x in range(i):
        print(f"当前进程号：{p1.name}    正在唱歌")
        time.sleep(1)


def dance():
    for x in range(5):
        print(f"当前进程号：{p2.name}    正在跳舞")
        time.sleep(1)

p1 = None
p2 = None
def main():
    global p1,p2
    p1 = Process(target=sing, args=(3,))
    p2 = Process(target=dance)
    # 看看p1 是死 是活
    print("调用start()之前",p1.is_alive())

    # 启动进程  复制一份内存空间，引入代码
    # import 04_process
    p1.start()
    print("调用start()之后", p1.is_alive())
    p2.start()
    p1.terminate()
    p1.join()
    print("调用join()之后", p1.is_alive())
    p2.join(3)
     # 立即结束p1 进程


# 在windows下必须代码规范  放在__name__下
if __name__ == '__main__':
    # 开始时间
    time_start = time.time()

    main()
    # 结束时间
    time_end = time.time()
    # 总时间
    print("总时间：", time_end - time_start)
