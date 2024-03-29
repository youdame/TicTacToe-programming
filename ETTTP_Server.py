'''
  0이면 서버 1이면 클라이언트 
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
            
        # 클라이언트의 IP 주소 가져오기
        client_ip = client_addr[0]

        start = random.randrange(0, 2)
        
       
        ###################################################################
        # Send start move information to peer
        start_msg = f"SEND ETTTP/1.0\r\nHost:{client_ip}\r\nFirst-Move:"
        
        if start == 0:
            start_msg += "ME\r\n\r\n"
        else:
            start_msg += "YOU\r\n\r\n"
        client_socket.send(start_msg.encode())

        ###################################################################
        
        # Receive ack - if ack is correct, start game
        ack_msg = f"ACK ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:"
        if start == 0:
            ack_msg += "YOU\r\n\r\n"
        else:
            ack_msg += "ME\r\n\r\n"
        ack = client_socket.recv(SIZE).decode()
        if ack == ack_msg:
            # ACK를 올바르게 받은 후에 게임을 시작합니다.
            print("Game started.")
            
            root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
            root.play(start_user=start)
            root.mainloop()
        else:
            print("Error in receiving ack. Exiting...")
            break
        
        client_socket.close()
        
        break
    server_socket.close()
