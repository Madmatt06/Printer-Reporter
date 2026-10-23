import socket


def main():
  host:str = input('Enter a host address/name: ')
  try:
    port:int = int(input("Enter a port: "))
  except ValueError:
    print("Invalid port entered")
    return
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((host, port))
  while(True):
    try:
      message:int = int(input('Enter a command: '))
    except ValueError:
      print('Invalid command given. Closing connection')
      client.close()
      return
    if message < 0:
      print(int.from_bytes(client.recv(1)))
    else:
      client.send(message.to_bytes())



if __name__ == '__main__':
    main()
