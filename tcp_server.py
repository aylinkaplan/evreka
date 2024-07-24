import django
django.setup()

import socket
import json
from device.tasks import process_location_data

HOST = '0.0.0.0'
PORT = 65432


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server started at {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                location_data = json.loads(data)
                process_location_data.delay(
                    location_data['device_id'],
                    location_data['latitude'],
                    location_data['longitude'],
                    location_data['created_at']
                )


if __name__ == '__main__':
    start_server()
