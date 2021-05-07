import time
from multiprocessing import Pool

def work(i):
    print("当前i: " ,i)
    time.sleep(1)


# 创建进程池
p1 = Pool(10)
 
# 批量创建10个任务
for x in range(100):
    p1.apply_async(work,args=(x,))

# 关闭之后不能再添加任务
p1.close()
# 等待结束
time_start = time.time()
p1.join()
time_end = time.time()
print("运行总时间：",time_end-time_start)