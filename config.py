import logging
import importlib
import os
import sys


def load_conf():
    conf_name = os.environ.get("BOT_ENV")
    if conf_name is None:
        conf_name = "production"
    try:
        conf = importlib.import_module("configs.{}".format(conf_name))
        logging.info(f"Load configuration '{conf_name}' - OK")
        return conf
    except (TypeError, ValueError, ImportError):
        print(f"Invalid config \"{conf_name}\"")
        sys.exit(1)
