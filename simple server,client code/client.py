import socket,time
import chatlib  

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5680


def build_and_send_message(conn, code, data): # code = command

	message = chatlib.build_message(code,data) # create the message( will look like this: LOGIN           |0009|aaaa#bbbb)
	conn.send(message.encode()) # send to the server the message in the right format
	

def recv_message_and_parse(conn):
	full_msg = conn.recv(1024).decode() # gets the message from the server   need to be something like this for example "LOGIN           |0009|aaaa#bbbb"
	cmd, data = chatlib.parse_message(full_msg) # split it to a tuple with the command and the data
	return cmd, data
	

def connect():
    """create a socket and connect to it(to receive and send messages)"""
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket,   socket.AF_INET = IP protocol,   socket.SOCK_STREAM = protocol TCP
    my_socket.connect((SERVER_IP,SERVER_PORT)) # connect to the socket(make it able to send messages in the socket)
    return my_socket


def error_and_exit(error_msg):
    print(error_msg)
    time.sleep(10)
    exit()


def build_send_recv_parse(conn,cmd,data):
	"""send the data it received(send the data,cmd(you need to put them when you call the function) with build_and_send_message
	receive data with recv_message_and_parse and returns the data,msg_code that it received"""
	build_and_send_message(conn,cmd,data) # build+send the message to the server
	msg_code,data2 = recv_message_and_parse(conn) # get the message from the server and parse it and put it in 2 variables
	return data2,msg_code


def main():
    using_socket = connect()
    while True:
        message = input("enter your message: ")
        build_and_send_message(using_socket, "MESSAGE", message)
        command,data = recv_message_and_parse(using_socket) # gets the username that it his turn
        print("server sent:",data)


if __name__ == '__main__':
    try:
        main()
    except ConnectionResetError: # error that raise when it cant speak/send_messages to the server because the server closed(closed = end the program)
        error_and_exit("An Error raised\nthe server closed before closing the client") # printing the error and exit() the program