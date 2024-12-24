import logging
import socket
import threading
import time
from collections import deque

from config import Config
from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)


class Server():
  """ TCP message server. """

  def __init__(self):
    self._config = Config()

    self._lt: list = []  # topic list
    self._kko: deque = deque()  # received messages
    self._kkw: deque = deque()  # sent messages
    self.stop_server = False
    self.clients = {}

    logger.debug(f"Starting TCP server \"{self._config["ServerID"]}\" with config:\n"
                 f"{"\n".join(f"{k}={v}" for k, v in self._config.items())}")

    self._start_communication_thread()
    self._start_monitoring_thread()
    self._start_ui_thread()

  def _start_communication_thread(self) -> None:
    """ Start the communication thread. """
    communication_thread = threading.Thread(target=self._listen)
    communication_thread.start()

  def _listen(self) -> None:
    """ Listen for incoming messages. """
    try:
      serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      logger.info(f"hostname: {socket.gethostname()}")
      serversocket.bind((socket.gethostname(), 8000))
      serversocket.listen(5)
      serversocket.settimeout(self._config["TimeOut"])
      while not self.stop_server:
        try:
          clientsocket, address = serversocket.accept()
          # check if the address is allowed
          # start a new thread to handle the connection
          client_thread = threading.Thread(
            target=self._handle_client, args=(clientsocket, address))
          client_thread.start()
          logger.debug(f"Connection from {address} has been established!")
          clientsocket.send(bytes("Welcome to the server!", "utf-8"))
        except socket.timeout:
          logger.debug("Socket timed out.")
        except OSError as e:
          logger.error(
            f"Encountered an OSError while accepting a connection: {e}")

    except PermissionError as e:
      logger.error(
        f"Encountered an exception while trying to start a socket: {e}")
    except OSError as e:
      logger.error(
        f"Encountered an OSError while trying to start a socket: {e}")

  def _handle_client(self, clientsocket: socket, address):
    """ Handle communication with the client. """
    clientsocket.settimeout(self._config["TimeOut"])
    while not self.stop_server:
      try:
        request = clientsocket.recv(self._config["SizeLimit"]).decode("utf-8")
        if request:
          logger.info(f"Received message from {address}: {request}")
          self._kko.append((address, request))
        # else:
          # logger.debug(f"Client {address} has disconnected.")  # temp prob
          break
      except socket.timeout:
        pass
      except socket.error as e:
        logger.error(
          f"Encountered a socket error while communicating with client {address}: {e}")
        break

  def _start_monitoring_thread(self) -> None:
    """ Start monitoring thread responsible for handling communication topics. """

    while not self._kko:
      time.sleep(1 / 1000)
    logger.info(self._kko)

  def _start_ui_thread(self) -> None:  # Main module for the server?
    """ Start the user interface thread (cli). """
    pass


if __name__ == "__main__":
  server = Server()
