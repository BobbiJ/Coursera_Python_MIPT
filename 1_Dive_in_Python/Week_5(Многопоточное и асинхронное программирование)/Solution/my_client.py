import socket
import time


class Client:
    def __init__(self, url, port, timeout=None):
        super().__init__()
        self.url = url
        self.port = port
        self.timeout = timeout
        self.connection = socket.create_connection((url, port), timeout)

    @staticmethod
    def sort_by_timestamp(arr):
        return arr[0]

    def put(self, name, value, timestamp=time.time()):
        timestamp = int(timestamp)
        response = f'put {name} {value} {timestamp}\n'
        self.connection.sendall(response.encode())
        request = self.connection.recv(1024)
        if request.decode().split('\n')[0] == 'error':
            raise ClientError()
        else:
            return request.decode()

    def get(self, key):
        response = f"get {key}\n".encode()
        self.connection.send(response)
        request = self.connection.recv(1024)
        request_arr = request.decode().split('\n')
        if request_arr[0] == 'ok':
            request_dict = dict()
            for entry in request_arr[1:]:
                if len(entry) > 0:
                    metric = entry.split(' ')
                    if metric[0] not in request_dict.keys():
                        request_dict.update({metric[0]: [(int(metric[2]), float(metric[1]))]})
                    else:
                        exist_arr = request_dict[metric[0]]
                        exist_arr.append((int(metric[2]), float(metric[1])))
                        exist_arr.sort(key=Client.sort_by_timestamp)
                        request_dict.update({metric[0]: exist_arr})
        else:
            raise ClientError()
        return request_dict


class ClientError (Exception):
    pass


client = Client('127.0.0.1', 8181, 1)
print(client.get("palm"))