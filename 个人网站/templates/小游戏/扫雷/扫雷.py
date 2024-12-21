from flask import Flask, render_template, request
from flask_cors import CORS
import random
from flask_socketio import SocketIO, Namespace, emit , join_room, leave_room
import time

app扫雷 = Flask(__name__)
socketio = SocketIO(app扫雷, cors_allowed_origins="*")  # 允许所有来源访问

class GameNamespace(Namespace):
##################################################################################
    # 游戏命名空间类，负责扫雷游戏逻辑的处理

    def __init__(self, namespace=None):
        super().__init__(namespace)
        # 匹配队列，存储等待匹配的玩家
        self.waiting_players = []
        # 全局字典
        self.player_data = {}  # 玩家数据
        self.rooms_data = {}  # 房间数据，存储每个房间内玩家的状态

##################################################################################
    # 匹配——房间分配——连接/断开事件

    # 添加新玩家
    def add_player(self , user_id , user_name , user_avatar):
        """
        添加一个新的玩家数据，使用 request.sid 作为键
        """
        self.player_data[request.sid] = {
            'user_id': user_id,  # 账号
            'user_name': user_name,  # 用户名
            'user_avatar': user_avatar,  # 头像
            'board_size': 10,  # 棋盘大小
            'mines': 10,  # 地雷数量
            'game_started': False,  # 游戏是否已经开始
            'game_over': False,  # 游戏是否失败
            'game_victory': False,  # 游戏是否胜利
            'board': [[0 for _ in range(10)] for _ in range(10)],  # 初始化棋盘，全部为 0
            'revealed': [[False for _ in range(10)] for _ in range(10)],  # 初始化揭示状态
            'flags': [[False for _ in range(10)] for _ in range(10)],  # 初始化旗帜状态
        }

    # 监听前台连接事件
    def on_connect(self):
        """监听玩家连接事件"""
        print(f"++++++++ {request.sid} 已连接")


    # 监听匹配请求
    def on_start_match(self , data):
        """
        监听玩家发起匹配请求，
        如果有两个玩家匹配成功，就将他们分配到同一个房间，
        并通知前台进行倒计时。
        """

        user_id,user_name,user_avatar=data['user_id'],data['user_name'],data['user_avatar']
        self.add_player(user_id,user_name,user_avatar)
        print(f"玩家 {request.sid} 开始匹配，数据: {self.player_data.get(request.sid)}")

        # 向当前玩家发送匹配中的提示
        emit('match_status', to=request.sid)

        # 将玩家数据加入等待队列
        # 检查 sid 是否已经存在于 waiting_players 中
        if not any(player['sid'] == request.sid for player in self.waiting_players):
            self.waiting_players.append({'sid': request.sid, 'data': self.player_data.get(request.sid)})
        else:
            print(request.sid,'重复加入')

        # 检查队列中是否有两名玩家可以进行匹配
        if len(self.waiting_players) >= 2:
            # 取出队列中的前两名玩家
            player1 = self.waiting_players.pop(0)
            player2 = self.waiting_players.pop(0)

            # 使用两个玩家的 sid 合并来生成房间ID
            room_id = f"{player1['sid']}_{player2['sid']}"

            # 将两名玩家加入同一个房间
            join_room(room_id, sid=player1['sid'])
            join_room(room_id, sid=player2['sid'])

            # 将玩家数据保存到字典中
            self.player_data[player1['sid']] = player1['data']
            self.player_data[player2['sid']] = player2['data']

            # 保存房间数据
            self.rooms_data[room_id] = {
                player1['sid'],player2['sid']
            }

            print(f"房间 {self.rooms_data}")

            # 通知玩家匹配成功，开始 3 秒倒计时
            for i in range(3, 0, -1):
                emit('match_success', {'status': f'匹配成功，{i} 秒后开始游戏'}, room=room_id)
                time.sleep(1)  # 模拟倒计时

            # 倒计时结束，发送匹配完成消息
            print(f"房间 {room_id} 倒计时结束，开始游戏！")
            self.send()


    # 监听断开连接事件
    def on_disconnect(self):
        """
        监听玩家断开连接事件，
        如果玩家在房间中，则从房间中移除并删除字典中的玩家数据，
        同时从匹配队列中删除该玩家。
        """
        player_sid = request.sid
        print(f"玩家 {player_sid} 已断开连接")

        # 从匹配队列中删除该玩家
        self.waiting_players = [player for player in self.waiting_players if player['sid'] != player_sid]

        # 检查玩家是否在任何房间中
        for room_id, room_data in list(self.rooms_data.items()):
            if player_sid in room_data:
                # 如果玩家是房间中的玩家，移除该玩家并删除房间数据
                leave_room(room_id, sid=player_sid)
                self.rooms_data[room_id].remove(player_sid)
                print(f"玩家 {player_sid} 从房间 {room_id} 中被移除")

                # 如果房间没有玩家了，删除该房间
                if not room_data:
                    del self.rooms_data[room_id]
                    print(f"房间 {self.rooms_data}")
                break

        # 从玩家数据字典中删除该玩家的数据
        if player_sid in self.player_data:
            del self.player_data[player_sid]
            print(f"玩家 {player_sid} 数据已删除")


