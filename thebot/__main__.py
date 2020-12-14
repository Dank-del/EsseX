from pyrogram import  idle, Client
from thebot import dankbot
from thebot.modules import ALL_MODULES

import importlib

for module in ALL_MODULES:
    imported_module = importlib.import_module("thebot.modules." + module)
    importlib.reload(imported_module)


if __name__ == "__main__":
    dankbot.start()
    idle()
