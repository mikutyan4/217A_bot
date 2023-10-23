import requests
import json
import socket

class Server:
    def __init__(self, client_IP, client_port = 3000, server_port = 3000):
        self.get_server_IP()
        self.server_port = server_port
        url = f"http://{client_IP}:{client_port}"
        data = {"server_IP":self.server_IP,
                "server_port":self.server_port}
        response = requests.post(url, json = data)
        if response.status_code == 200:
            print("connected!")
            self.connected = True
        else:
            print("unabled to connect!")
            self.connected = False

    def get_server_IP(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            server_IP = s.getsockname()[0]
        except Exception:
            server_IP = '127.0.0.1'
        finally:
            s.close()
        self.server_IP = server_IP