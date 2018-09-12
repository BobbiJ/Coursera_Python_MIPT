import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    storage = ""

    @staticmethod
    def process_data(data):
        try:
            data_arr = data.split(' ')
            if data_arr[0] == 'put':
                try:
                    arr_to_add = [data_arr[1], str(float(data_arr[2])), str(int(data_arr[3])), '\n']
                    string_to_add = ' '.join(arr_to_add)
                    if string_to_add not in ClientServerProtocol.storage:
                        ClientServerProtocol.storage += string_to_add
                    return "ok\n\n"
                except Exception:
                    return 'error\nwrong command\n\n'
            elif data_arr[0] == 'get':
                storage_arr = ClientServerProtocol.storage.split('\n')
                response_arr = ''
                if data_arr[1].strip('\n') == '*':
                    return 'ok\n' + ClientServerProtocol.storage + '\n\n'
                for line in storage_arr:
                    if data_arr[1].strip('\n') in line:
                        response_arr += line + '\n'
                response_final = 'ok\n' + response_arr + '\n\n'
                return response_final
            else:
                return 'error\nwrong command\n\n'
        except Exception:
            return 'error\nwrong command\n\n'

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = ClientServerProtocol.process_data(data.decode())
        self.transport.write(resp.encode())


# run_server('127.0.0.1', 8888)
