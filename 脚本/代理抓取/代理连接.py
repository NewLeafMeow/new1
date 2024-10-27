import subprocess
import platform
import os
import ctypes
import sys

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

# 设置系统代理
def 设置系统代理(代理_IP, 代理端口):
    if platform.system() == "Windows":
        try:
            # 设置 WinHTTP 代理
            subprocess.run(f"netsh winhttp set proxy {代理_IP}:{代理端口}", shell=True, check=True)
            文本=(f"已设置 WinHTTP 代理为 {代理_IP}:{代理端口}")

            # 设置 WinINET 代理
            subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f', shell=True, check=True)
            subprocess.run(f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d "{代理_IP}:{代理端口}" /f', shell=True, check=True)
            文本+=(f"已设置 WinINET 代理为 {代理_IP}:{代理端口}")

            # 查看当前 WinHTTP 代理设置
            文本+=("当前 WinHTTP 代理设置：")
            result = subprocess.run("netsh winhttp show proxy", shell=True, capture_output=True, text=True, check=True)
            文本+=(result.stdout)

            # 查询 WinINET 代理设置
            文本+=("当前 WinINET 代理设置：")
            result = subprocess.run('reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                文本+=(result.stdout)
            else:
                文本+=(f"查询 WinINET 代理设置时发生错误: {result.stderr}")

        except subprocess.CalledProcessError as e:
            文本+=(f"设置代理时发生错误: {e}")
        except Exception as e:
            文本+=(f"无法连接: {e}")

    return 文本

# 关闭系统代理
def 关闭系统代理():
    if platform.system() == "Windows":
        try:
            # 清除 WinHTTP 代理
            subprocess.run("netsh winhttp reset proxy", shell=True, check=True)
            添加文本("已关闭 WinHTTP 代理")

            # 清除 WinINET 代理
            subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f', shell=True, check=True)
            subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /f', shell=True, check=True)
            添加文本("已关闭 WinINET 代理")

        except subprocess.CalledProcessError as e:
            添加文本(f"关闭代理时发生错误: {e}")
        except Exception as e:
            添加文本(f"无法关闭代理: {e}")

# 示例调用
if __name__ == '__main__':
    设置系统代理("61.129.2.212", "8080")  # 替换为您的代理 IP 和端口
    
    # 这里是程序的主要逻辑，您可以在这里运行任何需要代理的任务

    # 程序结束时关闭代理
    关闭系统代理()
