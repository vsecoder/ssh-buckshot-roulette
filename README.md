# ssh buckshot roulette

## Запуск сервера

```bash
ssh-keygen -t rsa -b 2048 -f test.rsa
pip3 install -r requirements.txt
python3 main.py
```

## Подключение

```bash
ssh root@ip -p 2222
```

`Пароль: root` 

Первый подключившийся - хост, который начинает игру.

```
=== Добро пожаловать в Buckshot Roulette! ===
Введите ваш ник: Добро пожаловать, vsecoder!
Вы хост. Нажмите Enter, чтобы начать игру.
Новый игрок: vsecoder
```

