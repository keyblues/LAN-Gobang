import socket


class GameSocket:
    def __init__(self):
        self.Socket = socket.socket()

    def connect(self, ip, port):
        # client
        self.Socket.connect((ip, port))

    def bind(self, ip, port):
        # server
        self.Socket.bind((ip, port))
        self.Socket.listen(5)
        sock, addr = self.Socket.accept()
        self.Socket = sock
        return sock

    def fall(self, coordinate_x, coordinate_y, piece_color, game_state):
        # 初始化落子数据
        data = {
            "x": coordinate_x,
            "y": coordinate_y,
            "color": piece_color,
            "game": game_state
        }
        text = str(data)
        print('发送：', text)
        # 向对手发送落子数据
        self.Socket.send(text.encode())

    def receive(self):
        # 接收对手落子数据
        receive_data = self.Socket.recv(2048).decode()
        # 格式化接收到的数据
        format_data = eval(receive_data)
        return format_data

    def disconnect(self):
        self.Socket.close()
