import logging


class Player:
    def __init__(self, name, channel):
        self.name = name
        self.channel = channel
        self.lives = 3
        self.alive = True

    def send_message(self, message, newline=True):
        try:
            if newline:
                self.channel.send(message.encode() + b"\r\n")
            else:
                self.channel.send(message.encode())
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")

    def shoot(self, target):
        if not self.alive:
            self.send_message(f"{self.name} уже мертв и не может стрелять.")
            return False

        if not target.alive:
            self.send_message(f"{target.name} уже мертв и не может быть целью.")
            return False

        self.send_message(f"{self.name} стреляет в {target.name}!")
        return True

    def take_damage(self):
        if self.lives > 0:
            self.lives -= 1
            self.send_message(
                f"{self.name} теряет жизнь! Осталось {self.lives} жизней."
            )
            if self.lives == 0:
                self.alive = False
                self.send_message(f"{self.name} убит!")

    def reset_lives(self):
        self.lives = 3
        self.alive = True
        self.send_message(f"{self.name} восстановил жизни до 3.")
