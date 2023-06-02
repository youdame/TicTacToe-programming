'''
  ETTTP_Sever_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe_skeleton import TTT, check_msg

    
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
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        start_msg = "SEND ETTTP/1.0\r\nHost: 127.0.0.1\r\nFirst-Move:"
        if start == 0:
            start_msg += "ME\r\n\r\n"
        else:
            start_msg += "YOU\r\n\r\n"
        client_socket.send(start_msg.encode())
    
        ###################################################################
        
        # Receive ack - if ack is correct, start game
        ack_msg = "ACK ETTTP/1.0\r\nHost: 127.0.0.1\r\nFirst-Move:"
        if start == 0:
            ack_msg += "YOU\r\n\r\n"
        else:
            ack_msg += "ME\r\n\r\n"
        ack = client_socket.recv(SIZE).decode()
        if ack == ack_msg:
            print("Game started.")
        else:
            print("Error in receiving ack. Exiting...")
            break
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()
