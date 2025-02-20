#===============================================================================
#Modules being imported
#===============================================================================

import socket

#===============================================================================
#localhost and port to transmit to
#===============================================================================

HOST = '127.0.0.1'
PORT = 65432

def server_communication():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    try:
        while True:
            msg = input('Enter a username to search: ')
            if msg.lower() == 'exit':
                break
            client_socket.send(msg.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f'Response from server: {response}')
    except:
        print('Connection closed')
    finally:
        client_socket.close()
    
if __name__ == '__main__':
    server_communication()