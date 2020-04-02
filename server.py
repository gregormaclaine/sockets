import socketserver
from telnetsrv.threaded import TelnetHandler, command
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

class MyHandler(TelnetHandler):
  WELCOME = "Connected to telnet server"

  @command('getscreen')
  def command_random(self, params):
    self.writeresponse(f'({getDisplayData()})')

class TelnetServer(socketserver.TCPServer):
  allow_reuse_address = True

server = TelnetServer(("0.0.0.0", PORT), MyHandler)
print(f'Listening on port {PORT}...')
server.serve_forever()