import socket
from PIL import Image
import pyautogui
pyautogui.FAILSAFE = True

PORT = 23

def toRLE(string):
  compressed_string = ''
  length = 1
  for i in range(2, len(string), 2):
    if string[i - 2:i] == string[i:i + 2]:
      length += 1
    else:
      compressed_string += f'{"" if length == 1 else f"{hex(length)[2:]}"}{string[i - 2:i]},'
      length = 1
  compressed_string += f'{"" if length == 1 else f"{hex(length)[2:]}"}{string[len(string) - 2:]}'
  return compressed_string

def compress(pixels):
  grayscale = map(lambda x: int((x[0] + x[1] + x[2]) / 3), pixels)
  toHex = lambda x: hex(x)[2:] if x >= 16 else f'0{hex(x)[2:]}'
  rleHexes = toRLE(''.join(map(toHex, grayscale)))
  return rleHexes

def getDisplayData():
  im = pyautogui.screenshot()
  im = im.resize((int(0.5 * im.size[0]), int(0.5 * im.size[1])), Image.ANTIALIAS)
  size = ','.join(map(str, im.size))
  pixels = im.getdata()

  return f'{size};{compress(pixels)}'

from servercommands import ServerCommands

shuttingdown = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('', PORT))
  print(f'Server listening on port {PORT}...')
  s.listen(1)
  while True:
    conn, addr = s.accept()
    with conn:
      print('Connected with', addr)
      def send(d):
        conn.send(d.encode())
      commandHandler = ServerCommands(send)

      while True:
        data = conn.recv(1024)
        if not data: continue
        words = data.decode().split(' ')
        commandHandler.handle(words[0], words[1:])
        if words[0] == 'quit':
          print('Connection with', addr, 'has closed.\nWaiting for new connections...')
          break
        elif words[0] == 'shutdown':
          print('Connection has requested shutdown of server.')
          if commandHandler.isAuthenticated:
            shuttingdown = True
            print('Authorised. Shutting down...')
            send('Authorised. Shutting down...')
            break
          else:
            print('Not Authorised.')
            send('Error: This command requires an authenticated connection')

      if shuttingdown:
        break
