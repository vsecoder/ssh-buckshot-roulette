import socket
import paramiko
import threading
import logging
from utils.read import read_until_newline
from game.game import Game
from paramiko import Transport, RSAKey
from game.player import Player


def handle_client(client, game):
    t = Transport(client)
    t.load_server_moduli()
    t.add_server_key(RSAKey(filename="test.rsa"))
    t.start_server(server=Server(game))

    chan = t.accept(20)
    if not chan:
        return

    chan.send("=== Добро пожаловать в Buckshot Roulette! ===\r\n")
    chan.send("Введите ваш ник: ")
    nickname = read_until_newline(chan)
    player = Player(nickname, chan)
    if game.add_player(player):
        chan.send(f"Добро пожаловать, {nickname}!\r\n")
    else:
        chan.send("Лобби заполнено. Подключение отклонено.\r\n")
        chan.close()
        return

    if game.host == player:
        chan.send("Вы хост. Нажмите Enter, чтобы начать игру.\r\n")
        read_until_newline(chan)
        game.start_game()
    else:
        chan.send("Ожидайте начала игры.\r\n")
        game.host.send_message(f"Новый игрок: {nickname}\r\n")


class Server(paramiko.ServerInterface):
    def __init__(self, game):
        self.event = threading.Event()
        self.user = "root"
        self.password = "root"
        self.game = game

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == self.user) and (password == self.password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        if (username == self.user) and (key == RSAKey(filename="test.rsa")):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def enable_auth_gssapi(self):
        return False

    def get_allowed_auths(self, username):
        return "password,publickey"

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(
        self, channel, term, width, height, pixelwidth, pixelheight, modes
    ):
        return True


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", 2222))
    server.listen(5)

    game = Game(rounds=3)

    while True:
        try:
            client, addr = server.accept()
            logging.debug(f"Новое подключение: {addr}")
            threading.Thread(target=handle_client, args=(client, game)).start()
        except Exception as e:
            logging.debug(e)
