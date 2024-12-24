""" Configuration module for the application. """
import json
import logging
import os
from collections.abc import MutableMapping
from typing import Any, Optional

from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(MutableMapping):
  """ Configuration class for the application. """

  def __init__(self,
               config_file_path: Optional[str] = None):

    self._default_config_path: str = os.path.join(
      PROJECT_ROOT, "config.json")
    self._config_file_path: str = config_file_path or self._default_config_path
    self._load_config()

  def init_config(self) -> None:
    """ Initialize default configuration values. """
    self._config = {
      "ServerID": "it's me, your server",
      "ListenAddresses": ["*"],
      "TimeOut": 3,
      "SizeLimit": 1048576,
      "AllowedIPAdddresses": ["10.0.0.0/24", "192.168.1.0/24"]
    }

    self._write_config_to_json()

  def _write_config_to_json(self) -> bool:
    """ Write config to a JSON file. 

    Returns:
      bool: True if the config was written successfully, False otherwise.
    """
    try:
      os.makedirs(os.path.dirname(self._config_file_path), exist_ok=True)

      with open(self._config_file_path, "w", encoding="utf-8") as config_file:
        json.dump(self._config, config_file, indent=2)
      return True
    except FileNotFoundError as e:
      logger.error(f"The configuration file was not found. {e}")
      return False
    except IOError as e:
      logger.error(
        f"An error occured while writing the configuration file. {e}")
      return False

  def _load_config(self) -> bool:
    """ Load config from the configuration file. 

    Returns:
      bool: True if the config was loaded successfully, False otherwise.
    """

    try:
      if not os.path.exists(self._config_file_path):
        logger.info(f"Configuration file {
                    self._config_file_path} not found. Initializing default configuration.")
        self.init_config()
        return True
      else:
        with open(self._config_file_path, "r", encoding="utf-8") as config_file:
          try:
            self._config = json.load(config_file)
          except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            self.init_config()
            return False
        return True
    except FileNotFoundError as e:
      logger.error(f"The configuration file was not found. {e}")
      return False
    except (IOError, json.JSONDecodeError) as e:
      logger.error(
        f"An error occured while reading the configuration file. {e}")
      return False

  """ MutableMapping methods """

  def __getitem__(self, key: str) -> Any:
    return self._config[key]

  def __setitem__(self, key: str, value: Any):
    self._config[key] = value
    self._write_config_to_json()

  def __delitem__(self, key: str):
    try:
      del self._config[key]
      self._write_config_to_json()
    except KeyError:
      logger.warning(f"Key not found in config: {key}.")

  def __iter__(self):
    return iter(self._config)

  def __len__(self):
    return len(self._config)

  def __repr__(self):
    return f"{self.__class__.__name__}({self._config})"


if __name__ == "__main__":
  """ Example usage of the config module. """

  # Initialize the config
  pwd = os.path.dirname(os.path.abspath(__file__))
  tmp_config_path = os.path.join(pwd, "tmp_config.json")
  config = Config(tmp_config_path)
  config.init_config()

  print(f"Current config: {config}")
  print(f"ServerID: {config["ServerID"]}")

  config["ServerID"] = "new_server_id"
  print(f"Updated config: {config}")

  del config["ServerID"]
  print(f"Deleted ServerID: {config}")

  # Cleanup
  os.remove(tmp_config_path)
