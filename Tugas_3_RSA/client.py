import socket
import sys
import threading
import os
from rsa import RSA
import pickle

public_keys = {}
rsa = RSA()

def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        decoded_data = data.decode('utf-8')
        try:
            username, msg = decoded_data.split("|")
            try: # parse public key as tuple
                public_key = eval(msg)
                if type(public_key) == tuple:
                    public_keys[username] = public_key
                    print(f"{username} ditambahkan sebagai teman.")
                else:
                    print("decrypting...")
                    msg = rsa.decrypt(int(msg))
                    print(f"  {username}: {msg.decode('utf-8')}")
            except:
                pass
        except:
            pass


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
    public_key_cli = rsa.public_key
    sock_cli.send(bytes(f"{username}|{public_key_cli}", "utf-8"))
    public_keys[username] = public_key_cli

    # buat thread utk membaca pesan dan jalankan threadnya
    thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
    thread_cli.start()

    while True:
        act = int(input("Pilih aksi [1: kirim pesan, 2: tambah teman, 3: exit, 4: lihat public key]:\n"))
        if act == 1:
            # kirim/terima pesan
            dest = input("Masukkan username tujuan: ")
            msg = input("Masukkan pesan untuk {}: ".format(dest))
            if dest in public_keys:
                public_key = public_keys[dest]
                encrypted = rsa.encrypt(msg, public_key)
                data = ["chat",username, dest, str(encrypted.text)]

                print("  <{}>: {}".format(username, msg))
                sock_cli.send(bytes('|'.join(data), 'utf-8'))
            else:
                print(f"{dest} belum ditambahkan sebagai teman.")
        elif act == 2:
            # tambah teman
            dest = input("Masukkan username yang ingin ditambahkan: ")
            data = "add|{}|{}".format(username, dest)
            sock_cli.send(bytes(data, 'utf-8'))
        elif act == 3:
            # sock_cli.send(bytes('exit', 'utf-8'))
            sock_cli.close()
            exit()
        elif act == 4:
            print("Public key for {} is {}".format(username, public_keys[username]))
            continue