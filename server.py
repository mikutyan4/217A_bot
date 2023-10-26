import requests
import json
import socket
from flask import Flask, request, jsonify
import os

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

app = Flask(__name__)

@app.route('/', methods = ['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'no uploaded file', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'no file to choose', 400
    
    if file:
        filename = file.filename
        file.save(os.path.join('./images',filename))
        message = process()
        return message, 200

def process():
    print("process the pic here!")
    return jsonify({'message:':' hello!'})

if __name__ == '__main__':
    client_IP = "192.168.128.156"
    try:
        my_server = Server(client_IP)
    except Exception as e:
        print("didn't send IP!")
    app.run(host='0.0.0.0',port = 3000, debug=True)
    