import django


django.setup()

import socket
import json
from device.tasks import process_location_data


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 65432))
        s.listen(5)
        while True:
            client_socket, addr = s.accept()
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                try:
                    location_data = json.loads(data)
                    process_location_data.delay(
                        location_data['device_id'],
                        location_data['latitude'],
                        location_data['longitude'],
                    )
                    client_socket.sendall(b"Data received and processed")
                except json.JSONDecodeError:
                    client_socket.sendall(b"Invalid JSON format")
            client_socket.close()


if __name__ == '__main__':
    start_server()
