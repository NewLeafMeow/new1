from flask import Flask, render_template, request
from flask_cors import CORS
import random
from flask_socketio import SocketIO, Namespace, emit
from 房间分配 import Player,RoomManager

app扫雷 = Flask(__name__)
socketio = SocketIO(app扫雷, cors_allowed_origins="*")  # 允许所有来源访问

class GameNamespace(Namespace):
    # 游戏命名空间类，负责扫雷游戏逻辑的处理

    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.user_id=None
        self.user_name=None
        self.BOARD_SIZE = 10  # 棋盘大小
        self.MINES = 10  # 地雷数量
        self.game_started = False  # 游戏是否已经开始
        self.game_over = False  # 游戏是否失败
        self.game_victory = False  # 游戏是否胜利
        self.board, self.revealed, self.flags
        self.board, self.revealed, self.flags = self.generate_board()  # 初始化棋盘、揭示状态和旗帜状态
        self.aiting_players = []# 匹配队列，存储等待匹配的玩家
        self.plaers_data={}
        self.rooms_data = {}# 房间数据，存储每个房间内玩家的状态
        '''
        data = {
            'room_id': {
                'sid': {
                    self.user_id:'账号',
                    self.BOARD_SIZE: '棋盘大小',
                    self.MINES: '地雷数量',
                    self.game_started: '是否开始',
                    self.game_over: '是否失败',
                    self.game_victory: '是否胜利',
                    self.board: ['棋盘状态'],
                    self.revealed: ['揭示'],
                    self.flags: ['旗帜'],
                },
                'sid': {
                    '数据1': '值1',
                    '数据2': '值2',
                    ......
                    ......
                }
            }
        }
        '''

    
##################################################################################
#匹配——房间分配——连接/断开事件


    # 监听前台连接事件
    def on_connect(self):
        """监听玩家连接事件"""
        print(f"玩家 {request.sid} 已连接")

    # 监听匹配请求
    def on_start_match(self):
        """
        监听玩家发起匹配请求，
        如果有两个玩家匹配成功，就将他们分配到同一个房间，
        并通知前台进行倒计时。
        """
        global waiting_players, player_data, rooms_data
        print(f"玩家 {request.sid} 开始匹配，数据: {player_data}")

        self.user_id=self.
        self.user_name=
        #玩家信息字典
        player_data={
            request.sid:
                {
                    self.user_id, #账号
                    self.user_name, #用户名
                    self.BOARD_SIZE, # 棋盘大小
                    self.MINES, # 地雷数量,
                    self.game_started, # 游戏是否已经开始
                    self.game_over,  # 游戏是否失败
                    self.game_victory,  # 游戏是否胜利
                    self.board, #棋盘状态
                    self.revealed, #揭示状态
                    self.flags #旗帜状态
                }
            }
        
        # 向当前玩家发送匹配中的提示
        socketio.emit('match_status', {'status': '匹配中...'}, to=request.sid)
        
        # 将玩家数据加入等待队列
        waiting_players.append({'sid': request.sid, 'data': player_data})
        
        # 检查队列中是否有两名玩家可以进行匹配
        if len(waiting_players) >= 2:
            # 取出队列中的前两名玩家
            player1 = waiting_players.pop(0)
            player2 = waiting_players.pop(0)
            
            # 使用两个玩家的 sid 合并来生成房间ID
            room_id = f"{player1['sid']}_{player2['sid']}"
            
            # 将两名玩家加入同一个房间
            join_room(room_id, sid=player1['sid'])
            join_room(room_id, sid=player2['sid'])
            
            # 保存房间数据
            rooms_data[room_id] = {
                player1: player1['data'],
                player2: player2['data']
            }
            
            print(f"房间 {room_id} 匹配成功: 玩家1 {player1['data']}, 玩家2 {player2['data']}")
            
            # 通知玩家匹配成功，开始 3 秒倒计时
            for i in range(3, 0, -1):
                socketio.emit('match_status', {'status': f'匹配成功，{i} 秒后开始游戏'}, room=room_id)
                time.sleep(1)  # 模拟倒计时
            
            # 倒计时结束，发送匹配完成消息
            socketio.emit('match_success', {'room': room_id, 'players': [player1['data'], player2['data']]}, room=room_id)
            print(f"房间 {room_id} 倒计时结束，开始游戏！")

    # 监听断开连接事件
    def on_disconnect():
        """
        监听玩家断开连接事件，
        如果玩家在房间中，则从房间中移除并删除字典中的玩家数据，
        同时从匹配队列中删除该玩家。
        """
        global rooms_data, rooms_data, waiting_players
        player_sid = request.sid
        print(f"玩家 {player_sid} 已断开连接")
        
        # 从匹配队列中删除该玩家
        waiting_players = [player for player in waiting_players if player['sid'] != player_sid]
        
        # 检查玩家是否在任何房间中
        for room_id, room_data in list(rooms_data.items()):
            for player in list(room_data.keys()):
                if player['sid'] == player_sid:
                    # 如果玩家是房间中的玩家，移除该玩家并删除房间数据
                    leave_room(room_id, sid=player['sid'])
                    del room_data[player]
                    print(f"玩家 {player_sid} 从房间 {room_id} 中被移除")
                    
                    # 如果房间没有玩家了，删除该房间
                    if not room_data:
                        del data[room_id]
                    break

