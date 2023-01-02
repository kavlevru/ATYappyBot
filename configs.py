import importlib
import os
import sys


def load_conf():
    conf_name = os.environ.get("BOT_ENV")
    if conf_name is None:
        conf_name = "production"å
    try:
        return importlib.import_module(f"configs.{conf_name}")
    except (TypeError, ValueError, ImportError):
        print(f"Invalid config \"{conf_name}\"")
        sys.exit(1)
