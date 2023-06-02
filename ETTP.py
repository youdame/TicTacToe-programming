'''
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        # Receive message using socket
        msg = self.socket.recv(1024).decode()

        # Check if the received message is valid ETTTP format
        msg_valid_check = check_msg(msg, self.peer_ip)

        if not msg_valid_check:  # Message is not valid
            self.socket.close()
            self.quit()
            return
        else:  # If message is valid - send ACK, update board, and change turn
            # Send ACK message to the peer
            ack_msg = "ACK ETTTP/1.0\r\nHost:{}\r\n\r\n".format(self.peer_ip)
            self.socket.send(ack_msg.encode())

            # Extract the move from the received message
            move_line = [line for line in msg.split("\r\n") if line.startswith("New-Move:")]
            if not move_line:
                print("Invalid message format: Move information is missing")
                self.socket.close()
                self.quit()
                return

            move_str = move_line[0].split(":")[1].strip()
            try:
                loc = int(move_str)
            except ValueError:
                print("Invalid message format: Invalid move information")
                self.socket.close()
                self.quit()
                return

            ######################################################

            # Update board with the received move
            self.update_board(self.computer, loc, get=True)

            if self.state == self.active:
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']


    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0, "end")
            return

        # Get message from the input box
        d_msg = self.t_debug.get(1.0, "end")
        d_msg = d_msg.replace("\\r\\n", "\r\n")   # Sanitize the message as \r\n may be modified when given as input
        self.t_debug.delete(1.0, "end")

        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''

        # Check if the selected location is already taken
        if self.board[loc] != " ":
            print("Invalid move: Location already taken")
            return

        '''
        Send message to peer
        '''

        # Create the ETTTP request message
        message = f"SEND ETTTP/1.0\r\nHost: {self.peer_ip}\r\nMessage: {d_msg}\r\n\r\n"

        # Send the message to the peer using TCP socket
        try:
            self.socket.sendall(message.encode())
            # Wait for acknowledgement from the peer
            ack = self.socket.recv(1024).decode()

            # Process the acknowledgement message

            # Check if the acknowledgement is valid
            if ack.startswith("ACK ETTTP/1.0"):
                print("Message sent successfully")
            else:
                print("Error sending message to peer")
                return
        except socket.error as e:
            print(f"Error sending message to peer: {e}")
            return

        '''
        Get ack
        '''

        loc = 5  # Peer's move, from 0 to 8

        ######################################################

        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)

        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move, ())

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
        
    def send_move(self, selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row, col = divmod(selection, 3)
        
        # Create the ETTTP request message
        message = f"SEND ETTTP/1.0\r\nHost: {self.peer_ip}\r\nNew-Move: ({row},{col})\r\n\r\n"
        
        # Send the message to the peer using TCP socket
        try:
            self.socket.sendall(message.encode())
            # Wait for acknowledgement from the peer
            ack = self.socket.recv(1024).decode()
            
            # Process the acknowledgement message
            
            # Check if the acknowledgement is valid
            if ack.startswith("ACK ETTTP/1.0"):
                return True
            else:
                return False
        except socket.error as e:
            print(f"Error sending move to peer: {e}")
            return False
        
    def check_result(self, winner, get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and needs to report the result first
        '''
        ###################  Fill Out  #######################
        if get:
            # This user is the winner and needs to report the result
            result_msg = "RESULT ETTTP/1.0\r\nHost:{}\r\nWinner: ME\r\n\r\n".format(self.peer_ip)
        else:
            # This user is not the winner and waits for the result from the peer
            result_msg = "RESULT ETTTP/1.0\r\nHost:{}\r\nWinner: {}\r\n\r\n".format(self.peer_ip, winner)

        # Send the result message to the peer
        self.socket.send(result_msg.encode())

        # Receive the result message from the peer
        received_msg = self.socket.recv(1024).decode()

        # Check if the received message is the same as the sent message
        if received_msg == result_msg:
            return True
        else:
            return False
        ######################################################

            
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

    def check_msg(msg, recv_ip):
        '''
        Function that checks if received message is ETTTP format
        '''

        # Split the message into lines
        lines = msg.split("\r\n")

        # Check if the first line starts with "ETTTP"
        if not lines[0].startswith("ETTTP"):
            print("Invalid message format: First line does not start with 'ETTTP'")
            return False

        # Check if the host IP is specified in the message
        host_line = [line for line in lines if line.startswith("Host:")]
        if not host_line:
            print("Invalid message format: Host IP is missing")
            return False

        # Extract the host IP from the host line
        host_ip = host_line[0].split(":")[1].strip()

        # Check if the host IP matches the expected receiver IP
        if host_ip != recv_ip:
            print("Invalid message format: Host IP does not match the expected receiver IP")
            return False

        return True