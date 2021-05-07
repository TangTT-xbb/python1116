from multiprocessing import Process
class Process_Class(Process):
    def __init__(self,name):
        #  直接调用父类的构造方法
        # Process.__init__()
        super(Process_Class, self).__init__()
        # 初始化赋值
        self.name = name
    def run(self):
        print("我是Process继承类",self.name)

# 创建子进程
p1 = Process_Class('TTT')
p1.start()
