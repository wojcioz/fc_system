import socket

def check_connection(ip, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout value of 2 seconds
        sock.settimeout(2)
        
        # Attempt to connect to the IP address and port
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            print(f"Connection to {ip}:{port} is successful")
        else:
            print(f"Connection to {ip}:{port} failed")
        
        # Close the socket
        sock.close()
        
    except socket.error as e:
        print(f"Error occurred while connecting: {e}")

# Call the function to check the connection
check_connection("192.168.0.170", 8081)