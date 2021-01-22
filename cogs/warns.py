from discord.ext import commands, tasks
from discord import Embed, Member

from utils.data import DataController
from utils.logger import Logger
from utils.tempbans import Ban

from typing import Dict


class Warns(commands.Cog):
    def __init__(self, client):
        self.client: Client = client

        self.dataController = DataController()
        self.log: Logger = Logger()
        self.ban: Ban = Ban()

    async def on_ready(self) -> None:
        print("[*] Warns module loaded successfuly")

    async def add_warn(self, ctx, warnsValue: int, userName: str, reason: str) -> None:
        em: Embed = Embed(title=f"Warn!", description=f"""
                User: {userName}
                Received a warn ({warnsValue}/3) from {ctx.message.author}
                Reason: {reason} """, color=0x00a8ff)
        await ctx.send(embed=em)
        await self.log.system(f"{userName} has been warned by {ctx.message.author}, reason: {str(reason.encode('utf-8'))[2:-1]}")

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: Member, *reason) -> None:
        data: Dict[str, any] = await self.dataController.get_data()
        settings: Dict[str, any] = await self.dataController.get_settings()

        if not member.guild_permissions.administrator:
            if str(member.id) in data['warns']:
                data['warns'][str(member.id)] += 1

                await self.add_warn(ctx=ctx,warnsValue=data['warns'][str(member.id)],
                            userName=member.name, reason=str(" ".join(reason)))

                
                if data['warns'][str(member.id)] >= int(settings['warns']['max-warns']) and settings['warns']['ban-warns-reach']:
                    await self.ban.temp(client=self.client, member=member, admin=self.client.user.name, 
                                reason="Warn limit reached", time=int(settings['warns']['ban-time']))
                    await self.log.system(f"{member.name} was temporarily banned, reason: Warns limit reached")
                    data['warns'][str(member.id)] = 0
                    
            else:
                data['warns'].update({str(member.id): 1})
                await self.add_warn(ctx=ctx, warnsValue=data['warns'][str(member.id)], 
                            userName=member.name, reason=str(" ".join(reason)))

            await self.dataController.save_data(data)
        else:
            await ctx.send("You are not permitted to perform this operation")

def setup(client) -> None:
    client.add_cog(Warns(client))        
