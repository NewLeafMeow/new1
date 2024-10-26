import subprocess
import platform

代理_IP = "49.87.154.98"
代理端口 = "10800"

# 设置系统代理
def 设置系统代理(代理_IP, 代理端口):
    if platform.system() == "Windows":
        # 设置代理
        subprocess.run(f"netsh winhttp set proxy {代理_IP}:{代理端口}", shell=True)
        print(f"已设置 Windows 系统代理为 {代理_IP}:{代理端口}")
        
        # 查看当前代理设置
        print("当前代理设置：")
        subprocess.run("netsh winhttp show proxy", shell=True)

设置系统代理(代理_IP, 代理端口)