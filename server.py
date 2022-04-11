import socket
import tqdm
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
APK_NAME = "TeamCode-debug.apk"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))

def listen_for_file():
	s.listen(10)
	print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
	print("Waiting for the client to connect... ")
	client_socket, address = s.accept()
	print(f"[+] {address} is connected.")
	received = client_socket.recv(BUFFER_SIZE).decode()
	filename, filesize= received.split(SEPARATOR)
	filename = os.path.basename(filename)
	filesize = int(filesize)
	progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
	with open(filename, "wb") as f:
		while True:
			bytes_read = client_socket.recv(BUFFER_SIZE)
			if not bytes_read:
				break
			f.write(bytes_read)
			progress.update(len(bytes_read))
	client_socket.close()

def send_apk_to_device():
	if os.path.exists(APK_NAME):
		os.popen("adb install " + APK_NAME)

while __name__ == "__main__":
	listen_for_file()
	send_apk_to_device()
