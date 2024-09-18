import sys
import random
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
from PyQt5.QtMultimedia import QSound

class a(QWidget):
    # 初始化方法
    def __init__(self):
        super(a, self).__init__()  # 调用父类的构造函数
        self.initUi()  # 初始化用户界面
        self.tray()  # 创建系统托盘
        self.is_follow_mouse = False  # 初始化鼠标跟随标志
        self.鼠标状态双击=False
        self.is_flying = False  # 初始化飞行标志
        self.mouse_drag_pos = self.pos()  # 初始化鼠标拖动位置
        # 定时器，每隔一段时间做一次动作
        self.timer = QTimer()#动作切换
        self.timer.timeout.connect(self.am)
        self.timer.start(120)
        # 定时器，每隔一段时间做一次动作
        self.timer1 = QTimer()#随机
        self.timer1.timeout.connect(self.amrdm)
        self.timer1.start(3000)
        # 定时器，每隔一段时间做一次动作
        self.timer2 = QTimer()#左右移动

    # 初始化用户界面
    def initUi(self):
        self.w = 500  # 初始化窗口x位置
        self.h = 500  # 初始化窗口y位置
        self.direction = 1  # 初始化方向
        self.action = 1  # 初始化动作（路径）
        self.setGeometry(self.w, self.h, 308, 270)  # 设置窗口位置和大小
        self.lbl = QLabel(self)  # 创建一个 QLabel 控件
        self.frame = 1  # 初始化帧数（路径）
        self.pic_url = 'AstrumAureus\AstrumAureus\AstrumAureus' + str(self.action)+str(self.frame) + '.png'  # 设置初始图片路径
        self.pm = QPixmap(self.pic_url)  # 创建 QPixmap 对象并设置图片
        self.lbl.setPixmap(self.pm)  # 在 QLabel 控件中显示图片
        # 设置窗口属性，使其无边框、置顶、背景透明
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()  # 显示窗口
        self.repaint()  # 重绘窗口
        self.temp=0#随机数-移动

    # 创建系统托盘
    def tray(self):
        tp = QSystemTrayIcon(self)  # 创建系统托盘图标对象
        tp.setIcon(QIcon('AstrumAureus\AstrumAureus_BossChecklist.png'))  # 设置托盘图标
        ation_quit = QAction('退出', self, triggered=self.quit)  # 创建退出动作
        tpMenu = QMenu(self)  # 创建菜单
        tpMenu.addAction(ation_quit)  # 将退出动作添加到菜单中
        tp.setContextMenu(tpMenu)  # 设置托盘图标的右键菜单
        tp.show()  # 显示托盘图标

    #动画
    def am(self):
        if self.action!=2:
            self.timer2 = None

        #帧
        if self.frame<6:
            self.frame+=1
        else:
            self.frame=1
            
        #走
        if self.action==2:
            if self.w<-400:
                    self.w=1920
            elif self.w>1920:
                    self.w=-380
            self.timer2 = QTimer()#位移
            self.timer2.timeout.connect(self.walk)
            self.timer2.start(10)

        #刷新图片
        self.pic_url = 'AstrumAureus\AstrumAureus\AstrumAureus' + str(self.action)+str(self.frame) + '.png'  # 更新图片路径
        self.pm = QPixmap(self.pic_url)  # 创建 QPixmap 对象并设置图片
        self.lbl.setPixmap(self.pm)
    
    #移动
    def walk(self):
        self.w+=self.direction
        self.move(self.w,self.h)

    #随机
    def amrdm(self):
        self.jptm=False
        if self.temp <=0.6 and self.temp>=0:#状态平滑
            self.action=1
            self.temp = 1
            return
        self.temp = random.random()#随机数
        if self.temp > 0.6:  #静止
            self.action=1
        elif self.temp>0.3:#右移
            self.action=2
            self.direction = 1
        else:#左移
            self.action=2
            self.direction = -1

    # 鼠标按下事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  # 如果是左键按下
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()  # 记录鼠标拖动的位置
            event.accept()  # 接受事件
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 设置鼠标形状为手型
        elif event.button() == Qt.RightButton:  # 如果是右键按下
           self.is_follow_mouse = False

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.is_follow_mouse:  # 如果是左键按下且鼠标跟随状态为True
            self.move(event.globalPos() - self.mouse_drag_pos)  # 移动窗口到鼠标拖动位置
            xy = self.pos()  # 获取窗口当前位置
            self.w, self.h = xy.x(), xy.y()  # 获取窗口左上角坐标
            event.accept()  # 接受事件
            self.action = 3

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        self.鼠标状态双击=True

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False  # 设置鼠标跟随状态为False
        self.setCursor(QCursor(Qt.ArrowCursor))  # 设置鼠标形状为箭头
        if self.鼠标状态双击==False:
            self.action = 1
        self.鼠标状态双击=False

    # 托盘退出
    def quit(self):
        self.close()  # 关闭窗口
        sys.exit()  # 退出应用程序

# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建应用程序对象
    myPet = a()  # 创建 a 类的实例对象
    sys.exit(app.exec_())  # 运行应用程序，直到窗口关闭并退出程序