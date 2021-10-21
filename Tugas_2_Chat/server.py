import socket
import threading
import os

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
        
        # parsing pesannya
        act = data.decode("utf - 8").split("|")[0]

        if act == 'get_user':
            send_user_list(sock_cli)
        elif act == 'add':
            _, user_1, user_2 = data.decode("utf - 8").split("|")
            if user_2 in clients:
                add_friend(user_1, user_2)
                send_msg(sock_cli, '{} added as friend'.format(user_2))
            else:
                send_msg(sock_cli, '{} not found'.format(user_2))

        elif act == 'chat':
            act, sender, dest, msg = data.decode("utf - 8").split("|")
            msg = "<{}>: {}".format(username_cli, msg)

            #terusankan psan ke semua klien
            if dest =="bcast":
                send_broadcast(clients, '[bcast] ' + msg, addr_cli, sender)
            else:
                if dest in clients:
                    if dest in friends[sender]:
                        dest_sock_cli = clients[dest][0]
                        send_msg(dest_sock_cli, msg)
                    else:
                        send_msg(sock_cli, '{} is not a friend yet'.format(dest))
                else:
                    send_broadcast(clients, '[bcast] ' + msg, addr_cli, sender)
            print(data)
        elif act == 'file':
            act, sender, dest, msg = data.decode("utf - 8").split("|")
            filename = msg
            server_recieve_file(sock_cli,filename)
            # terusankan file ke semua klien
            if dest =="bcast":
                send_broadcast(clients,"file" , addr_cli, sender)
                send_file_broadcast(clients,filename , addr_cli, sender)
            else:
                if dest in clients:
                    if dest in friends[sender]:
                        dest_sock_cli = clients[dest][0]
                        send_msg(dest_sock_cli, "file")
                        server_send_file(dest_sock_cli, filename)
                    else:
                        send_msg(sock_cli, '{} is not a friend yet'.format(dest))
                else:
                    send_broadcast(clients, "file" , addr_cli, sender)
                    send_file_broadcast(clients,filename, addr_cli, sender)
            print(data)
            os.remove(filename)
    sock_cli.close()
    print("Connection closed", addr_cli)

# kirim ke semua klien
def send_broadcast(clients, data, sender_addr_cli, sender_uname):
    for uname in friends[sender_uname]:
        sock_cli, addr_cli, _ = clients[uname]
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg(sock_cli, data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

def send_user_list(sock_cli):
    send_msg(sock_cli, ', '.join(clients.keys()))

def add_friend(username_cli, username_friend):
    friends[username_cli].append(username_friend)

def server_recieve_file(server_socket,filename):

    size = server_socket.recv(65535)
    size = size.decode('utf-8')
    size = int(float(size))
    size += 1
    file = open(filename, 'wb')
    while size > 0:
        data = server_socket.recv(65535)
        file.write(data)
        size -= 1
    file.close()

def server_send_file(server_socket,filename):
    server_socket.send(bytes(filename,"utf-8"))

    file = open(filename)
    file.seek(0, os.SEEK_END)
    filesize =str(file.tell()/65535)
    server_socket.send(bytes(filesize,"utf-8"))
    file.close()

    file = open(filename,'rb')
    while True:
        data = file.read(65535)
        if not data:
            file.close()
            break
        server_socket.send(data)

def send_file_broadcast(clients, filename, sender_addr_cli, sender_uname):
    for uname in friends[sender_uname]:
        sock_cli, addr_cli, _ = clients[uname]
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            server_send_file(sock_cli, filename)

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

    while True:
        # accept connection dari klien
        sock_cli, addr_cli = sock_server.accept()

        # baca username klien
        username_cli = sock_cli.recv(65535).decode("utf-8")
        print(username_cli, " joined")

        # buat thread baru untuk membaca pesan dan jalankan threadnya
        thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
        thread_cli.start()

        # simpan informasi ttg klien ke dictionary
        clients[username_cli] = (sock_cli, addr_cli, thread_cli)
        friends[username_cli] = []

