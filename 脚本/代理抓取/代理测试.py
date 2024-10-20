import requests
import time
import socks
import socket
import 代理获取

# 测试HTTP和SOCKS代理的可用性和延迟
def 测试代理(代理列表, 测试网址='https://httpbin.org/ip', 超时时间=5):
    可用代理 = []
    
    for 协议, ip, 端口 in 代理列表:
        端口 = int(端口)
        代理 = {协议: f"{协议}://{ip}:{端口}"}
        
        if 协议 == 'http':
            # 测试HTTP代理
            try:
                开始时间 = time.time()
                响应 = requests.get(测试网址, proxies=代理, timeout=超时时间)
                响应.raise_for_status()
                延迟 = time.time() - 开始时间
                print(f"HTTP代理 {ip}:{端口} 可用，延迟: {延迟:.2f}秒")
                可用代理.append((协议, ip_端口, 延迟))
            except Exception as e:
                print(f"HTTP代理 {ip}:{端口} 不可用，错误: {e}")
        
        elif 协议 == 'socks4' or 协议 == 'socks5':
            # 测试SOCKS4/5代理
            try:
                socks.set_default_proxy(socks.SOCKS5 if 协议 == 'socks5' else socks.SOCKS4, ip, 端口)
                socket.socket = socks.socksocket
                开始时间 = time.time()
                响应 = requests.get(测试网址, timeout=超时时间)
                响应.raise_for_status()
                延迟 = time.time() - 开始时间
                print(f"{协议.upper()} 代理 {ip}:{端口} 可用，延迟: {延迟:.2f}秒")
                可用代理.append((协议, ip_端口, 延迟))
            except Exception as e:
                print(f"{协议.upper()} 代理 {ip}:{端口} 不可用，错误: {e}")
    
    return 可用代理

# 示例代理列表 [(协议, ip:端口)]
代理列表 = [
    ('http', '123.456.78.90:8080'),
    ('socks5', '98.76.54.32:1080')
]

# 测试代理可用性
if __name__=="__main__":
    代理获取.下载代理文件()
    代理列表=代理获取.读取代理信息()
    测试代理(代理列表)
