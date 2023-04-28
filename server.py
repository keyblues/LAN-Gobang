import json
import os
import socket
import sys
import threading
import time

import pygame.freetype

from data import game


def game_conn():
    global sock, code, screen
    code = 0
    sock, addr = s.accept()
    print(sock, addr)
    code = 1
    conn_code()


def conn_code():
    global sock, x, y, color, black, win, lose
    while True:
        time.sleep(0.05)
        if game.win():
            time.sleep(9999)
        if color:
            game.add_ops([[x, y], color])
            if game.win():
                win = True
            data = {
                "x": x,
                "y": y,
                "color": color,
                "game": win
            }
            text = str(data)
            print('发送：', text)
            sock.send(text.encode())
            black = True
            if game.win():
                win = True
        if black:
            over = sock.recv(2048).decode()
            s = eval(over)
            if s['game']:
                print('lose')
                lose = True
            print('接收：', s)
            game.add_ops([[s['x'], s['y']], s['color']])
            black = False


config = dict(json.load(open('config/config.json', 'r')))
print(config)
s = socket.socket()
# 绑定端口
s.bind((config['server']['ip'], config['server']['port']))
s.listen(5)
pygame.init()
over = []
black = False
win = False  # 游戏状态
lose = False
# 开启一个子线程，等待连接
t = threading.Thread(target=game_conn)
t.setDaemon(True)
t.start()
screen = pygame.display.set_mode((670, 670))
pygame.display.set_caption('五子棋---服务端')
dir_path = os.path.split(os.path.realpath(__file__))[0]
f1 = pygame.freetype.Font(dir_path + '/data/yahei.ttf', 30)
f1.render_to(screen, [250, 300], "等待连接中……", fgcolor=(255, 251, 0), bgcolor=(0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if code:
        game.de1()
        x, y, color = game.de2()
        if game.win():
            win = True
            if lose:
                f1.render_to(screen, [250, 300], "你输了！", fgcolor=(255, 251, 0), bgcolor=(0, 0, 0))
                pygame.display.update()
                time.sleep(1)
            else:
                f1.render_to(screen, [250, 300], "你赢了！", fgcolor=(255, 251, 0), bgcolor=(0, 0, 0))
                pygame.display.update()
                time.sleep(1)
    pygame.display.update()
