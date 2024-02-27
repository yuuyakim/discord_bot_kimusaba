# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN=os.getenv("TOKEN")

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    async def on_reaction_add(self, reaction, user):
        message = await reaction.message.fetch()
        if not message.role_mentions:
            return
        channel = message.channel
        reactions = message.reactions
        reactions_count = 0
        for reaction in reactions:
            reactions_count += reaction.count
        if reactions_count == 4:
            msg = f"{str(message.role_mentions[0].mention)}\n \
            \n スタンプありがとう！ \n This is test message"
            await channel.send(msg)

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

client = MyClient(intents=intents)
client.run(TOKEN)
