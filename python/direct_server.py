# -*- coding:utf-8 -*-
import socket
import threading
import select
import sys

from direct_client import SocketClient


def process(request, client_address):
    print request,client_address
    conn = request
    # conn.sendall('欢迎致电 10086，请输入1xxx,0转人工服务.')
    flag = True
    socketClient = SocketClient()
    while flag:
        data = conn.recv(4096)
        retmsg = socketClient.conn_tac(data)
        conn.sendall(retmsg)
        
# print '端口:', str(sys.argv[1])
print 'start'
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

address = ('',20018)
sk.bind(address)
sk.listen(5)


while True:
    r, w, e = select.select([sk,],[],[],1)
    # print 'looping'
    if sk in r:
        print 'get request'
        request, client_address = sk.accept()
        t = threading.Thread(target=process, args=(request, client_address))
        t.daemon = False
        t.start()

sk.close()