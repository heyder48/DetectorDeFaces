import socket

class Sender(object):

    def __init__(self, sock = None):

        if sock is None:

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        else:

            self.sock = sock
    
    def Connect(self, host, port):

        self.sock.connect((host, port))    
    
    def SendData(self,data):

        totalSend = 0

        while totalSend < len(data):

            sent = self.sock.send(data[totalSend:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")

            totalSend+=sent

    def Close(self):

        self.sock.close() 