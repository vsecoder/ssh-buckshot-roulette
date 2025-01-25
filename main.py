from server.server import start_server
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler("game.log"), logging.StreamHandler()],
)

if __name__ == "__main__":
    start_server()
