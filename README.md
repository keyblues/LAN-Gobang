# LAN-Gobang

五子棋局域网对战游戏，使用python编写。

## 效果

![这是图片](./data/server.png "Magic Gardens")

## 下载方式

可执行文件：
https://github.com/liujiakang199/pybackgammon/releases

源代码可直接clone使用，体积更小

## 游玩方法

源代码版本使用前需要安装相应的包

```pip install -r package.txt```

client端开启前，需要更改config/config.json文件

```  
"client": {
    "ip": "server端ip",
    "port": 8888
  }
 ```

**注意**：必须先打开server端等待连接才能打开client端，出现棋盘即为连接成功

不正确的退出会导致端口占用，更改两端的config.json文件端口即可

本游戏可跨平台对战，例如linux端可和windows端对战

## 博客

**https://www.keyblue.cn**
