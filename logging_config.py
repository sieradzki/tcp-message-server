import logging
import sys


def configure_logging():
  """ Configures the root logger. """

  logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    handlers=[logging.StreamHandler(sys.stdout)]
  )
