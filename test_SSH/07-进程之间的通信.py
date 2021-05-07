import random
import time
from multiprocessing import Process, Queue


def write(queue):
    for x in ['A', 'B', 'C', 'D']:
        # 把 x 放入队列中
        queue.put(x)
        print(f"把{x}放到队列中了")
        # 设置休息时间
        time.sleep(random.random() * 2)


def read(queue):
    while True:
        print("读出：", queue.get(queue))

    # print('我在写')


# 创建队列  当没有参数时 无限大  以内存大小为基准
q = Queue()

#  创建进程
pw = Process(target=write, args=(q,))
pr = Process(target=read, args=(q,))
# 启动进程
pw.start()

pr.start()
# 等待结束
pw.join()
pr.join()
