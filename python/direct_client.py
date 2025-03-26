import socket
import struct

# HOST = '10.200.4.183'
HOST = '192.168.233.129'
PORT = 20018


def conn_one():
    s = socket.socket()
    s.connect((HOST, PORT))
    while True:
        msg = input('>>:').strip()
        s.send(msg.encode('utf-8'))
        # s.send(('hello ').encode('utf-8'))
        data = s.recv(1024)
        print('recved:', data.decode())
    s.close()


def conn_one_with_file_open():
    s = socket.socket()
    s.connect((HOST, PORT))

    fo = open("D:/16_workspace/eps/messagedata.out", "rb")
    str = fo.read(4)
    print ( str)
    s.send(str)
    str = fo.read(int(str))
    print( str)
    # msg = input('>>:').strip()
    s.send(str)
    # # s.send(('hello ').encode('utf-8'))
    data = s.recv(1024)
    print('recved:', data)

    s.close()
class SocketClient:
    def __init__(self):
        self.s = socket.socket()
        self.s.connect((HOST, PORT))

    def conn_tac(self,msg):
        # s = socket.socket()
        # s.connect((HOST, PORT))

        # str = "58020105010111002193724856CF84CE0300000000000000000000056AA930000000000210057252420190831221332"
        #str = "58020105200008170000000101B32013030000000000000000000000011051122334455660000000120080105163100"
        # print ( str.encode())
        # _len = len(msg)
        # b = _len.to_bytes(2, 'little', signed=True)
        # b = bytes([0, 95])
        # b = b'95'
        # b = struct.pack(">H", _len)
        # print(b)
        # print( int.from_bytes(b,'little'))
        # self.s.send(b)
        self.s.send(msg.encode())

        data = self.s.recv(4096)
        # print ('recved:', data)

        self.s.close()
        
        return data

        # s.close()



