import asyncio
import importlib
import sys
import time
import traceback
import logging
from pyrogram import  idle, Client
from thebot import dankbot
from thebot.modules import start, anilist, help, dev

dankbot.start()
idle()
