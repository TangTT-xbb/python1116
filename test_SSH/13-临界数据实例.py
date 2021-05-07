import threading

value1 = 0
value2 = 0


def writer_worker():
    global value1
    global value2
    count = 0
    # 加锁

    while True:
        # lock.acquire()
        count += 1
        with lock:
            value1 = count
            value2 = count

        # lock.release()


def check_worker():
    while True:
        lock.acquire()
        if value2 != value1:
            print(f"+++++v1:{value1}++v2:{value2}+++")
        lock.release()


if __name__ == '__main__':
    t1 = threading.Thread(target=writer_worker, name="写线程")
    t2 = threading.Thread(target=check_worker, name="读线程")
    lock = threading.Lock()
    t1.start()
    t2.start()
