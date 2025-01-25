import logging
from utils.read import read_until_newline
from .gun import Gun


class Game:
    def __init__(self, rounds=3):
        self.players = []
        self.gun = Gun()
        self.current_player_index = 0
        self.rounds = rounds
        self.current_round = 1
        self.host = None

    def add_player(self, player):
        if len(self.players) < 4:
            self.players.append(player)
            if not self.host:
                self.host = player
            return True
        return False

    def broadcast(self, message, newline=True):
        for player in self.players:
            player.send_message(message, newline)

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        logging.debug(
            f"Следующий игрок: {self.players[self.current_player_index].name}"
        )

    def get_current_player(self):
        return self.players[self.current_player_index]

    def play_turn(self, target_index):
        try:
            current_player = self.get_current_player()
            target = self.players[target_index]

            if not target.alive:
                current_player.send_message("Цель уже мертва. Выберите другую.")
                return

            logging.debug(f"{current_player.name} стреляет в {target.name}")

            if not current_player.shoot(target):
                return

            bullet = self.gun.fire()

            if bullet == "+":
                target.take_damage()
                if not target.alive:
                    self.broadcast(f"{target.name} убит!")
                self.next_player()
            else:
                self.broadcast(f"Холостой выстрел! {target.name} не пострадал.")
                if target == current_player:
                    self.broadcast(
                        f"{current_player.name} выстрелил в себя холостым. Ход остается у него."
                    )

            if self.gun.current_bullet >= len(self.gun.bullets):
                self.broadcast("Все патроны использованы. Перезарядка...")
                self.gun.reload()
                self.broadcast("Ружье перезаряжено. Продолжаем игру.")
                self.broadcast(f"Барабан: {self.gun.get_bullets_display()}")

            if self.check_winner():
                return

        except IndexError:
            logging.error(f"Цель {target_index} не существует.")
        except Exception as e:
            logging.error(f"Ошибка в play_turn: {e}")

    def check_winner(self):
        alive_players = [player for player in self.players if player.alive]
        if len(alive_players) == 1:
            self.broadcast(f"=== {alive_players[0].name} выиграл раунд! ===")
            return True
        return False

    def reset_round(self):
        self.broadcast(f"\n--- Раунд {self.current_round} завершен. ---")
        for player in self.players:
            player.reset_lives()
        self.gun.reload()
        self.current_round += 1
        self.broadcast("Ружье перезаряжено. Начинается следующий раунд.")
        self.broadcast(f"Барабан: {self.gun.get_bullets_display()}")

    def start_game(self):
        self.broadcast("=== Начало игры! ===")
        while self.current_round <= self.rounds:
            self.broadcast(f"\n=== Раунд {self.current_round} ===")
            self.broadcast(f"Барабан: {self.gun.get_bullets_display()}")
            while True:
                alive_players = [player for player in self.players if player.alive]
                if len(alive_players) == 1:
                    self.broadcast(f"=== {alive_players[0].name} выиграл раунд! ===")
                    break

                current_player = self.get_current_player()
                if not current_player.alive:
                    self.next_player()
                    continue

                current_player.send_message("Ваш ход. Выберите цель:")
                for i, player in enumerate(self.players):
                    if player.alive:
                        current_player.send_message(f"{i}: {player.name}")

                try:
                    target_index = int(read_until_newline(current_player.channel))
                    logging.debug(f"Выбрана цель: {target_index}")
                    if 0 <= target_index < len(self.players):
                        if not self.players[target_index].alive:
                            current_player.send_message(
                                "Цель уже мертва. Выберите другую."
                            )
                            continue
                        self.play_turn(target_index)
                    else:
                        current_player.send_message(
                            "Неверный выбор цели. Попробуйте снова."
                        )
                except ValueError as e:
                    logging.error(f"Ошибка ввода: {e}")
                    current_player.send_message("Ошибка ввода. Попробуйте снова.")
                except Exception as e:
                    logging.error(f"Неожиданная ошибка: {e}")
                    current_player.send_message("Ошибка. Попробуйте снова.")

            if self.current_round < self.rounds:
                self.reset_round()
            else:
                self.broadcast("=== Игра окончена. ===")
                break
