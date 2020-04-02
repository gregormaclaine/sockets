import socket

HOST = 'localhost'
PORT = 23
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))

  while True:
    i = ''
    while i == '':
      i = input('>>>')
    s.send(i.encode())
    data = s.recv(1024)
    print(data.decode('ascii') + '\n')
