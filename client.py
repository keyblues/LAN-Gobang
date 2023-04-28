import json
import os
import socket
import sys
import threading
import time

import pygame.freetype

from data import game

config = dict(json.load(open('config/config.json', 'r')))

s1 = socket.socket()
s1.connect((config['client']['ip'], config['client']['port']))
color = False


def conn_code():
    global s1, over, x, y, color, white, lose, win
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
            s1.send(text.encode())
            white = True
            if game.win():
                win = True
        if white:
            over = s1.recv(2048).decode()
            s = eval(over)
            if s['game']:
                print('lose')
                lose = True
            print('接收：', s)
            game.add_ops([[s['x'], s['y']], s['color']])
            white = False


white = True  # 棋子状态
win = False  # 游戏状态
t = threading.Thread(target=conn_code)
t.setDaemon(True)
t.start()
pygame.init()
screen = pygame.display.set_mode((670, 670))
pygame.display.set_caption('五子棋---客户端')
dir_path = os.path.split(os.path.realpath(__file__))[0]
f1 = pygame.freetype.Font(dir_path + '/data/yahei.ttf', 30)
over = []
lose = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
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
