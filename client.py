import socket
import sys

if len(sys.argv) < 3:
  HOST = 'localhost'
else:
  HOST = sys.argv[2]

PORT = 23
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  try:
    s.connect((HOST, PORT))
  except ConnectionRefusedError:
    print(f'Error: Could not connect with host ({HOST}:{PORT})')
    exit()

  while True:
    i = ''
    while i == '':
      i = input('>>>')

    s.send(i.encode())
    if i == 'quit':
      print('Connection with host closed.')
      break

    data = s.recv(1024).decode('ascii')
    if i == 'shutdown' and 'Shutting down...' in data:
      print('Connection with host closed.')
      break

    print(data + '\n')
