import asyncio
import aiohttp
from aiohttp import ClientTimeout
from aiohttp_socks import ProxyConnector
from python_socks._errors import ProxyConnectionError
import 代理获取
import os
import time

# 设置工作目录为脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 测试单个代理的异步函数，带有重试机制和即时输出
async def 测试单个代理(协议, ip, 端口, 测试网址='https://httpbin.org/ip', 超时时间=10, 重试次数=1):
    for 尝试 in range(重试次数):
        try:
            开始时间 = time.time()  # 记录开始时间
            if 协议.startswith('socks'):
                连接器 = ProxyConnector.from_url(f"{协议}://{ip}:{端口}")
                async with aiohttp.ClientSession(connector=连接器) as 会话:
                    timeout = ClientTimeout(connect=超时时间, total=超时时间 * 2)
                    async with 会话.get(测试网址, timeout=timeout) as 响应:
                        响应.raise_for_status()
                        延迟 = int((time.time() - 开始时间) * 1000)  # 计算延迟并转为整数毫秒
                        print(f"{协议.upper()} 代理 {ip}:{端口} 可用，延迟: {延迟}毫秒")
                        return (协议, f"{ip}:{端口}", 延迟)
            else:
                代理 = {协议: f"{协议}://{ip}:{端口}"}
                timeout = ClientTimeout(connect=超时时间, total=超时时间 * 2)
                async with aiohttp.ClientSession() as 会话:
                    async with 会话.get(测试网址, proxy=代理[协议], timeout=timeout) as 响应:
                        响应.raise_for_status()
                        延迟 = int((time.time() - 开始时间) * 1000)  # 计算延迟并转为整数毫秒
                        print(f"{协议.upper()} 代理 {ip}:{端口} 可用，延迟: {延迟}毫秒")
                        return (协议, f"{ip}:{端口}", 延迟)
        except (aiohttp.ClientError, asyncio.TimeoutError, ProxyConnectionError, OSError) as 错误:
            if 尝试 == 重试次数 - 1:
                错误信息 = str(错误).split(':')[-1].strip()  # 仅保留错误的主要部分
                print(f"{协议.upper()} 代理 {ip}:{端口} 不可用，错误: {错误信息}")
                return (协议, f"{ip}:{端口}", None, 错误信息)
            await asyncio.sleep(1)

# 测试代理的异步主函数
async def 测试代理(代理列表, 测试网址='https://httpbin.org/ip', 超时时间=10):
    可用代理 = []  # 初始化可用代理列表
    任务列表 = []  # 初始化任务列表

    # 为代理列表中的每个代理创建任务
    for 协议, ip, 端口 in 代理列表:
        任务列表.append(测试单个代理(协议, ip, 端口, 测试网址, 超时时间))  # 将每个代理的测试任务加入任务列表
    
    try:
        结果 = await asyncio.gather(*任务列表, return_exceptions=True)  # 并发执行所有测试任务并收集结果
    except Exception as e:
        print(f"执行测试代理时发生错误: {e}")
        return []

    # 处理每个测试结果
    for 结果 in 结果:
        if isinstance(结果, Exception):  # 检查是否是异常
            print(f"发生错误: {结果}")
            continue
        if len(结果) == 3:  # 如果结果中没有错误
            协议, ip_端口, 延迟 = 结果  # 解包协议、IP和端口以及延迟
            ip,端口=ip_端口.split(":")
            print(f"{协议.upper()} 代理 {ip_端口} 可用，延迟: {延迟}毫秒")  # 打印代理可用的信息
            可用代理.append((协议,ip,端口,延迟))  # 将可用代理加入可用代理列表
        else:
            协议, ip_端口, _, 错误信息 = 结果  # 解包协议、IP和端口以及错误信息
            print(f"{协议.upper()} 代理 {ip_端口} 不可用，错误: {错误信息}")  # 打印代理不可用的信息
    
    return 可用代理  # 返回可用代理列表

# 运行异步测试
if __name__ == '__main__':
    代理列表 = 代理获取.读取代理信息('临时代理文件.txt')
    
    if not 代理列表:
        print("代理列表为空，无法测试。")
    else:
        可用代理 = asyncio.run(测试代理(代理列表))
        print("所有可用代理:", 可用代理)
