import discord
import os

from keep_alive import keep_alive

TOKEN=os.getenv("TOKEN")
LOL_MENTION_ID=os.getenv("LOL_MENTION_ID")
SEVEN_OCLOCK_EMOJI=os.getenv("SEVEN_OCLOCK_EMOJI")
EIGHT_OCLOCK_EMOJI=os.getenv("EIGHT_OCLOCK_EMOJI")
NINE_OCLOCK_EMOJI=os.getenv("NINE_OCLOCK_EMOJI")
TEN_OCLOCK_EMOJI=os.getenv("TEN_OCLOCK_EMOJI")

def set_time(reaction):
    match reaction.emoji:
        case "🕖":
            return "19時"
        case "🕗":
            return "20時"
        case "🕘":
            return "21時"
        case "🕙":
            return "22時"
        case _:
            return ""

async def add_clock_reaction(message):
    await message.add_reaction(SEVEN_OCLOCK_EMOJI)
    await message.add_reaction(EIGHT_OCLOCK_EMOJI)
    await message.add_reaction(NINE_OCLOCK_EMOJI)
    await message.add_reaction(TEN_OCLOCK_EMOJI)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author.bot:
            return
        if not (message.role_mentions and message.role_mentions[0].id == int(LOL_MENTION_ID)):
            return
        if not ("カスタム" in message.content):
            return
        await add_clock_reaction(message=message)

    async def on_reaction_add(self, reaction, user):
        message = await reaction.message.fetch()
        if not message.role_mentions:
            return
        reactions = message.reactions

        msg_at = ""
        user_set = set()
        for reaction in reactions:
            _msg_at = set_time(reaction=reaction)
            count = 0
            async for user in reaction.users():
                user_set.add(user)
                count += 1
            if _msg_at and count > 1:
                msg_at = _msg_at
        if len(user_set) - 1 == 10:
            msg = f"{str(message.role_mentions[0].mention)}\n{msg_at}カスタム開催！！！！！！！！！！！！"
            await message.reply(msg)

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True

client = MyClient(intents=intents)
keep_alive()
client.run(TOKEN)