##################################################################
#游戏逻辑处理


    def is_board_valid(self):
        """
        检查棋盘是否有效（无封闭环路）
        """
        board = self.player_data[request.sid]['board']
        board_size = self.player_data[request.sid]['board_size']

        for row in range(board_size):
            for col in range(board_size):
                if board[row][col] != -1:  # 找到一个空白区域作为开始点
                    start_row, start_col = row, col
                    break
        revealed_copy = [[False] * board_size for _ in range(board_size)]
        self.dfs(request, start_row, start_col)

        # 如果所有非雷位置都已展开，则棋盘有效
        for row in range(board_size):
            for col in range(board_size):
                if board[row][col] != -1 and not revealed_copy[row][col]:
                    return False
        return True

    def dfs(self, row, col):
        """
        深度优先搜索，用于模拟展开空白区域
        """
        board = self.player_data[request.sid]['board']
        revealed = [[False] * self.player_data[request.sid]['board_size'] for _ in range(self.player_data[request.sid]['board_size'])]

        if revealed[row][col]:
            return
        revealed[row][col] = True
        if board[row][col] == 0:  # 如果是空白区域，继续展开
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.player_data[request.sid]['board_size'] and 0 <= c < self.player_data[request.sid]['board_size']:
                        self.dfs(request, r, c)

    def generate_mines(self, num_mines, first_click_row, first_click_col):
        """
        生成地雷，确保第一次点击的格子不是地雷且不会形成封闭环路
        """
        board = self.player_data[request.sid]['board']
        board_size = self.player_data[request.sid]['board_size']
        mines_placed = 0
        mines = set()

        while mines_placed < num_mines:
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - 1)

            # 如果该位置已有地雷，或是第一次点击的格子，跳过
            if (row, col) in mines or (row == first_click_row and col == first_click_col):
                continue

            # 暂时放置一个地雷
            board[row][col] = -1
            mines.add((row, col))

            # 检查是否会形成封闭环路
            if self.is_board_valid(request):
                mines_placed += 1
            else:
                # 如果形成封闭环路，撤销该地雷
                board[row][col] = 0
                mines.remove((row, col))

        return board

    def send(self, request):
        """
        直接发送玩家字典给当前连接的玩家
        """
        emit('match_status', self.player_data[request.sid], to=request.sid)  # 直接发送玩家字典

    def openwhite(self):
        """
        空白开片逻辑，自动揭示周围的非雷格子
        """
        board = self.player_data[request.sid]['board']
        revealed = self.player_data[request.sid]['revealed']
        board_size = self.player_data[request.sid]['board_size']

        for row_ in range(board_size):
            for col_ in range(board_size):
                if board[row_][col_] == 0:
                    for r in range(row_ - 1, row_ + 2):
                        for c in range(col_ - 1, col_ + 2):
                            if 0 <= r < board_size and 0 <= c < board_size:
                                revealed[r][c] = True

    def gameVt(self, request):
        """
        检测游戏是否胜利
        """
        board = self.player_data[request.sid]['board']
        revealed = self.player_data[request.sid]['revealed']
        board_size = self.player_data[request.sid]['board_size']

        self.player_data[request.sid]['game_victory'] = True
        for row_ in range(board_size):
            for col_ in range(board_size):
                if board[row_][col_] >= 0 and not revealed[row_][col_]:
                    self.player_data[request.sid]['game_victory'] = False
                    break
        if self.player_data[request.sid]['game_victory']:
            self.send(request)

    def on_reveal_cell(self, request, data):
        """
        处理前端揭示格子的请求
        """
        row, col = data['row'], data['col']
        revealed = self.player_data[request.sid]['revealed']
        board = self.player_data[request.sid]['board']

        if revealed[row][col]:
            return  # 已经揭示过的格子，不再处理

        if not self.player_data[request.sid]['game_started']:
            self.player_data[request.sid]['game_started'] = True  # 游戏开始
            while True:
                board = self.generate_mines(request, self.player_data[request.sid]['mines'], row, col)  # 在第一次点击时生成地雷
                if board[row][col] != -1:  # 如果点击的格子不是地雷，则生成地雷
                    break

            # 填充数字
            for row_ in range(self.player_data[request.sid]['board_size']):
                for col_ in range(self.player_data[request.sid]['board_size']):
                    if board[row_][col_] == -1:
                        continue
                    for r in range(row_ - 1, row_ + 2):
                        for c in range(col_ - 1, col_ + 2):
                            if 0 <= r < self.player_data[request.sid]['board_size'] and 0 <= c < self.player_data[request.sid]['board_size'] and board[r][c] == -1:
                                board[row_][col_] += 1

        if board[row][col] == -1:  # 踩到地雷
            revealed[row][col] = True
            self.player_data[request.sid]['game_over'] = True
            self.send(request)
            return

        revealed[row][col] = True

        # 开片逻辑
        self.openwhite(request)

        # 检测胜利
        self.gameVt(request)

        # 更新状态
        self.send(request)

    def on_reveal_all_cell(self, request, data):
        """
        处理前端快速揭示的请求
        """
        row, col = data['row'], data['col']
        revealed = self.player_data[request.sid]['revealed']
        board = self.player_data[request.sid]['board']
        flags = self.player_data[request.sid]['flags']

        if not revealed[row][col]:
            return

        flag_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.player_data[request.sid]['board_size'] and 0 <= c < self.player_data[request.sid]['board_size']:
                    if flags[r][c]:
                        flag_count += 1

        if flag_count == board[row][col]:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.player_data[request.sid]['board_size'] and 0 <= c < self.player_data[request.sid]['board_size']:
                        if not revealed[r][c] and not flags[r][c]:
                            revealed[r][c] = True
                            if board[r][c] == -1:
                                self.player_data[request.sid]['game_over'] = True
                                return
                            if board[r][c] == 0:
                                self.on_reveal_all_cell(request, {'row': r, 'col': c})

        self.gameVt(request)
        self.send(request)

    def on_flag_cell(self, request, data):
        """
        处理前端标记旗帜的请求
        """
        row, col = data['row'], data['col']
        self.player_data[request.sid]['flags'][row][col] = not self.player_data[request.sid]['flags'][row][col]
        self.send(request)


# 注册命名空间
socketio.on_namespace(GameNamespace('/game扫雷'))

if __name__ == '__main__':
    socketio.run(app扫雷, host='0.0.0.0', port=5001, debug=True, use_reloader=False)