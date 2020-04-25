from discord import TextChannel, Embed, Message

from os import pardir
from os.path import abspath, join, dirname, realpath

from datetime import datetime

import asyncio

class Logger():
    def __init__(self):
        self.__workDirectory = abspath(join(dirname(realpath(__file__)), pardir, "logs/"))
        self.__systemLogsFile = join(self.__workDirectory, "bot.log")

    def __create_filename(self, member_name: str) -> str:
        return f"{datetime.now().strftime('%Y%m%d')}{member_name}"

    async def message(self, channel: TextChannel, message: Message):
        if channel != None and message != None:
            with open(join(self.__workDirectory, self.__create_filename(channel.name)), 'a+') as f:
                f.write(f"{datetime.now().strftime('%H:%M:%S')}/  {message.author}: {message.content}\n")

    async def system(self, message: str):
        if message != None:
            with open(self.__systemLogsFile, 'a+') as f:
                f.write(f"{datetime.now().strftime('%H:%M:%S')}/   {message}\n")

    async def channel(self, channel: TextChannel, message: str):
        if channel != None:
            await channel.send(f"{datetime.now().strftime('%H:%M:%S')}/   {message}\n")

    