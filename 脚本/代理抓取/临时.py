import logging
import io

# 创建一个内存缓冲区
log_stream = io.StringIO()

# 设置 logging 配置
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# 添加一个 StreamHandler，用于打印到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# 添加一个 StreamHandler，用于捕获到内存缓冲区
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# 示例：使用 logger 代替 print 进行输出
logger.info("这是第一个输出")
print("这是第二个输出")

# 获取 log_stream 的内容
captured_output = log_stream.getvalue()
print("\n捕获的内容为：")
print(captured_output)


