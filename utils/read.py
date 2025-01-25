import socket
import logging


# Функция для чтения данных до символа новой строки
def read_until_newline(chan, buffer_size=1024):
    data = ""
    try:
        while not chan.closed:
            chunk = chan.recv(buffer_size).decode("utf-8")
            logging.debug(f"Получены данные: {chunk}")
            if not chunk:
                break
            data += chunk
            if "\r\n" in data or "\r" in data:
                data = data.split("\r\n")[0].split("\r")[0]
                break
    except socket.timeout:
        logging.warning("Таймаут при чтении данных.")
    except Exception as e:
        logging.error(f"Ошибка в read_until_newline: {e}")
    return data.strip()
