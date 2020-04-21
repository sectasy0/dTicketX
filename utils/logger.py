from discord import TextChannel

from os import pardir
from os.path import abspath, join, dirname, realpath

from datetime import datetime

import asyncio

class Logger():
    def __init__(self):
        self.__workDirectory = abspath(join(dirname(realpath(__file__)), pardir, "logs/"))
        self.__systemLogsFile = join(self.__workDirectory, "bot.log")

    def __create_filename(self, member_name: str) -> str:
        return f"{datetime.now().strftime('%Y%m%d')}-{member_name}"

    async def message(self, target: str):
        if target != None:
            with open(self.__workDirectory+self.__create_filename(target), 'a+') as f:
                f.write(f"{datetime.now().strftime('%H:%M:%S')}/  {target}\n")

    async def system(self, message: str):
        if message != None:
            with open(self.__systemLogsFile, 'a+') as f:
                f.write(f"{datetime.now().strftime('%H:%M:%S')}/  {message}\n")

    async def channel(self, channel: TextChannel, message: str):
        pass
    