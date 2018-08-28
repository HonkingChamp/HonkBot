import discord
from discord.ext import commands
import random
import asyncio
import time
class MiscCogs:

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description="sends pics of kissing", brief="Inspired by KawaiiBot")
    async def kiss(self, ctx, member: discord.Member=None):
        kissingimgs=("https://saboteur365.files.wordpress.com/2015/05/gay-men-kissing-gif.gif","http://www.speakgif.com/wp-content/uploads/2015/09/gay-kissing-gay-animated-gif.gif","https://media.giphy.com/media/14isOPBgsN47cc/giphy.gif","http://imgur.com/WCQXqaV","https://queerty-prodweb.s3.amazonaws.com/wp/docs/2013/12/ken-duken-kostja-ullmann-kiss.gif","http://images.hellogiggles.com/uploads/2017/01/09034535/anigif_sub-buzz-13419-1483929242-9.gif","http://68.media.tumblr.com/51ed5b0265837a5d6c1d48407ba437ff/tumblr_olthpghe511sz8civo1_400.gif","http://68.media.tumblr.com/eaa70c9854021532eb4d57bd9c761563/tumblr_olqc5909vy1vp4whno4_r1_540.gif","http://68.media.tumblr.com/da2e54f94244552bed1ef69ff98c3700/tumblr_numjk67atg1rawmqbo1_400.gif","http://68.media.tumblr.com/2fa1e7b0e89ee04048e8c7387d5aedf1/tumblr_oiclabXQYw1u91sbso1_400.gif","http://68.media.tumblr.com/2b29da9b7e92c4010ef9a45782d320a5/tumblr_nte9mkPSNR1sxhdaxo2_540.gif","http://68.media.tumblr.com/0b8f8932bd6b0b293c37adbdb08a9478/tumblr_nz3gyfJ5sN1ued844o1_250.gif","http://68.media.tumblr.com/d1feb67865b2d4c5ffa500c3709d625f/tumblr_nuhltj50hN1rawmqbo1_400.gif")
        emb = discord.Embed(description=f"{member.display_name} has been kissed by {ctx.author.display_name}", colour=0xf805c3, set_image=random.choice(kissingimgs))
        await ctx.channel.send(embed=emb)

    @commands.command(description="Honk Honk", brief="Fuck you and the pizza")
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
            c = m.content.lower()
            return m.author == ctx.author and m.channel == ctx.channel and c == "rock" or m.author == ctx.author\
                and m.channel == ctx.channel and c == "paper" or m.author == ctx.author and \
                m.channel == ctx.channel and c == "scissors"

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
