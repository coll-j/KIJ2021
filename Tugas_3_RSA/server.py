import socket
import threading
import os

public_keys = {}

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        # parsing pesannya
        act = data.decode("utf - 8").split("|")[0]

        if act == 'add':
            # TODO: add friend will pass public key to be stored in client
            _, user_1, user_2 = data.decode("utf - 8").split("|")
            if user_2 in clients:
                add_friend(user_1, user_2)
                msg = public_keys[user_2]
            else:
                msg = "[error not found]"
            send_msg(sock_cli, f'{user_2}|{msg}')


        elif act == 'chat':
            act, sender, dest, msg = data.decode("utf - 8").split("|")
            msg = "<{}>|{}".format(username_cli, msg)

            #terusankan psan ke semua klien
            if dest in clients:
                if dest in friends[sender]:
                    dest_sock_cli = clients[dest][0]
                    send_msg(dest_sock_cli, msg)
                else:
                    send_msg(sock_cli, '{} is not a friend yet'.format(dest))
            else:
                send_msg(sock_cli, '{} user not found'.format(dest))
            print(data)
    sock_cli.close()
    print("Connection closed", addr_cli)

# kirim ke semua klien
def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

def add_friend(username_cli, username_friend):
    friends[username_cli].append(username_friend)


if __name__ == '__main__':
    # buat object socket server
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # buat object socket server
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binding object socket ke alamat IP dan port tertentu
    sock_server.bind(("0.0.0.0", 6666))

    # listen for an incoming connection
    sock_server.listen(5)

    # buat dictionary utk menyimpan informasi ttg klien
    clients = {}
    friends = {}

    try:
        while True:
            # accept connection dari klien
            sock_cli, addr_cli = sock_server.accept()

            # baca username klien
            username_cli, public_key = sock_cli.recv(65535).decode("utf-8").split("|")
            print(username_cli, " joined")
            public_keys[username_cli] = public_key

            # buat thread baru untuk membaca pesan dan jalankan threadnya
            thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
            thread_cli.start()

            # simpan informasi ttg klien ke dictionary
            clients[username_cli] = (sock_cli, addr_cli, thread_cli)
            friends[username_cli] = []
    except KeyboardInterrupt:
        sock_server.close()
        exit()
