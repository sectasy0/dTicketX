from discord import Client
from discord.ext import commands, tasks
from datetime import datetime
from dateutil import parser
import asyncio

from utils.tempbans import BansDataController
from utils.data import DataController
from utils.logger import Logger


class Worker(commands.Cog):
    def __init__(self, client):
        self.client: Client = client

        self.bansData: BansDataController = BansDataController()
        self.data: DataController = DataController()
        self.log: Logger = Logger()

        self.unban.start()
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("[*] Workers module loaded successfuly")

    async def _get_bans(self, bans: dict):
        for ban in bans['list']:
            yield bans['list'][ban]

    @tasks.loop(minutes=8)
    async def unban(self) -> None:
        await self.client.wait_until_ready()

        bans = await self.bansData.get_bans()
        settings = await self.data.get_settings()

        changed = False
        async for ban in self._get_bans(bans):
            if ban['active']:
                if datetime.now() > parser.parse(ban['unban-date']):
                    channel = self.client.get_channel(settings['channels']['support-channel-id'])
                    Member = await self.client.fetch_user(ban['member-id'])
                    
                    await channel.guild.unban(Member)

                    ban['active'] = False
                    changed = True
        
        if changed:
            await self.bansData.save(bans)


def setup(client) -> None:
    client.add_cog(Worker(client)) 
