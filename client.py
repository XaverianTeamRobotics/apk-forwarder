import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
HOST = "robopi.local"
PORT = 5001

def send_apk():
    s = socket.socket()
    print(f"[+] Connecting to {HOST}:{PORT}")
    s.connect((HOST, PORT))
    print("[+] Connected to ", HOST)
    filename = "TeamCode-debug.apk"
    filepath = "./TeamCode/build/intermediates/apk/debug/TeamCode-debug.apk"
    filesize = os.path.getsize(filepath)
    s.send(f"{filename}{SEPARATOR}{filesize}{SEPARATOR}{PASSWORD}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filepath, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()

if __name__ == "__main__":
    send_apk()
