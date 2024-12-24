import socket
import json
import time


class Client:
  """ TCP message client. """

  def __init__(self, server_address, server_port):
    self._server_address = server_address
    self._server_port = server_port
    self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def connect(self):
    """ Connect to the server. """
    try:
      self.client_socket.connect((self._server_address, self._server_port))
      print("Connected to server!")
      # receive welcome message
      welcome_message = self.client_socket.recv(1024).decode("utf-8")
      print(f"Server: {welcome_message}")
    except ConnectionRefusedError:
      print("Connection refused.")
    except ConnectionResetError:
      print("Connection reset.")
    except ConnectionAbortedError:
      print("Connection aborted.")

  def send_message(self, message_type, topic="", content=""):
    message = {
        "type": message_type,
        "topic": topic,
        "content": content
    }
    try:
      self.client_socket.send(json.dumps(message).encode("utf-8"))
      print(f"Sent message: {message}")
    except ConnectionResetError:
      print("Connection reset.")
    except ConnectionAbortedError:
      print("Connection aborted.")

  def close(self):
    self.client_socket.close()
    print("Connection closed.")


if __name__ == "__main__":
  client = Client("y700", 8000)
  client.connect()

  # Example usage:
  client.send_message("register", "topic1", "producer")
  time.sleep(1)
  client.send_message("message", "topic1", "Hello from client!")
  time.sleep(1)
  client.send_message("withdraw", "topic1", "producer")

  client.close()
