import json

from discord import (Game, Status, Embed, 
    TextChannel, RawReactionActionEvent)
from discord.ext import commands


from utils.data import DataController
from utils.logger import Logger

class Support(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.dataController = DataController()
        self.log = Logger()

    async def send_support_message(self, supportChannel: TextChannel):
        em = Embed(title=f"Welcome to the support department!", description=f"""To create ticket react with: :ticket: 

                Special text channel will be created after reacting which only you can see and administration.
                Describe your problem on this channel and we will try to solve it.

                
                Limit: 1 active ticket per user.
                """, color=0x00a8ff)

        message = await supportChannel.send(embed=em)

        await message.add_reaction("🎫")
        await message.pin()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        data = await self.dataController.get_data()
        settings = await self.dataController.get_settings()
        
        try:
            supportChannel = self.client.get_channel(settings['channels']['support-channel-id'])
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
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        data = await self.dataController.get_data()
        settings = await self.dataController.get_settings()

        if not payload.user_id == self.client.user.id:
            if payload.channel_id in data['ticket-channel-ids'] and payload.emoji.name == "❌":
                ticketChannel = self.client.get_channel(payload.channel_id)

                data['users-with-active-tickets'].remove(payload.member.id)
                data['ticket-channel-ids'].remove(payload.channel_id)

                await self.log.system(f"{self.client.user.name}// Ticket({ticketChannel.name}) has been closed by {payload.member.name}")
                await ticketChannel.delete()


            if payload.channel_id ==  settings['channels']['support-channel-id'] and payload.emoji.name == "🎫":
                if not payload.user_id in data['users-with-active-tickets']:
                    supportCategory = self.client.get_channel(settings['channels']['support-category-id'])
                    
                    if not payload.member.id in data['ticket-channel-ids']:
                            data['ticket-id-counter'] += 1
                            ticketChannel = await supportCategory.create_text_channel(f"ticket#{data['ticket-id-counter']}-{payload.member.name}")

                            data['ticket-channel-ids'].append(ticketChannel.id)
                            data['users-with-active-tickets'].append(payload.member.id)

                            supportRole = [r for r in supportCategory.guild.roles if r.name == settings['support-role']][0]

                            await supportCategory.set_permissions(supportCategory.guild.roles[0], send_messages=False, read_messages=False)
                            await supportCategory.set_permissions(payload.member, send_messages=True, read_messages=True)
                            await supportCategory.set_permissions(supportRole, send_messages=True, read_messages=True)
                            
                            em = Embed(title=f"New ticket from {payload.member.name}#{payload.member.discriminator}", 
                                    description=f"""You just created a new ticket, please wait patiently! 
                                                    Soon, {supportRole.mention} will respond to your ticker.
                                                    
                                                    To close ticket click on: :x:""", color=0x00a8ff)

                            message = await ticketChannel.send(embed=em)

                            await self.log.system(f"{self.client.user.name}// A new ticket has been submitted from {payload.member.name}.")
                            await message.add_reaction("\U0000274c")
                            await message.pin()

            await self.dataController.save_data(data)

def setup(client):
    client.add_cog(Support(client))