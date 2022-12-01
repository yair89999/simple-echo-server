##############################################################################
# server.py
##############################################################################

import socket,select,random,requests,json
import chatlib


global messages_to_send
messages_to_send = [] # (client IP+port, message(LOGIN_ok        |0012|aaaa#bbbb))

ERROR_MSG = "Error! "
SERVER_PORT = 5680
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    message = chatlib.build_message(code,msg) # create the message( will look like this: LOGIN_OK        |0012|aaaa#bbbb)
    messages_to_send.append((conn, message))
    print(f"[SERVER] msg to{conn.getpeername()}: ",message)	  # Debug print

def recv_message_and_parse(conn):
    full_msg = conn.recv(1024).decode() # gets the message from the server   need to be something like this for example "LOGIN           |0009|aaaa#bbbb"
    if full_msg == "":
        return None, None
    cmd, data = chatlib.parse_message(full_msg) # split it to a tuple with the command and the data
    print(f"[CLIENT] {conn.getpeername()} msg: ",full_msg)  # Debug print
    return cmd, data

def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket,   socket.AF_INET = IP protocol,   socket.SOCK_STREAM = protocol TCP
    sock.bind((SERVER_IP,SERVER_PORT)) # 
    sock.listen() # listen to sockets
    return sock
	


		
def send_error(conn, error_msg):
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], error_msg)
	

room1 = [] # (conn,name)
room1_user_turn = 1
room2 = [] # (conn,name)
room2_user_turn = 2

rooms = {} # "room num" : [(socket,username),(socket,username)]
rooms_users_turn = {}

def get_user_in_room(conn,cmd,data):
    pass
def handle_client_message(conn, cmd, data):
    build_and_send_message(conn,cmd,data)


def main():
    global messages_to_send,room1,room2
	
    print("Chat room server is up and running")
	
    server_socket = setup_socket()
    client_sockets = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [],[])
        for current_socket in ready_to_read: # a loop that go over all of the sockets you can read from
            if current_socket is server_socket: # if the current socket is the server socket(if a new client arrived)
                (client_socket, client_address) = current_socket.accept() # get the client socket and the client IP/create a conaction with the client
                print("New client joined!",client_address)
                client_sockets.append(client_socket) # append to the sockets list new client socket
                
            else: # if the server got new message
                #print("New data from client")
                try:
                    cmd,data = recv_message_and_parse(current_socket) # gets the command+data
                    if cmd == None or cmd == "" and data == "": # closes the socket
                        client_sockets.remove(current_socket)
                        current_socket.close()
                        print(current_socket.getpeername(),"disconnect, socket closed")
                    handle_client_message(current_socket, cmd,data)
                except Exception as e: # if it got error (will be ConnectionResetError if the client closed the cmd window)
                    #print("Error user closed cmd window\n",e)
                    try: # trying to logout
                        # doing it because if the client just close the window it wont do the logout
                        client_sockets.remove(current_socket)
                        current_socket.close()
                        print(current_socket.getpeername(),"disconnect, socket closed")
                    except: # gives an error if the socket is already closed
                        pass
                    
        for message1 in messages_to_send:
            socket1 = message1[0]
            message = message1[1]
            try:
                socket1.send(message.encode())
            except:
                pass
        messages_to_send = []



if __name__ == '__main__':
    main()
    """# code to run this server no matter what(even if it gets errors)
    while True:
        try: # there can be an error in main()
            main()
        except Exception as error:
            print(error)"""