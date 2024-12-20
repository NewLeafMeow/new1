from flask import Flask
from flask_cors import CORS
import random
from flask_socketio import SocketIO, Namespace, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # 允许所有来源访问

class GameNamespace(Namespace):
    # 游戏参数和状态
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.BOARD_SIZE = 10  # 棋盘大小
        self.MINES = 10  # 地雷数量
        self.game_started = False  # 游戏是否已经开始
        self.game_over = False #游戏是否失败
        self.game_victory = False #游戏是否胜利
        self.board, self.revealed, self.flags = self.generate_board()  # 棋盘、揭示状态、旗帜状态

    # 检查棋盘是否有效（无封闭环路）
    def is_board_valid(self, board):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if board[row][col] != -1:  # 找到一个空白区域作为开始点
                    start_row, start_col = row, col
                    break
        revealed_copy = [[False] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.dfs(board, revealed_copy, start_row, start_col)
        
        # 如果所有非雷位置都已展开，则棋盘有效
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if board[row][col] != -1 and not revealed_copy[row][col]:
                    return False
        return True

    # 深度优先搜索，用于模拟展开空白区域
    def dfs(self, board, revealed, row, col):
        if revealed[row][col]:
            return
        revealed[row][col] = True
        if board[row][col] == 0:  # 如果是空白区域，继续展开
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                        self.dfs(board, revealed, r, c)

    # 生成地雷的函数
    def generate_mines(self, board, num_mines, first_click_row, first_click_col):
        mines_placed = 0
        mines = set()

        while mines_placed < num_mines:
            row = random.randint(0, self.BOARD_SIZE - 1)
            col = random.randint(0, self.BOARD_SIZE - 1)

            # 如果该位置已有地雷，或是第一次点击的格子，跳过
            if (row, col) in mines or (row == first_click_row and col == first_click_col):
                continue

            # 暂时放置一个地雷
            board[row][col] = -1
            mines.add((row, col))

            # 检查是否会形成封闭环路
            if self.is_board_valid(board):
                mines_placed += 1
            else:
                # 如果形成封闭环路，撤销该地雷
                board[row][col] = 0
                mines.remove((row, col))

        return board

    # 生成一个初始棋盘
    def generate_board(self):
        board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        revealed = [[False for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        flags = [[False for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        return board, revealed, flags

    #发送游戏信息
    def send(self):
        game_state = {  'board': self.board, 
                        'revealed': self.revealed, 
                        'flags': self.flags, 
                        'game_over': self.game_over, 
                        'game_victory': self.game_victory}
        emit('game_state', game_state, broadcast=True)

    # 空白开片
    def openwhite(self):
        for row_ in range(self.BOARD_SIZE):
            for col_ in range(self.BOARD_SIZE):
                if self.board[row_][col_] == 0:
                    for r in range(row_ - 1, row_ + 2):
                        for c in range(col_ - 1, col_ + 2):
                            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                                self.revealed[r][c] = True

    # 检测游戏胜利
    def gameVt(self):
        self.game_victory = True
        for row_ in range(self.BOARD_SIZE):
            for col_ in range(self.BOARD_SIZE):
                if self.board[row_][col_] >= 0 and not self.revealed[row_][col_]:
                    self.game_victory = False
                    '''^^^^^^^^^^^^'''
                    print("胜利")
                    '''
                    预留
                    '''
                    break
        if self.game_victory:
            self.send()

    @app.route('/')
    def index():
        return "服务器正在运行"

    # 启动时发送初始的游戏状态
    def on_connect(self):
        self.send()

    # 处理前端的揭示格子请求
    def on_reveal_cell(self, data):
        row, col = data['row'], data['col']
        if self.revealed[row][col]:
            return  # 已经揭示过的格子，不再处理

        if not self.game_started:
            self.game_started = True  # 游戏开始
            # 生成地雷并确保点击的格子不是地雷
            while True:
                self.board = self.generate_mines(self.board, self.MINES, row, col)  # 在第一次点击时生成地雷
                if self.board[row][col] != -1:  # 如果点击的格子不是地雷，则生成地雷
                    break
            # 填充数字
            for row_ in range(self.BOARD_SIZE):
                for col_ in range(self.BOARD_SIZE):
                    if self.board[row_][col_] == -1:
                        continue
                    # 计算相邻地雷数
                    for r in range(row_ - 1, row_ + 2):
                        for c in range(col_ - 1, col_ + 2):
                            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == -1:
                                self.board[row_][col_] += 1

        if self.board[row][col] == -1:  # 踩到地雷
            self.revealed[row][col] = True
            game_over = True
            '''^^^^^^^^^^^^'''
            print("失败")
            self.send()
            return

        # 揭开方块
        self.revealed[row][col] = True

        #开片
        self.openwhite()

        #检测胜利
        self.gameVt()

        # 状态上传
        self.send()
        print("揭开了", row, col)

    # 处理前端快速揭示请求
    def on_reveal_all_cell(self, data):
        row, col = data['row'], data['col']

        # 只处理已经揭示的格子
        if not self.revealed[row][col]:
            return
        
        # 获取该格子周围的旗子数量
        flag_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                    if self.flags[r][c]:
                        flag_count += 1

        # 如果旗子数量与该格子数字相等，则进行快速揭示
        if flag_count == self.board[row][col]:
            # 遍历该格子周围的八个格子
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                        if not self.revealed[r][c] and not self.flags[r][c]:
                            self.revealed[r][c] = True
                            print("揭开了", row, col,"!!")
                            if self.board[r][c] == -1:  # 如果踩到地雷，游戏结束
                                self.game_over = True
                                '''^^^^^^^^^^^^'''
                                print("失败")
                                return
                            # 如果没有地雷，继续检查是否为空白格子并递归揭示
                            if self.board[r][c] == 0:
                                self.on_reveal_all_cell({'row': r, 'col': c})  # 递归调用揭示周围空白格子

        #检测游戏胜利
        self.gameVt()

        # 状态上传
        self.send()


    # 处理前端的标记旗帜请求
    def on_flag_cell(self, data):
        row, col = data['row'], data['col']
        self.flags[row][col] = not self.flags[row][col]
        self.send()

# 注册命名空间
socketio.on_namespace(GameNamespace('/game扫雷'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
