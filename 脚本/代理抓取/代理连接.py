import subprocess
import platform
import os

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置系统代理
def 设置系统代理(代理_IP, 代理端口):
    if platform.system() == "Windows":
        # 设置代理
        subprocess.run(f"netsh winhttp set proxy {代理_IP}:{代理端口}", shell=True)
        print(f"已设置 Windows 系统代理为 {代理_IP}:{代理端口}")
        
        # 查看当前代理设置
        print("当前代理设置：")
        subprocess.run("netsh winhttp show proxy", shell=True)