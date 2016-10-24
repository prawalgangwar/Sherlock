import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)


while True:
	conn, addr = s.accept()
	print 'Got connection from', addr
	f = open('received_image.jpg', 'wb')
    print 'file opened'
    while True:
        print('receiving data...')
        data = conn.recv(1024)
        if not data:
            break
        # write data to a filex
        f.write(data)
        f.close()


print('Successfully get the file')
s.close()
print('connection closed')