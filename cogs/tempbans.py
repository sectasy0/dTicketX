from discord.ext import commands

from discord import Member, Client
from utils.tempbans import BansDataController

from typing import Dict

class TempBans(commands.Cog):

    def __init__(self, client):
        self.client: Client = client

        self.bans: Dict[str, any] = BansDataController().get_bans()
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("[*] Tempbans module loaded successfuly")

    @commands.command(name='tempban')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: Member, minutes=10) -> None:
        print(f"{member} {minutes}")

def setup(client) -> None:
    client.add_cog(TempBans(client))
