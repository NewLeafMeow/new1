import tkinter as tk
from tkinter import ttk
import asyncio
import threading
import time
import 代理获取
import 代理测试异步
import 代理连接
import sys
import ctypes
import os

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 检查是否具有管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # 重新启动程序以获取管理员权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

代理列表=[]

# 向数据列表中添加示例数据
def 刷新列表():
    数据列表.delete(0, tk.END)  # 清空数据列表
    for 索引, 元组 in enumerate(代理列表):  # 示例数据
        协议, ip, 端口, 延迟 = 元组
        数据列表.insert(tk.END, f"{索引+1}|\t{协议}://{ip}:{端口}---延迟:{延迟}")
    print("列表已刷新")

def 保存代理列表(文件名='代理文件.txt'):
    global 代理列表
    with open(文件名, 'w', encoding='utf-8') as 文件:
        for 代理 in 代理列表:
            协议, ip, 端口, 延迟 = 代理
            # 将协议、IP、端口和延迟格式化为字符串
            行 = f"{协议}://{ip}:{端口}---延迟:{延迟}\n"
            文件.write(行)  # 写入文件
    添加文本("文件已保存")

def 添加文本(内容):
    # 允许文本框修改
    运行文本.config(state="normal",font=("Consolas", 10))
    
    # 插入文本
    运行文本.insert(tk.END, 内容 + "\n")
    
    # 自动滚动到最后
    运行文本.see(tk.END)
    
    # 禁用文本框，防止手动编辑
    运行文本.config(state="disabled")

def 排序():
    global 代理列表
    代理列表 = sorted(代理列表, key=lambda x: int(x[-1]))
    保存代理列表()
    刷新列表()
    添加文本("..已重新排列")

def 新线程1():
    线程1 = threading.Thread(target=测试全部)
    线程1.start()
    
def 新线程3():
    线程3 = threading.Thread(target=获取新的代理)
    线程3.start()

代理列表=代理获取.完整读取("代理文件.txt")

# 创建主窗口
主窗口 = tk.Tk()
主窗口.title("root")
主窗口.geometry("800x600")

# 创建顶部菜单栏框架
顶部框架 = tk.Frame(主窗口)
顶部框架.pack(side=tk.TOP, fill=tk.X)

# 添加两个按钮到菜单栏
按钮1 = tk.Button(顶部框架, text="获取新的代理", command=lambda: 新线程3())
按钮1.pack(side=tk.LEFT, padx=5, pady=5)

按钮2 = tk.Button(顶部框架, text="测试全部", command=lambda: 新线程1())
按钮2.pack(side=tk.LEFT, padx=5, pady=5)

按钮3 = tk.Button(顶部框架, text="排序", command=lambda: 排序())
按钮3.pack(side=tk.LEFT, padx=5, pady=5)

# 创建一个可调整的主框架，分为左右两部分
主框架 = tk.PanedWindow(主窗口, orient=tk.HORIZONTAL)
主框架.pack(fill=tk.BOTH, expand=True)

# 左侧数据列表框架
左侧框架 = tk.Frame(主框架)
主框架.add(左侧框架, width=int(800 * 0.45))  # 设置左侧框架宽度为窗口的 70%

# 右侧运行数据框架
右侧框架 = tk.Frame(主框架, width=300)  # 设置右侧框架宽度为 300 像素
主框架.add(右侧框架)

# 数据列表标题标签
列表标签 = tk.Label(左侧框架, text="数据列表", font=("Arial", 12))
列表标签.pack(anchor="w", padx=10, pady=5)

# 创建滚动条和数据列表框
列表框架 = tk.Frame(左侧框架)
列表框架.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# 添加滚动条
列表滚动条 = tk.Scrollbar(列表框架)
列表滚动条.pack(side=tk.RIGHT, fill=tk.Y)

# 创建数据列表并绑定滚动条
数据列表 = tk.Listbox(列表框架, yscrollcommand=列表滚动条.set)
数据列表.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
列表滚动条.config(command=数据列表.yview)

# 运行数据标题标签
运行标签 = tk.Label(右侧框架, text="运行数据", font=("Arial", 12))
运行标签.pack(anchor="w", padx=10, pady=5)

# 创建只读运行数据文本框并设置滚动条
运行文本 = tk.Text(右侧框架, wrap=tk.WORD, height=20, state="disabled")
运行文本.pack(fill=tk.BOTH, expand=True)

# 为运行数据文本框添加滚动条
运行滚动条 = tk.Scrollbar(运行文本, command=运行文本.yview)
运行文本.config(yscrollcommand=运行滚动条.set)
运行滚动条.pack(side=tk.RIGHT, fill=tk.Y)

刷新列表()

# 右键菜单弹出函数
def 显示右键菜单(事件):
    # 获取被右击的列表项
    try:
        选中索引 = 数据列表.nearest(事件.y)  # 获取鼠标点击处最近的列表项索引
        选中数据 = 数据列表.get(选中索引)  # 获取选中的数据项内容
    except:
        return

    # 定义按钮点击事件，打印选中的数据名称和按钮名称
    def 点击按钮(按钮名称):
        协议,ip,端口,延迟 = 代理列表[选中索引]
        添加文本(代理连接.设置系统代理(ip,端口))

    # 创建右键菜单
    右键菜单 = tk.Menu(主窗口, tearoff=0)
    右键菜单.add_command(label="连接", command=lambda: 点击按钮("连接"))
    右键菜单.add_command(label="删除", command=lambda: 点击按钮("删除"))

    # 显示右键菜单
    右键菜单.tk_popup(事件.x_root, 事件.y_root)

# 绑定右键点击事件到数据列表
数据列表.bind("<Button-3>", 显示右键菜单)

def 获取新的代理():
    按钮2.config(state="disabled")
    代理获取.下载代理文件("临时代理文件.txt")
    按钮2.config(state="normal")
    添加文本("/代理已获取----")

def 测试全部():
    global 代理列表
    按钮1.config(state="disabled")
    按钮2.config(state="disabled")
    
    临时代理列表 = 代理获取.读取代理信息("临时代理文件.txt")
    临时代理列表 = asyncio.run(测试代理异步(临时代理列表))

    代理列表 = 代理获取.文件读取("代理文件.txt")
    代理列表 = asyncio.run(测试代理异步(代理列表))

    代理列表=代理获取.去重代理(代理列表+临时代理列表)
    print(f"\n{代理列表}\n")

    保存代理列表()
    刷新列表()
    按钮1.config(state="normal")
    按钮2.config(state="normal")
    添加文本(f"可用列表: {代理列表}")
    添加文本("测试完成!!")

async def 测试代理异步(列表名):
    代理列表 = await 代理测试异步.测试代理(列表名)
    return 代理列表

主窗口.mainloop()

代理连接.关闭系统代理()

sys.exit()