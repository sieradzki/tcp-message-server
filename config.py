""" Configuration module for the application. """
import json
import logging
import os
from collections.abc import MutableMapping
from typing import Any, Optional

logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(MutableMapping):
  def __init__(self,
               config_file_path: Optional[str] = None):

    self._default_config_path = os.path.join(
      PROJECT_ROOT, "config.json")
    self._config_file_path = config_file_path or self._default_config_path
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

    self.write_config_to_JSON()

  def write_config_to_JSON(self) -> bool:
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
          self._config = json.load(config_file)
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
    self.write_config_to_JSON()

  def __delitem__(self, key: str):
    del self._config[key]
    self.write_config_to_JSON()

  def __iter__(self):
    return iter(self._config)

  def __len__(self):
    return len(self._config)

  def __repr__(self):
    return f"{self.__class__.__name__}({self._config})"


if __name__ == "__main__":
  config = Config()
  print(config)