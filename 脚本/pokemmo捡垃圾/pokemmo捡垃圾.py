import ctypes
import time
from pywinauto import Application
import random
import pyautogui
from pywinauto import Application
import keyboard
import itertools
from pywinauto import Desktop
import os
import cv2

# 获取当前脚本的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 切换到脚本所在的目录
os.chdir(script_dir)

# 定义虚拟键码
按键3 = 0x33

# 定义按键消息
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

def 时间(t):
    t = random.uniform(t - 0.05, t + 0.05)
    print(t)
    return t

def 按下(k, t):
    pyautogui.keyDown(k)
    time.sleep(时间(t))  # 按下的时间
    pyautogui.keyUp(k)

def 点击(pos):
    pyautogui.moveTo(pos)  # 移动到目标位置
    time.sleep(时间(0.1))  # 确保移动完成
    pyautogui.click()  # 执行点击

# 包含拉丁字母和西里尔字母的组合
characters = {
    'P': ['P', 'Р'],  # 拉丁 'P' 和西里尔 'Р'
    'o': ['o', 'о'],  # 拉丁 'o' 和西里尔 'о'
    'k': ['k', 'к'],  # 拉丁 'k' 和西里尔 'к'
    'e': ['e', 'е'],  # 拉丁 'e' 和西里尔 'е'
    'M': ['M', 'М'],  # 拉丁 'M' 和西里尔 'М'
    'O': ['O', 'О']   # 拉丁 'O' 和西里尔 'О'
}

# 生成所有可能的组合
def generate_combinations(characters):
    # 对 'PokeMMO' 的每个字符生成组合
    char_lists = [characters[c] for c in 'PokeMMO']
    all_combinations = list(itertools.product(*char_lists))
    return [''.join(combo) for combo in all_combinations]

# 获取所有窗口标题
def get_window_titles():
    windows = Desktop(backend="uia").windows()
    return [win.window_text() for win in windows if win.window_text().strip()]

# 比对窗口标题和PokeMMO的组合
def find_matching_window():
    poke_mmo_combinations = generate_combinations(characters)
    window_titles = get_window_titles()

    # 查找匹配的窗口标题
    for window_title in window_titles:
        for poke_title in poke_mmo_combinations:
            if window_title == poke_title:
                print(f"找到匹配的窗口标题: {window_title}")
                return window_title
    print("未找到匹配的窗口标题")
    return None

# 主程序3qq3
if __name__ == "__main__":
    window_title = find_matching_window()

# 使用 win32 后台模式连接到应用程序
app = Application(backend='win32').connect(title=window_title)

# 获取主窗口q
window = app.window(title=window_title)

# 打印窗口信息以确认
print("窗口标题:", window.element_info.name)

# 将窗口激活
window.set_focus()

# 获取窗口句柄
hwnd = window.handle

# 无限循环，持续执行操作
while True:
    try:
        # 检测是否按下了 'esc' 键，如果按下则退出循环
        if keyboard.is_pressed('esc'):
            print("检测到 Esc 键，程序退出")
            break

        # 查找图像 '鱼竿.png'
        text_location = pyautogui.locateOnScreen('鱼竿.png', confidence=0.8)

        if text_location:
            # 获取图像中心点坐标
            text_center = pyautogui.center(text_location)
            点击(text_center)
            print("点击了图像位置：", text_center)
        else:
            print("未找到图像位置")
        
        time.sleep(时间(0.2))

        按下("q", 0.1)

        # 查找图像 '闪光.png'
        # try:
        #     print(pyautogui.locateOnScreen('闪光.png', confidence=0.8),"\n发现闪光")
        #     break
        # except Exception as e:
        #     print(f"未发现闪光: {e}")
        
        # 查找图像 '战斗.png'
        text_location = pyautogui.locateOnScreen('战斗.png', confidence=0.8)

        if text_location:
            # 获取图像中心点坐标
            text_center = pyautogui.center(text_location)
            点击(text_center)
            print("点击了图像位置：", text_center)
        else:
            print("未找到图像位置")
        
        time.sleep(时间(0.2))

        # 查找图像 '聚宝功.png'
        text_location = pyautogui.locateOnScreen('聚宝功.png', confidence=0.8)

        if text_location:
            # 获取图像中心点坐标
            text_center = pyautogui.center(text_location)
            点击(text_center)
            print("点击了图像位置：", text_center)
        else:
            print("未找到图像位置")

        time.sleep(时间(0.2))

        # 检测图像 '萎了.png'
        if pyautogui.locateOnScreen('萎了.png', confidence=0.8):
            print("检测到 '萎了.png' 图像")
            time.sleep(时间(2))

            # 查找图像 '逃跑.png'
            text_location = pyautogui.locateOnScreen('逃跑.png', confidence=0.8)

            if text_location:
                # 获取图像中心点坐标q3
                text_center = pyautogui.center(text_location)
                点击(text_center)
                print("点击了图像位置：", text_center)
            else:
                print("未找到图像位置")

            time.sleep(时间(4))

            # 查找图像 '传送宠.png'
            text_location = pyautogui.locateOnScreen('传送宠.png', confidence=0.8)

            if text_location:
                # 获取图像中心点坐标q3
                text_center = pyautogui.center(text_location)
                点击(text_center)
                print("点击了图像位置：", text_center)
            else:
                print("未找到图像位置")

            time.sleep(时间(0.5))

            # 查找图像 '瞬间移动.png'
            text_location = pyautogui.locateOnScreen('瞬间移动.png', confidence=0.8)

            if text_location:
                # 获取图像中心点坐标q3
                text_center = pyautogui.center(text_location)
                点击(text_center)
                print("点击了图像位置：", text_center)
            else:
                print("未找到图像位置")

            time.sleep(时间(7))

            按下("space", 0.1)

            time.sleep(时间(3))

            按下("space", 0.1)

            time.sleep(时间(3))

            按下("space", 0.1)

            time.sleep(时间(3))

            按下("space", 0.1)

            time.sleep(时间(9))

            按下("space", 0.1)

            time.sleep(时间(2))

            按下("s", 3)

            time.sleep(时间(2))

            # 查找图像 '自行车.png'
            text_location = pyautogui.locateOnScreen('自行车.png', confidence=0.8)

            if text_location:
                # 获取图像中心点坐标
                text_center = pyautogui.center(text_location)
                点击(text_center)
                print("点击了图像位置：", text_center)
            else:
                print("未找到图像位置")
            
            time.sleep(时间(0.5))

            按下("a", 0.5)

            time.sleep(时间(0.5))

            按下("s", 0.33)

            time.sleep(时间(0.5))

            按下("d", 2)

        else:
            print("未找到 '行车了.png' 图像")

        time.sleep(时间(0.5))

    except Exception as e:
        print(f"未找到图片: {e}")
        # 即使出现错误也继续循环
        continue
