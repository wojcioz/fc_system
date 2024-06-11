
import socket
# import pickle
def send_request(url, data):
    ip = url.split(":", 1)[0]
    port = int(url.split(":", 1)[1])
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout value of 2 seconds
        sock.settimeout(2)
        
        # Attempt to connect to the IP address and port
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            print(f"Connection to {ip}:{port} is successful")
            sock.send(data)
        else:
            print(f"Connection to {ip}:{port} failed")

        # Close the socket
        sock.close()
    
    except socket.error as e:
        print(f"Error occurred while connecting: {e}")
   