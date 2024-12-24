import logging
import sys
import colorlog


def configure_logging():
  """ Configures the root logger with colored output. """

  handler = colorlog.StreamHandler()
  handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    log_colors={
      'DEBUG': 'cyan',
      'INFO': 'green',
      'WARNING': 'yellow',
      'ERROR': 'red',
      'CRITICAL': 'red,bg_white',
    },
  ))

  logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler]
  )
