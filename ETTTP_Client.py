'''
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg
    
if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
        recv_header = client_socket.recv(SIZE).decode()

         # Check if the message is valid
        if not check_msg(recv_header, SERVER_IP):
            client_socket.close()
        
        # 1차적으로 : send 뒤에 문자열을 변수로 가져오고 (ack 그대로 보내는 것 용도)
        split_message = recv_header.split("SEND ")[1]

        # 2차적으로 : 첫 번째에서 만든 변수에서 YOU나 ME를 파싱해서 start 변수에 넣어주기

        # 주어진 메시지를 줄바꿈 문자('\r\n')을 기준으로 분할
        lines = split_message.split("\r\n")

        # 분할된 결과에서 'First-Move:'를 찾아 값을 추출
        for line in lines:
            if line.startswith('First-Move:'):
                value = line.split(':')[1].strip()
                break
            
        if value == "YOU":
            start = 1
            ack_message = f"ETTTP/1.0\r\nHost:{SERVER_IP}\r\nFirst-Move:ME\r\n\r\n"
        elif value == "ME":
            start = 0
            ack_message = f"ETTTP/1.0\r\nHost:{SERVER_IP}\r\nFirst-Move:YOU\r\n\r\n"
    
        
        # Send ACK 
        # ACK 문자열 뒤에 한칸 띄어쓰기하고 첫 번쨰 변수 그대로 보내기
        
        
        send_header = "ACK "+ ack_message
        client_socket.send(send_header.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        
        