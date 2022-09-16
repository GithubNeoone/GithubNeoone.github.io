import socket
import threading
import os
import json
import time

PORT = 11451
SERVER_ADDR = input('服务器地址：')

while 1:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER_ADDR, PORT))
        break
    except:
        time.sleep(0.5)
s.send(input('昵称：').encode())

os.chdir(os.path.dirname(__file__))

with open('money.txt') as f:
    money = int(f.read())
yazhu = 0

def process(data):
    global money, yazhu
    data = json.loads(data)
    info = data['data']
    if info == '本局开始！':
        yazhu = 0
    if info.startswith('+'):
        money += int(info)
        return
    if info == 'update':
        with open('money.txt', 'w') as f:
            f.write(str(money))
        return
    if info == 'money':    
        s.send(str(money).encode())
        return
    if info == 'cls':
        os.system('cls')
        return
    with open('money.txt', 'w') as f:
        f.write(str(money))
    if info.count('你是大盲注'):
        money -= 10
        yazhu = 10
    if info.count('[yu e]') > 0:
        info = info.replace('[yu e]', '你的余额: $%d'%money)
    if data['type']=='input':
        xz = False
        if info.count('[xiazhu]'):
            info = info.replace('[xiazhu]', '')
            xz = True
            zhu = info[info.find('当前下注: ')+6:]
            zhu = int(zhu[1:zhu.find(',')])
        while 1:
            while 1:
                a = time.perf_counter()
                x = input(info)
                b = time.perf_counter()
                if b - a > 0.1:
                    break
            if x == 'q':
                s.send(x.encode())
                return
            if x == '':
                x = 'none' if money > zhu else 'a'
            try:
                if x == 'none' or x == 'a' or (int(x) >= zhu and int(x) - yazhu < money):
                    break
            except:
                print('错误')
                continue
            print('下注不能比当前注少，不能比自己的金额多')
        if x == 'a':
            x += str(money)
            money = 0
            yazhu += money
        else:
            money -= (zhu if x == 'none' else int(x)) - yazhu
            yazhu = (zhu if x == 'none' else int(x))
        s.send(x.encode())
        return

    if data['type']=='print':
        print(info)

def receive():
    while True:
        data = s.recv(1024).decode()
        process(data)

receive()