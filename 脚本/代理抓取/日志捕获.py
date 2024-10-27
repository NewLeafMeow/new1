import io
import sys
import os

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def 开始捕获日志():
    # 设置工作目录为脚本所在的目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建一个 StringIO 对象，用于捕获输出
    output = io.StringIO()

    # 保存原始标准输出和标准错误
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # 将 sys.stdout 和 sys.stderr 重定向到 StringIO
    sys.stdout = output
    sys.stderr = output
    
    # 返回 StringIO 对象和原始 stdout、stderr，以便稍后还原
    return output, original_stdout, original_stderr

def 停止捕获日志(output, original_stdout, original_stderr):
    # 还原标准输出和标准错误
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    
    # 获取捕获的输出内容
    return output.getvalue()

# 示例主程序
if __name__ == '__main__':
    # 开始捕获日志
    output, original_stdout, original_stderr = 开始捕获日志()
    
    # 测试输出
    print("这是第一个测试输出")
    print("这是第二个测试输出")
    print("控制台输出被捕获到这里")

    # 停止捕获并获取日志内容
    日志内容 = 停止捕获日志(output, original_stdout, original_stderr)
    
    # 打印捕获的内容
    print("捕获的日志内容:\n", 日志内容)
