import threading
import time

# 定义线程要执行的函数
def print_hello():
    time.sleep(2)
    print("Hello from thread!")

# 创建一个线程
thread = threading.Thread(target=print_hello)

# 启动线程
thread.start()