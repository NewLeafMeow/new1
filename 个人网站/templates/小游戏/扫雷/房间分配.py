class Player:
    """
    玩家类，用于存储每个玩家的状态、信息等
    """
    def __init__(self, player_id):
        """
        初始化玩家类
        :param player_id: 玩家唯一标识符
        """
        self.player_id = player_id  # 玩家ID（在SocketIO中通常是sid）
        self.room_id = None         # 当前玩家所在的房间ID
        self.status = "waiting"     # 玩家状态（waiting: 等待匹配, in_game: 游戏中)
        
        #游戏数据状态
        self.BOARD_SIZE = 10  # 棋盘大小
        self.MINES = 10  # 地雷数量
        self.game_started = False  # 游戏是否已经开始
        self.game_over = False  # 游戏是否失败
        self.game_victory = False  # 游戏是否胜利
        self.board, self.revealed, self.flags = self.generate_board()  # 初始化棋盘、揭示状态和旗帜状态

    def join_room(self, room_id):
        """
        玩家加入房间
        :param room_id: 房间ID
        """
        self.room_id = room_id
        self.status = "in_game"  # 玩家状态改为游戏中
        print(f"Player {self.player_id} joined room {self.room_id}")

    def leave_room(self):
        """
        玩家离开房间
        """
        print(f"Player {self.player_id} left room {self.room_id}")
        self.room_id = None
        self.status = "waiting"  # 玩家状态恢复为等待匹配

    def __repr__(self):
        """
        返回玩家的基本信息
        """
        return f"Player(id={self.player_id}, status={self.status}, room={self.room_id})"


class RoomManager:
    """
    房间管理器类：管理公共房间、匹配功能和玩家映射
    """
    def __init__(self):
        self.rooms = {}  # 存储房间信息，键为 room_id，值为房间内玩家对象列表
        self.waiting_queue = []  # 待匹配玩家队列
        self.player_map = {}  # 全局玩家映射表，键为 player_id，值为 Player 对象
        self.max_players_per_room = 2  # 每个房间的最大玩家数
        self.room_counter = 0  # 用于生成唯一的房间ID

    def add_player(self, player):
        """
        将玩家添加到全局玩家映射表
        :param player: Player对象
        """
        self.player_map[player.player_id] = player
        print(f"Player {player.player_id} added to player map.")

    def get_player(self, player_id):
        """
        通过玩家ID快速获取玩家对象
        :param player_id: 玩家ID
        :return: Player对象或 None
        """
        return self.player_map.get(player_id)

    def remove_player(self, player):
        """
        将玩家从房间中或等待队列中移除，如果房间为空则删除房间
        :param player: 玩家对象
        """
        # 从房间中移除玩家
        for room_id, room_info in list(self.rooms.items()):
            if player in room_info["players"]:
                room_info["players"].remove(player)
                print(f"Player {player.player_id} removed from room {room_id}")
                if not room_info["players"]:
                    del self.rooms[room_id]
                    print(f"Room {room_id} is now empty and deleted.")
                player.leave_room()
                break

        # 从等待队列中移除玩家
        if player in self.waiting_queue:
            self.waiting_queue.remove(player)
            print(f"Player {player.player_id} removed from waiting queue.")

        # 从玩家映射表中删除
        if player.player_id in self.player_map:
            del self.player_map[player.player_id]
            print(f"Player {player.player_id} removed from player map.")

    def match_players(self, player):
        """
        匹配玩家，如果队列中已有一名玩家，则匹配成功并创建房间。
        :param player: 当前玩家对象
        :return: 房间ID（如果匹配成功），或 None（如果等待中）
        """
        if player.player_id in self.player_map:
            print(f"Player {player.player_id} already exists. Skipping re-match.")
            return None
        
        self.add_player(player)  # 添加到玩家映射表

        if self.waiting_queue:
            # 匹配成功：从队列中取出等待的玩家
            matched_player = self.waiting_queue.pop(0)
            room_id = self.create_room([matched_player, player])  # 创建房间
            return room_id
        else:
            # 没有玩家等待，将当前玩家加入匹配队列
            self.waiting_queue.append(player)
            print(f"Player {player.player_id} is waiting for a match.")
            return None

    def create_room(self, players):
        """
        创建一个新的公共房间，并将玩家加入其中
        :param players: 玩家对象列表
        :return: 房间ID
        """
        self.room_counter += 1
        room_id = f"room_{self.room_counter}"
        self.rooms[room_id] = {
            "players": players,
            "status": "full"
        }
        for player in players:
            player.join_room(room_id)
        print(f"Room {room_id} created with players: {', '.join([p.player_id for p in players])}")
        return room_id

    def get_room_by_player(self, player):
        """
        获取玩家所在的房间信息
        :param player: Player对象
        :return: 房间ID 或 None
        """
        return player.room_id
