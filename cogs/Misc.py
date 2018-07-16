import discord
from discord.ext import commands
import random
import asyncio
import time
class MiscCogs:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Honk Honk", brief="Fuck you and your fucking black friends")
    async def honk(self, ctx):
         await ctx.channel.send("honk honk")

    @commands.command(description="Lol", brief="Random image about Google")
    async def whatisthis(self, ctx):
        await ctx.channel.send("https://imgur.com/gallery/QeC5uC2")

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
            if a==b:
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
                
                
    @commands.command(description="Checks ping", brief="Check ping")
    async def ping(self, ctx):
        t = time.perf_counter()
        await ctx.trigger_typing()
        t = time.perf_counter() - t
        emb = discord.Embed(description='Pong!\ntook {:.0f}ms'.format(t*1000), colour=0xa15606)
        await ctx.channel.send(embed=emb)

def setup(bot):
    bot.add_cog(MiscCogs(bot))
