#===============================================================================
#Modules being imported
#===============================================================================

import socket 
import threading
from database.db_manager import DBManager

#===============================================================================
#localhost and port to listen on
#===============================================================================

HOST = '127.0.0.1'
#custom use TCP/UDP port 
PORT = 65432 

#===============================================================================
#function to handle connections to the client
#===============================================================================

def client_handler(client_socket, db_manager):
    while True:
        try:
            msg = client_socket.recv(1024).decode('utf-8') 
            if not msg:
                break
            print(f'Received: {msg}')
            result = db_manager.fetch_all('SELECT * FROM users WHERE username = ?', (msg,))
            client_socket.send(str(result).encode('utf-8'))
        except:
            break
    client_socket.close()

#===============================================================================
#main server functionality 
#===============================================================================

def main():
    db_manager = DBManager('user_db.db')
    db_manager.create_connection()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Server is listening on {HOST}:{PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        client_thread = threading.Thread(target=client_handler, args=(client_socket, db_manager))
        client_thread.start()

if __name__ == 'main':
    main()