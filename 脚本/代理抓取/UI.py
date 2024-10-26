import tkinter as tk
from tkinter import messagebox
from tkinter import Tk, Menu
import asyncio
import os
import 代理获取
import 代理测试异步
import subprocess
import platform

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

代理列表=[]

# 创建主窗口
主窗口 = tk.Tk()
主窗口.title("菜单示例")
主窗口.geometry("800x600")

# 设置系统代理
def 设置系统代理(代理_IP, 代理端口):
    if platform.system() == "Windows":
        # 设置代理
        subprocess.run(f"netsh winhttp set proxy {代理_IP}:{代理端口}", shell=True)
        print(f"已设置 Windows 系统代理为 {代理_IP}:{代理端口}")
        
        # 查看当前代理设置
        print("当前代理设置：")
        subprocess.run("netsh winhttp show proxy", shell=True)

def 抓取():
    global 代理列表
    代理获取.下载代理文件('临时代理文件.txt')
    代理列表=代理获取.读取代理信息('临时代理文件.txt')

async def 测试代理异步():
    global 代理列表
    代理列表 = await 代理测试异步.测试代理(代理列表)

def 测试():
    asyncio.run(测试代理异步())  # 在测试中调用异步函数
    print(代理列表)

抓取()
测试()

# 显示菜单的函数
def 显示菜单(event, 按钮名称):
    # 清空之前的菜单项
    菜单.delete(0, tk.END)

    # 为菜单动态添加菜单项
    菜单.add_command(label=f"连接", command=lambda: 按钮操作(按钮名称, "连接"))
    菜单.add_command(label=f"操作 2", command=lambda: 按钮操作(按钮名称, "操作 2"))

    # 在鼠标点击位置显示菜单
    菜单.post(event.x_root, event.y_root)

# 按钮操作的函数
def 按钮操作(按钮名称, 操作名称):
    print(按钮名称)#"-{i}——{协议}/{ip}:{端口}\t|{延迟}-"
    前缀, 后缀 = 按钮名称.split("——")  # 拆分出前缀和后缀
    协议, ip_端口_延迟 = 后缀.split("/")  # 进一步拆分后缀
    ip, 端口_延迟 = ip_端口_延迟.split(":") 
    端口, 延迟 = 端口_延迟.split("\t|")
    if(操作名称=="连接"):
        设置系统代理(ip, int(端口))

# 创建菜单
菜单 = Menu(主窗口, tearoff=0)

# 创建 Canvas 和 Scrollbar
画布 = tk.Canvas(主窗口)
滚动条 = tk.Scrollbar(主窗口, orient="vertical", command=画布.yview)
滚动条.pack(side=tk.RIGHT, fill=tk.Y)

# 创建一个 Frame 来包含按钮
按钮框架 = tk.Frame(画布)

# 配置画布
画布.create_window((0, 0), window=按钮框架, anchor='nw')
画布.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
画布.config(yscrollcommand=滚动条.set)

# 鼠标滚动事件
def 滚动(event):
    # 根据鼠标滚轮的方向调整滚动
    画布.yview_scroll(int(-1*(event.delta/120)), "units")

# 绑定鼠标滚轮事件
画布.bind_all("<MouseWheel>", 滚动)  # Windows 和 MacOS
画布.bind_all("<Button-4>", lambda event: 画布.yview_scroll(-1, "units"))  # Linux 向上滚动
画布.bind_all("<Button-5>", lambda event: 画布.yview_scroll(1, "units"))   # Linux 向下滚动

# 代理数量
for i in range(len(代理列表)):
    协议, ip_端口, 延迟 = 代理列表[i]
    ip, 端口 = ip_端口.split(":") 
    按钮名称 = f"-{i}——{协议}/{ip}:{端口}\t|{延迟}ms-"# 定义按钮名称
    按钮 = tk.Button(按钮框架, text=按钮名称, font=("Arial", 8),width=60,anchor='w')
    按钮.pack(pady=1,anchor="w")  # 上下排列按钮
    按钮.bind("<Button-3>", lambda event, name=按钮名称: 显示菜单(event, name))  # 绑定右键点击事件

# 更新画布的滚动区域
def 更新滚动区域(event):
    # 更新滚动区域
    画布.config(scrollregion=画布.bbox("all"))

# 绑定框架的配置事件
按钮框架.bind("<Configure>", 更新滚动区域)

# 运行主循环
主窗口.mainloop()