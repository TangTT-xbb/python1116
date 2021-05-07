from threading import Thread


# 定义自己的类
class MyThread(Thread):
    # 申明构造方法
    def __init__(self,name):
        super(MyThread, self).__init__()
        self.name = name

    def run(self):
        print(f"类继承方式{self.name}")


# 创建对象
mt = MyThread("hahah")
mt.start()