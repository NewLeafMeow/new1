import os
import asyncio
import 代理获取
import 代理测试异步

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def 去重代理(代理列表):
    唯一代理列表 = []  # 存储去重后的代理
    已见IP = set()  # 存储已经见过的IP

    for 代理 in 代理列表:
        ip = 代理[1]  # 获取代理元组中的IP（假设元组格式为 (协议, ip, 端口, 延迟)）
        if ip not in 已见IP:
            已见IP.add(ip)  # 记录已经见过的IP
            唯一代理列表.append(代理)  # 添加到去重后的列表中

    return 唯一代理列表

# 示例使用
代理列表 = [
    ('http', '192.168.0.1', '8080', 100),
    ('socks5', '192.168.0.2', '1080', 200),
    ('http', '192.168.0.1', '8081', 150),  # 重复IP
    ('http', '192.168.0.3', '8080', 250),
]

去重后的代理 = 去重代理(代理列表)
print(去重后的代理)
