import socket
import random
from tkinter import *

if __name__ == "__main__":
    # 설정
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'

    while True:
        client_socket, client_addr = server_socket.accept()
        start = random.randrange(0, 2)

        # 무작위로 시작할 사람을 선택하여 상대에게 시작 정보를 보냄
        # 구현해야 함
        client_socket.send(str(start).encode())  # 시작 정보를 클라이언트에게 전송

        # ACK를 받음 - ACK가 올바르면 게임 시작
        # 구현해야 함
        ack = client_socket.recv(SIZE).decode()  # 클라이언트로부터 ACK를 수신
        if ack == 'ACK':
            print("게임 시작")
        else:
            print("ACK 수신 실패")

        # 게임 시작
        root = TTT(client=False, target_socket=client_socket, src_addr=MY_IP, dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()

        client_socket.close()
        break

    server_socket.close()