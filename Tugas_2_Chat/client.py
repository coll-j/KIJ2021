import socket
import sys
import threading
import os
from des import des

key = "secret_k"
d = des()
def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        decoded_data = data.decode('utf-8')
        clear_line()
        username, msg = decoded_data.split("|")
        msg = d.decrypt(key, msg, padding=True)
        print(f"{username}: {msg}")
        print("Pilih aksi [1: kirim pesan, 2: tambah teman, 3: exit]:")

def clear_line():
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line

def client_recieve_file(client_socket,filename):
    size = client_socket.recv(65535)
    size = size.decode('utf-8')
    size = int(float(size))
    size += 1
    file = open(filename, 'wb')
    while size> 0:
        data = client_socket.recv(65535)
        file.write(data)
        size -= 1
    file.close()

def client_send_file(client_socket,filename):
    file = open(filename)
    file.seek(0, os.SEEK_END)
    filesize =str(file.tell()/65535)
    client_socket.send(bytes(filesize, "utf-8"))
    file.close()

    file = open(filename,'rb')

    while True:
        data = file.read(65535)
        if not data:
            file.close()
            break
        client_socket.send(data)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected Username as command line argument')
        exit()

    # buat object socket
    sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect ke server
    sock_cli.connect(("127.0.0.1", 6666))

    # kirim username ke server
    username = sys.argv[1]
    sock_cli.send(bytes(username, "utf-8"))

    # buat thread utk membaca pesan dan jalankan threadnya
    thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
    thread_cli.start()

    while True:
        act = int(input("Pilih aksi [1: kirim pesan, 2: tambah teman, 3: exit]:\n"))
        clear_line()
        if act == 1:
            clear_line()
            # kirim/terima pesan
            dest = input("Masukkan username tujuan (ketikan bcast untuk broadcast pesan):")
            clear_line()
            msg = input("Masukkan pesan untuk {}:".format(dest))
            encrypted = d.encrypt(key, msg, padding=True)
            clear_line()
            data = ["chat",username, dest, encrypted]

            print("<{}>: {}".format(username, msg))
            sock_cli.send(bytes('|'.join(data), 'utf-8'))
        elif act == 2:
            # tambah teman
            clear_line()
            dest = input("Masukkan username yang ingin ditambahkan:")
            # clear_line()
            
            data = "add|{}|{}".format(username, dest)
            sock_cli.send(bytes(data, 'utf-8'))
        if act == 3:
            # sock_cli.send(bytes('exit', 'utf-8'))
            sock_cli.close()
            break

    exit()