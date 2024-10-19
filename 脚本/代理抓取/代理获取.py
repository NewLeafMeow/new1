import requests

# 目标下载URL
下载网址 = 'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text'
默认文件名 = '代理文件.txt'

# 下载代理文件并保存
def 下载代理文件():
    try:
        响应 = requests.get(下载网址)
        响应.raise_for_status()  # 检查请求是否成功
        with open(默认文件名, 'wb') as 文件:
            文件.write(响应.content)
        print(f"文件已下载并保存为: {默认文件名}")
    except Exception as e:
        print(f"下载失败，错误: {e}")

# 读取文件并提取代理信息
def 读取代理信息():
    代理列表 = []
    try:
        with open(默认文件名, 'r') as 文件:
            for 行 in 文件:
                行 = 行.strip()
                if 行:
                    if '://' in 行:
                        协议, 其余部分 = 行.split('://')
                        IP, 端口 = 其余部分.split(':')
                        代理列表.append((协议, IP, 端口))
        return 代理列表
    except Exception as e:
        print(f"读取文件失败，错误: {e}")
        return []

#输出代理信息
if __name__=="__main__":
    下载代理文件()
    代理列表=读取代理信息()
    for 协议,IP,端口 in 代理列表:
        print(f"协议:{协议}--ip:{IP}--端口:{端口}")