import socket
import pickle


def run_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('0.0.0.0', 8081))

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server is listening on port 8081...')

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f'Connected to client: {client_address}')

        # Receive data from the client
        data = client_socket.recv(1024)
        # print(f'Received data: {data.decode("utf-8")}')
        print(f'Received data: {pickle.loads(data)}')
        
        # Send a response back to the client
        response = 'HTTP/1.1 200 OK\n\nHello, client!'
        client_socket.send(response.encode())
        # Close the client connection
        client_socket.close()

# if __name__ == '__main__':
run_server()