import os
import unittest
from unittest import mock
import tempfile
import json

from config import Config


class TestConfig(unittest.TestCase):
  """ Unit tests for the Config class. """

  @classmethod
  def setUpClass(cls):
    # Create temp directory and set as working dir to prevent overriding current config
    cls.temp_dir = tempfile.TemporaryDirectory()
    cls.original_cwd = os.getcwd()
    os.chdir(cls.temp_dir.name)
    cls.config_path = os.path.join(os.getcwd(), "config.json")

    # remove any existing config file
    if os.path.exists(cls.config_path):
      os.remove(cls.config_path)

  @classmethod
  def tearDownClass(cls):
    # Clean up temp directory and restore original working directory
    os.chdir(cls.original_cwd)
    cls.temp_dir.cleanup()

  def test_initialize_config_file_created(self):
    """ Test creation of config file. """
    _ = Config(self.config_path)
    self.assertTrue(os.path.exists(self.config_path))

  def test_load_config_from_existing_file(self):
    """ Test that the config is loaded correctly from an existing file. """
    with open(self.config_path, "w", encoding="utf-8") as f:
      json.dump({"ServerID": "test_server"}, f)
    config = Config(self.config_path)
    self.assertEqual(config["ServerID"], "test_server")

  def test_modify_and_save_config_value(self):
    """ Test that modifying a config value updates the file. """
    config = Config(self.config_path)
    config["ServerID"] = "new_server_id"

    # reload and check
    config = Config(self.config_path)
    self.assertEqual(config["ServerID"], "new_server_id")

  def test_delete_config_value(self):
    """ Test that deleting a config value updates the file. """
    config = Config(self.config_path)
    del config["ServerID"]

    # reload and check
    config = Config(self.config_path)
    self.assertNotIn("ServerID", config)

  def test_mutable_mapping_methods(self):
    """ Test MutableMapping methods. """
    config = Config()
    print(config)

    # __setitem__ and __getitem__
    config["NewKey"] = "NewValue"
    self.assertEqual(config["NewKey"], "NewValue")

    # __delitem__
    del config["NewKey"]
    with self.assertRaises(KeyError):
      _ = config["NewKey"]

    # __iter__ and __len__
    print(config)
    self.assertEqual(len(config), 5)
    expected_keys = {
      "ServerID", "ListenAddresses", "TimeOut", "SizeLimit",
      "AllowedIPAdddresses"
    }
    self.assertEqual(set(config), expected_keys)

  def test_write_config_to_json_filenotfounderror(self):
    """ Test FileNotFoundError is raised. """
    with mock.patch("config.open", side_effect=FileNotFoundError("Mocked FileNotFoundError.")), mock.patch("logging.Logger.error") as mock_error:
      _ = Config(self.config_path)
      mock_error.assert_called_with(
        "The configuration file was not found. Mocked FileNotFoundError.")

  def test_write_config_to_json_ioerror(self):
    """ Test IOError is raised. """
    config = Config(self.config_path)
    with mock.patch("config.open", side_effect=IOError("Mocked IOError.")), mock.patch("logging.Logger.error") as mock_error:
      config._write_config_to_json()
      mock_error.assert_called_with(
        "An error occured while writing the configuration file. Mocked IOError.")

  def test_config_invalid_json(self):
    """ Test handling of invalid JSON in the config file. """
    with open(self.config_path, "w", encoding="utf-8") as f:
      f.write("invalid json")
    with mock.patch("logging.Logger.error") as mock_error:
      _ = Config(self.config_path)
      mock_error.assert_called_once()

  def test_config_file_contents(self):
    """ Test all the config options are created. """
    config = Config()
    self.assertEqual(config["ServerID"], "it's me, your server")
    self.assertEqual(config["ListenAddresses"], ["*"])
    self.assertEqual(config["TimeOut"], 3)
    self.assertEqual(config["SizeLimit"], 1048576)
    self.assertEqual(config["AllowedIPAdddresses"], [
                     "10.0.0.0/24", "192.168.1.0/24"])
