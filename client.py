import socket
from tkinter import *


if __name__ == '__main__':
    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)
    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)
        
        # 서버로부터 먼저 시작할 플레이어를 받음
        start = client_socket.recv(SIZE).decode()  # 서버로부터 시작 정보를 수신
        start = int(start)
        
        # ACK 전송
        ack = 'ACK'
        client_socket.send(ack.encode())  # ACK를 서버에게 전송
        
        # 게임 시작
        root = TTT(target_socket=client_socket, src_addr=MY_IP, dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
