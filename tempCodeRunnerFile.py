
if __name__ == '__main__':
    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)
    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)
        

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
        root = TTT(target_socket=client_socket, src_addr=MY_IP, dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()

