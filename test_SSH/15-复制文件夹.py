# 复制文件夹

import os
import sys
from multiprocessing import Pool, Manager


def copy_file(file, old_dir, new_dir, queue):
    # 1.打开老文件
    fr = open(old_dir + "/" + file, "rb")
    # 2. 打开新的文件
    fw = open(new_dir + "/" + file, "wb")
    # 3. 取出老文件的内容
    buf = fr.read()
    # 4. 把这个内容写入
    fw.write(buf)
    # 5. 关闭文件
    fr.close()
    fw.close()
    # 把文件名推到队列中去
    queue.put(file)


def main():
    # 创建一个队列
    global new_dir, old_dir
    queue = Manager().Queue()
    try:
        old_dir = sys.argv[1]
        new_dir = sys.argv[2]
    except:
        print("使用方法：python3 " + sys.argv[0] + " 源目录 新目录")
        exit(0)
    try:
        os.mkdir(new_dir)
    except:
        pass
    files = os.listdir(old_dir)
    # 创建进程池
    pool = Pool(3)

    for file in files:
        pool.apply_async(copy_file, (file, old_dir, new_dir))

    # 关闭进程池
    pool.close()
    # 进度条
    files_len = len(files)
    # 已完成的文件数
    files_count = 0

    while True:
        # 当满足条件的时候就退出
        if files_count == files_len:
            print()
            break
        # 从队列中取出来，如果有就files_count就加1
        if queue.get():
            files_count += 1
            print("\r 当前已完成：%.2f %%" % (files_count / files_len * 100), end="")

    # 等待结束
    pool.join()


if __name__ == "__main__":
    main()
