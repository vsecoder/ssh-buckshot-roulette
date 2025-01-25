import random
import logging


class Gun:
    def __init__(self):
        self.bullets = []
        self.unshufled_bullets = []
        self.current_bullet = 0
        self.reload()

    def reload(self):
        total_bullets = random.randint(2, 8)

        live_bullets = random.randint(1, total_bullets - 1)
        blank_bullets = total_bullets - live_bullets

        self.bullets = ["-"] * blank_bullets + ["+"] * live_bullets
        self.unshufled_bullets = self.bullets.copy()

        random.shuffle(self.bullets)
        self.current_bullet = 0

    def get_bullets_display(self):
        bullet_display = " | ".join(self.unshufled_bullets)
        return f"[ {bullet_display} ]"

    def fire(self):
        if self.current_bullet >= len(self.bullets):
            logging.debug("Все патроны использованы.")
            return None

        bullet = self.bullets[self.current_bullet]
        self.current_bullet += 1
        logging.debug(
            f"Использован патрон: {bullet}, Осталось: {len(self.bullets) - self.current_bullet}"
        )
        return bullet
