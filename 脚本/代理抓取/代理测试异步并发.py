import asyncio  # 导入 asyncio 库，用于异步编程
import aiohttp  # 导入 aiohttp 库，用于异步 HTTP 请求
from aiohttp import ClientTimeout  # 从 aiohttp 中导入 ClientTimeout 类，用于设置请求超时时间
from aiohttp_socks import ProxyConnector  # 从 aiohttp_socks 中导入 ProxyConnector，用于处理 SOCKS 代理连接
import 代理获取

# 测试单个代理的异步函数
async def 测试单个代理(协议, ip, 端口, 测试网址='https://httpbin.org/ip', 超时时间=5):
    # 如果是SOCKS代理，使用ProxyConnector
    if 协议.startswith('socks'):
        连接器 = ProxyConnector.from_url(f"{协议}://{ip}:{端口}")  # 创建 SOCKS 代理连接器
        async with aiohttp.ClientSession(connector=连接器) as 会话:  # 创建一个带有 SOCKS 代理的异步会话
            try:
                timeout = ClientTimeout(total=超时时间)  # 设置请求的超时时间
                async with 会话.get(测试网址, timeout=timeout) as 响应:  # 使用会话发送异步请求
                    响应.raise_for_status()  # 检查响应状态，如果不正常则抛出异常
                    return (协议, f"{ip}:{端口}", 响应.status)  # 返回代理的协议、IP和端口，以及响应状态码
            except (aiohttp.ClientError, asyncio.TimeoutError) as 错误:  # 处理客户端错误或超时异常
                return (协议, f"{ip}:{端口}", None, str(错误))  # 返回代理的协议、IP和端口，以及错误信息
    else:
        # 如果是HTTP代理，直接使用代理参数进行请求
        代理 = {协议: f"{协议}://{ip}:{端口}"}  # 构建 HTTP 代理字典
        try:
            timeout = ClientTimeout(total=超时时间)  # 设置请求的超时时间
            async with aiohttp.ClientSession() as 会话:  # 创建一个异步会话
                async with 会话.get(测试网址, proxy=代理[协议], timeout=timeout) as 响应:  # 使用代理发起异步请求
                    响应.raise_for_status()  # 检查响应状态，如果不正常则抛出异常
                    return (协议, f"{ip}:{端口}", 响应.status)  # 返回代理的协议、IP和端口，以及响应状态码
        except (aiohttp.ClientError, asyncio.TimeoutError) as 错误:  # 处理客户端错误或超时异常
            return (协议, f"{ip}:{端口}", None, str(错误))  # 返回代理的协议、IP和端口，以及错误信息

# 测试代理的异步主函数
async def 测试代理(代理列表, 测试网址='https://httpbin.org/ip', 超时时间=5):
    可用代理 = []  # 初始化可用代理列表
    任务列表 = []  # 初始化任务列表
    
    # 为代理列表中的每个代理创建任务
    for 协议, ip, 端口 in 代理列表:
        任务列表.append(测试单个代理(协议, ip, 端口, 测试网址, 超时时间))  # 将每个代理的测试任务加入任务列表
    
    结果 = await asyncio.gather(*任务列表)  # 并发执行所有测试任务并收集结果
    
    # 处理每个测试结果
    for 结果 in 结果:
        if len(结果) == 3:  # 如果结果中没有错误
            协议, ip_端口, 状态码 = 结果  # 解包协议、IP和端口以及状态码
            print(f"{协议.upper()} 代理 {ip_端口} 可用，状态码: {状态码}")  # 打印代理可用的信息
            可用代理.append((协议, ip_端口, 状态码))  # 将可用代理加入可用代理列表
        else:
            协议, ip_端口, _, 错误信息 = 结果  # 解包协议、IP和端口以及错误信息
            print(f"{协议.upper()} 代理 {ip_端口} 不可用，错误: {错误信息}")  # 打印代理不可用的信息
    
    return 可用代理  # 返回可用代理列表

# 运行异步测试
if __name__ == '__main__':
    代理获取.下载代理文件()
    代理列表=代理获取.读取代理信息()
    可用代理=测试代理(代理列表)
    print(可用代理)