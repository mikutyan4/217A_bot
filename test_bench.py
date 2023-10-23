import server

def server_test():
    my_server = server.Server("192.168.128.156")
    print(my_server.server_IP)
if __name__ == "__main__":
    server_test()