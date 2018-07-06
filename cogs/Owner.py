import discord
import re
import shlex
import subprocess
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx):
        await ctx.guild.leave()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update_bot(self, ctx, *, options=None):
        """Does a git pull"""
        cmd = 'git pull'.split(' ')
        self.bot.threadpool = ThreadPoolExecutor(max_workers=2)
        if options:
            cmd.extend(shlex.split(options))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = await self.bot.loop.run_in_executor(self.bot.threadpool, p.communicate)
        out = out.decode('utf-8')
        if err:
            out = err.decode('utf-8') + out

        if len(out) > 2000:
            out = out[:1996] + '...'

        await ctx.send(out)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
