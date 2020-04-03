import os
from dotenv import load_dotenv
load_dotenv()

PASSWORD = os.getenv("PASSWORD")

class command():
  '''Wrapper to show it is a server command'''
  def __init__(self, name, reqauth=False):
    self.name = name
    self.reqauth = reqauth
  
  def __call__(self, fn):
    fn.command_name = self.name
    fn.reqauth = self.reqauth
    return fn

class ServerCommands:
  def __init__(self, send):
    self.send = send
    self.commands = {}

    self.isAuthenticated = False

    for k in dir(self):
      method = getattr(self, k)
      try:
        name = method.command_name.lower()
      except:
        continue
      self.commands[name] = method

  def handle(self, command, params):
    print(f'>{command} {" ".join(params)}')
    command = command.lower()
    if command in ['quit', 'shutdown']:
      pass
    elif command not in self.commands:
      self.send('Error: Command not recognised.')
    elif not self.isAuthenticated and self.commands[command].reqauth:
      self.send('Error: This command requires an authenticated connection')
    else:
      self.commands[command](params)

  @command('auth')
  def auth_command(self, params):
    if len(params) == 0:
      self.send(f'Connection is {"" if self.isAuthenticated else "not "}authenticated.')
    elif params[0] == PASSWORD:
      self.isAuthenticated = True
      self.send(f'Authentication successful.')
      print('Connection authenticated\n')
    else:
      self.send(f'Authentication failed.')

  @command('hello')
  def test_command(self, params):
    self.send('Hello!')
  