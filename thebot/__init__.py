import os
import sys
import time
import logging
from thebot.config import Config
from pyrogram import Client, errors

API_ID = Config.API_ID
API_HASH = Config.API_HASH
TOKEN = Config.TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    handlers=[logging.StreamHandler()]
)
LOGS = logging.getLogger(__name__)

dankbot = Client('dank', api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
