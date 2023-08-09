import socket

HOST = '192.168.1.67'  # Change this to the IP address of your Unity machine if needed
PORT = 1755

hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)

def send_data(data):
    s = socket.socket()          
              
    # connect to the server on local computer 
    s.connect((IPAddr, PORT))
    s.send(data.encode())
    s.close()

# Example usage:
send_data("ORGA")
#send_data("RECY")
#send_data("O")
#send_data("R")