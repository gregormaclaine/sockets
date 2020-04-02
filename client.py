import telnetlib

HOST = "localhost"
print('Connecting...')
tn = telnetlib.Telnet(HOST)
print('Connected.')
tn.write(b'getscreen\n')
print('Reading data...')
print(tn.read_all().decode('ascii'))
print('/\\')