import discord
import json
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor
import sys, traceback

initial_extensions = ['cogs.Owner',
                      'cogs.Admin',
                      'cogs.Misc']

bot = commands.Bot(command_prefix="?", description='Cogs')
bot.threadpool = ThreadPoolExecutor(max_workers=2)
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(activity=discord.Game(name='Fuck Rice'))
        servers = list(bot.guilds)
        print("Connected on " + str(len(bot.guilds)) + " servers:")
        for x in range(len(servers)):
            print('  ' + servers[x].name)
@bot.event
async def on_message_delete(message):
    fmt = '{0.author.name} has deleted the message:\n{0.content}'
    print(fmt.format(message))

@bot.event
async def on_message(message: discord.Message):
    if message.content.startswith("Spain") and message.author != bot.user:
        a = await message.channel.send("Russia trashed Spain")
        msg = await message.channel.send('Nerea rart')
        await msg.delete()
        await a.delete()
    bob = message.content.lower()
    if "micky" in bob and "gay" in bob or "mickygay" in bob:
        emb = discord.Embed(description="I will fuck her and the pizza", colour=0xa15606)
        emb.set_author(name="Micky", icon_url="https://pbs.twimg.com/media/DahxOugU0AAQ4eM.jpg")
        emb.set_image(url="https://cdn.discordapp.com/attachments/297061271205838848/463864376630312960/IMG_20180501_215320.png")
        await message.channel.send(embed=emb)
    await bot.process_commands(message)

with open('config.json') as f:
    config = json.load(f)
bot.run(config['token'], bot=True, reconnect=True)