##################################################################
#游戏逻辑处理


    def is_board_valid(self, board):
        """
        检查棋盘是否有效（无封闭环路）
        """
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

    def dfs(self, board, revealed, row, col):
        """
        深度优先搜索，用于模拟展开空白区域
        """
        if revealed[row][col]:
            return
        revealed[row][col] = True
        if board[row][col] == 0:  # 如果是空白区域，继续展开
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                        self.dfs(board, revealed, r, c)

    def generate_mines(self, board, num_mines, first_click_row, first_click_col):
        """
        生成地雷，确保第一次点击的格子不是地雷且不会形成封闭环路
        """
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

    def generate_board(self):
        """
        生成一个初始棋盘，包括地雷分布、揭示状态和旗帜状态
        """
        board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        revealed = [[False for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        flags = [[False for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        return board, revealed, flags

    def send(self):
        """
        发送当前的游戏状态给所有连接的客户端
        """
        game_state = {
            'board': self.board,
            'revealed': self.revealed,
            'flags': self.flags,
            'game_over': self.game_over,
            'game_victory': self.game_victory
        }
        emit('game_state', game_state, broadcast=True)

    def openwhite(self):
        """
        空白开片逻辑，自动揭示周围的非雷格子
        """
        for row_ in range(self.BOARD_SIZE):
            for col_ in range(self.BOARD_SIZE):
                if self.board[row_][col_] == 0:
                    for r in range(row_ - 1, row_ + 2):
                        for c in range(col_ - 1, col_ + 2):
                            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                                self.revealed[r][c] = True

    def gameVt(self):
        """
        检测游戏是否胜利
        """
        self.game_victory = True
        for row_ in range(self.BOARD_SIZE):
            for col_ in range(self.BOARD_SIZE):
                if self.board[row_][col_] >= 0 and not self.revealed[row_][col_]:
                    self.game_victory = False
                    break
        if self.game_victory:
            self.send()

    def on_reveal_cell(self, data):
        """
        处理前端揭示格子的请求
        """
        row, col = data['row'], data['col']
        if self.revealed[row][col]:
            return  # 已经揭示过的格子，不再处理

        if not self.game_started:
            self.game_started = True  # 游戏开始
            while True:
                self.board = self.generate_mines(self.board, self.MINES, row, col)  # 在第一次点击时生成地雷
                if self.board[row][col] != -1:  # 如果点击的格子不是地雷，则生成地雷
                    break

            # 填充数字
            for row_ in range(self.BOARD_SIZE):
                for col_ in range(self.BOARD_SIZE):
                    if self.board[row_][col_] == -1:
                        continue
                    for r in range(row_ - 1, row_ + 2):
                        for c in range(col_ - 1, col_ + 2):
                            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == -1:
                                self.board[row_][col_] += 1

        if self.board[row][col] == -1:  # 踩到地雷
            self.revealed[row][col] = True
            game_over = True
            self.send()
            return

        self.revealed[row][col] = True

        # 开片逻辑
        self.openwhite()

        # 检测胜利
        self.gameVt()

        # 更新状态
        self.send()

    def on_reveal_all_cell(self, data):
        """
        处理前端快速揭示的请求
        """
        row, col = data['row'], data['col']

        if not self.revealed[row][col]:
            return

        flag_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                    if self.flags[r][c]:
                        flag_count += 1

        if flag_count == self.board[row][col]:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                        if not self.revealed[r][c] and not self.flags[r][c]:
                            self.revealed[r][c] = True
                            if self.board[r][c] == -1:
                                self.game_over = True
                                return
                            if self.board[r][c] == 0:
                                self.on_reveal_all_cell({'row': r, 'col': c})

        self.gameVt()
        self.send()

    def on_flag_cell(self, data):
        """
        处理前端标记旗帜的请求
        """
        row, col = data['row'], data['col']
        self.flags[row][col] = not self.flags[row][col]
        self.send()

# 注册命名空间
socketio.on_namespace(GameNamespace('/game扫雷'))

if __name__ == '__main__':
    socketio.run(app扫雷, host='0.0.0.0', port=5001, debug=True, use_reloader=False)