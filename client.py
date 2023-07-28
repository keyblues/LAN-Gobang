import json
import os
import sys
import threading
import tkinter

import pygame.freetype

from data import game, network

config = dict(json.load(open('config/config.json', 'r')))
print(config)

pygame.init()
game_socket = network.GameSocket()
game_state = 0  # 游戏状态 0 - 游戏中  1 - 执黑子赢  2 - 执白子赢
game_client = False
game_server = False
game_receive_state = False
game_server_bind_state = False


def connect_windows():
    root = tkinter.Tk()
    root.title('输入IP')
    root.resizable(width=False, height=False)
    entry_ip = tkinter.Entry(root, font=('Arial', 14))
    entry_ip.pack()
    tkinter.Button(root, width=10, height=1, text='连接', font=('Arial', 14),
                   command=lambda: connect_ip(root, entry_ip.get())).pack()
    entry_ip.focus_set()
    root.mainloop()


def connect_ip(root, entry_ip):
    global game_client, game_socket, screen
    game_ip = entry_ip
    game_socket.connect(game_ip, 5555)
    # 连接成功后关闭主窗口
    screen = pygame.display.set_mode((900, 670))
    game_client = True
    root.destroy()


def game_receive():
    global game_receive_state, game_state
    recv_data = game_socket.receive()
    game.add_ops([[recv_data['x'], recv_data['y']], recv_data['color']])
    game_state = recv_data['game']
    # 接收到数据，将接收状态改为False
    game_receive_state = False
    return recv_data


def game_server_bind():
    global game_server_bind_state, game_receive_state
    game_socket.bind("0.0.0.0", 5555)
    # 当连接成功时，设置game_server_bind_state参数为True
    game_server_bind_state = True
    game_receive_state = True
    game_receive_threading = threading.Thread(target=game_receive)
    game_receive_threading.setDaemon(True)
    game_receive_threading.start()
    return True


# 首页
window_size = window_x, window_y = 800, 480
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('五子棋 LAN-Gobang v2.0')

# 系统路径
dir_path = os.path.split(os.path.realpath(__file__))[0]

# 设置字体
font = pygame.font.Font(dir_path + '/data/yahei.ttf', 30)

# 加载首页图片
bg = pygame.image.load(dir_path + '/data/Gobang800x480.png')

# 显示字
text = font.render("F1-连接  F2-等待连接", True, (255, 255, 255))
text_reset = font.render("F3-重置", True, (255, 255, 255))
text_bind = font.render("等待连接···", True, (255, 255, 255))
text_now = font.render("轮到你了", True, (255, 255, 255))
text_wait = font.render("对手正在思考··", True, (255, 255, 255))
text_white = font.render("你执白子", True, (255, 255, 255))
text_black = font.render("你执黑子", True, (255, 255, 255))
text_white_win = font.render("执白子胜！", True, (255, 255, 255))
text_black_win = font.render("执黑子胜！", True, (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(event)
            # 按下了f1
            if event.key == 1073741882:
                game_client = False
                connect_windows()

            # 按下了f2
            if event.key == 1073741883:
                game_server = True
                # 未连接时，启动线程等待连接
                if not game_server_bind_state:
                    game_server_bind_threading = threading.Thread(target=game_server_bind)
                    game_server_bind_threading.setDaemon(True)
                    game_server_bind_threading.start()
                    screen = pygame.display.set_mode((900, 670))

    screen.blit(bg, (0, 0))
    screen.blit(text, (475, 395))

    while game_client:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 按下了f3
                if event.key == 1073741884:
                    game_state = 0  # 游戏状态 0 - 游戏中  1 - 执黑子赢  2 - 执白子赢
                    game_client = False
                    game_server = False
                    game_receive_state = False
                    game_server_bind_state = False
                    # 断开连接
                    game_socket.disconnect()
                    # 重置游戏
                    game.restart()
                    # 重置窗口
                    screen = pygame.display.set_mode(window_size)
                    game_socket = network.GameSocket()

        game.fix()
        screen.blit(text_reset, (710, 30))
        screen.blit(text_black, (710, 600))
        x, y, color = game.position_state()

        if not game_state:
            # 当game_state为0时,可以落子
            if color and not game_receive_state:
                # 当color为True，game_receive_state为Fleas时可以落子
                screen.blit(text_now, (700, 400))
                game.add_ops([[x, y], color])
                if game.win():
                    # 判断五子连心
                    game_state = 1
                game_socket.fall(x, y, color, game_state)
                print(game.get_over())
                game_receive_state = True

                if game_receive_state:
                    # 当game_receive_state为True时启动数据接收线程
                    game_receive_threading = threading.Thread(target=game_receive)
                    game_receive_threading.setDaemon(True)
                    game_receive_threading.start()
            if game_receive_state:
                screen.blit(text_wait, (690, 400))
            elif not game_receive_state and game_client:
                screen.blit(text_now, (700, 400))

        if game_state == 1:
            # 执黑子赢得游戏
            screen.blit(text_black_win, (690, 300))
        if game_state == 2:
            # 执白子赢得游戏
            screen.blit(text_white_win, (690, 300))

        pygame.display.flip()

    while game_server:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 按下了f3
                if event.key == 1073741884:
                    game_state = 0  # 游戏状态 0 - 游戏中  1 - 执黑子赢  2 - 执白子赢
                    game_client = False
                    game_server = False
                    game_receive_state = False
                    game_server_bind_state = False
                    # 断开连接
                    game_socket.disconnect()
                    # 重置游戏
                    game.restart()
                    # 重置窗口
                    screen = pygame.display.set_mode(window_size)
                    game_socket = network.GameSocket()

        game.fix()
        screen.blit(text_reset, (710, 30))
        screen.blit(text_white, (710, 600))
        x, y, color = game.position_state()
        if not game_server_bind_state:
            screen.blit(text_bind, (700, 200))

        if not game_state:
            # 当game_state为0时,可以落子
            if color and not game_receive_state:
                # 当color为True，game_receive_state为Fleas时可以落子
                screen.blit(text_now, (700, 400))
                game.add_ops([[x, y], color])
                if game.win():
                    # 判断五子连心
                    game_state = 2
                game_socket.fall(x, y, color, game_state)
                print(game.get_over())
                game_receive_state = True

                if game_receive_state:
                    # 当game_receive_state为True时启动数据接收线程
                    game_receive_threading = threading.Thread(target=game_receive)
                    game_receive_threading.setDaemon(True)
                    game_receive_threading.start()
            if game_receive_state:
                screen.blit(text_wait, (690, 400))
            elif not game_receive_state and game_server_bind_state:
                screen.blit(text_now, (700, 400))

        if game_state == 1:
            # 执黑子赢得游戏
            screen.blit(text_black_win, (690, 300))
        if game_state == 2:
            # 执白子赢得游戏
            screen.blit(text_white_win, (690, 300))

        pygame.display.flip()

    pygame.display.flip()
