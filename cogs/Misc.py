import discord
from discord.ext import commands
import random
import asyncio
class MiscCogs:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Honk Honk", brief="Fuck you and your fucking black friends")
    async def honk(self, ctx):
         await ctx.channel.send("honk honk")

    @commands.command(description="Lol", brief="Random image about Google")
    async def whatisthis(self, ctx):
        my_files = ['C:/Users/Choong Jueen Mao/Downloads/Just Google It.jpg', ]
        with open(random.choice(my_files), 'rb') as fp:
            await ctx.channel.send(file=discord.File(fp))

    @commands.command(description="Gay stuff", brief="really gay stuff")
    async def mickygay(self, ctx):
        await ctx.channel.send("https://cdn.discordapp.com/attachments/297061271205838848/463864376630312960/IMG_20180501_215320.png")

    @commands.command(description="Repeats a message", brief="Repeating the message")
    async def echo(self, ctx, *, arg):
        await ctx.send(arg)

    @commands.command(description="plays a game", brief="Some rock paper scissors")
    async def rps(self, ctx):
        await ctx.channel.send("Let's play a simple game of rock paper scissors, type rock, scissors or paper to play")
        Rockpaperscissors = ["rock", "paper", "scissors"]
        b = random.choice(Rockpaperscissors)

        def pred(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            d = await self.bot.wait_for('message', check=pred, timeout=120)
            a = d.content.lower()
        except asyncio.TimeoutError:
            await ctx.channel.send('You took too long...')
        else:
            if (a == "rock" and b == "rock") or (a == "scissors" and b == "scissors") or (
                    a == "paper" and b == "paper"):
                await ctx.channel.send(f"I chose {b}.")
                await ctx.channel.send("It's a draw")
            elif (a == "rock" and b == "scissors") or (a == "scissors" and b == "paper") or (
                    a == "paper" and b == "rock"):
                await ctx.channel.send(f"I chose {b}.")
                await ctx.channel.send("OOF")
            elif (a == "rock" and b == "paper") or (a == "scissors" and b == "rock") or (
                    a == "paper" and b == "scissors"):
                await ctx.channel.send(f"I chose {b}.")
                await ctx.channel.send("FeelsGoodMan")

def setup(bot):
    bot.add_cog(MiscCogs(bot))