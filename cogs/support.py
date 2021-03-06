import json

from discord import (Game, Status, Embed, 
    TextChannel, RawReactionActionEvent, Message, Role, Client)
from discord.ext import commands

from typer import Dict

from utils.data import DataController
from utils.logger import Logger

class Support(commands.Cog):

    def __init__(self, client):
        self.client: Client = client

        self.dataController: DataController = DataController()
        self.log: Logger = Logger()

    async def send_support_message(self, supportChannel: TextChannel) -> None:
        em: Embed = Embed(title=f"Welcome to the support department!", description=f"""To create ticket react with: :ticket: 

                Special text channel will be created after reacting which only you can see and administration.
                Describe your problem on this channel and we will try to solve it.

                
                Limit: 1 active ticket per user.
                """, color=0x00a8ff)

        message: Message = await supportChannel.send(embed=em)

        await message.add_reaction("🎫")
        await message.pin()

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        data: Dict[str, any] = await self.dataController.get_data()
        settings: Dict[str, any] = await self.dataController.get_settings()

        if message.channel.id in data['ticket-channel-ids']:
            await self.log.message(channel=message.channel, message=message)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("[*] Support module loaded successfuly")
        await self.client.wait_until_ready()

        data: Dict[str, any] = await self.dataController.get_data()
        settings: Dict[str, any] = await self.dataController.get_settings()
        
        try:
            supportChannel: TextChannel = self.client.get_channel(settings['channels']['support-channel-id'])
            if [msg async for msg in supportChannel.history()] == []:
                await self.send_support_message(supportChannel=supportChannel)
            else:
                async for message in supportChannel.history(limit=None):
                    if message.author.id != self.client.user.id:
                        await self.send_support_message(supportChannel=supportChannel)
                        await self.log.system(f"{self.client.user.name}// bot sent a initial message.")
                        break
        except FileExistsError:
            print("\x1b[1;31m[ERROR]:\x1b[0m Something went wrong, check logs/bot.log for more information.")
            await self.log.system(f"{self.client.user.name}// Invalid file configuration, please correct data.json ")
        await self.client.change_presence(activity=Game("Support"), status=Status.online)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent -> None):
        data: Dict[str, any] = await self.dataController.get_data()
        settings: Dict[str, any] = await self.dataController.get_settings()
        
        changed: bool = False
        if not payload.user_id == self.client.user.id:
            if payload.channel_id in data['ticket-channel-ids'] and payload.emoji.name == "❌":
                ticketChannel = self.client.get_channel(payload.channel_id)
                logChannel = self.client.get_channel(settings['channels']['support-log-channeld-id'])

                data['users-with-active-tickets'].remove(payload.member.id)
                data['ticket-channel-ids'].remove(payload.channel_id)

                await self.log.system(f"{self.client.user.name}// Ticket({ticketChannel.name}) has been closed by {payload.member.name}")

                if settings['enable-channel-logger']:
                    await self.log.channel(channel=logChannel, message=f"""User {payload.member.name} closed the ticket! channel name: {ticketChannel.name}""")
                
                changed = True
                await ticketChannel.delete()


            if payload.channel_id == settings['channels']['support-channel-id'] and payload.emoji.name == "🎫":
                if not payload.user_id in data['users-with-active-tickets']:
                    supportCategory = self.client.get_channel(settings['channels']['support-category-id'])
                    
                    data['ticket-id-counter'] += 1
                    ticketChannel = await supportCategory.create_text_channel(f"ticket#{data['ticket-id-counter']}-{payload.member.name}")

                    data['ticket-channel-ids'].append(ticketChannel.id)
                    data['users-with-active-tickets'].append(payload.member.id)

                    supportRole: Role = [r for r in supportCategory.guild.roles if r.name == settings['support-role']][0]

                    await supportCategory.set_permissions(supportCategory.guild.roles[0], send_messages=False, read_messages=False)
                    await supportCategory.set_permissions(payload.member, send_messages=True, read_messages=True)
                    await supportCategory.set_permissions(supportRole, send_messages=True, read_messages=True)
                    
                    em: Embed = Embed(title=f"New ticket from {payload.member.name}#{payload.member.discriminator}", 
                            description=f"""You just created a new ticket, please wait patiently! 
                                            Soon, {supportRole.mention} will respond to your ticker.
                                            
                                            To close ticket click on: :x:""", color=0x00a8ff)

                    message: Message = await ticketChannel.send(embed=em)

                    logChannel: TextChannel = self.client.get_channel(settings['channels']['support-log-channeld-id'])

                    await self.log.system(f"{self.client.user.name}// A new ticket has been submitted from {payload.member.name}.")

                    if settings['enable-channel-logger']:
                        await self.log.channel(channel=logChannel, message=f"""User {payload.member.name} created the ticket! channel name: {logChannel.name}""")

                    changed = True
                    await message.add_reaction("🎫") # \U0000274c
                    await message.pin()

            if changed:
                await self.dataController.save_data(data)

def setup(client):
    client.add_cog(Support(client))
