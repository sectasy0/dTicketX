from discord.ext import commands

from discord import Member
from utils.tempbans import BansDataController

class TempBans(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.bans = BansDataController().get_bans()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("[*] Tempbans module loaded successfuly")

    @commands.command(name='tempban')
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: Member, minutes=10):
        print(f"{member} {minutes}")

def setup(client):
    client.add_cog(TempBans(client))