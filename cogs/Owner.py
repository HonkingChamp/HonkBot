import discord
import re
from discord.ext import commands
import shlex
import subprocess
from concurrent.futures import ThreadPoolExecutor
import importlib
import time


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
            await ctx.send(f'**```ERROR: {type(e).__name__} - {e}```**')
        else:
            await ctx.send('**```SUCCESS```**')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**```ERROR: {type(e).__name__} - {e}```**')
        else:
            await ctx.send('**```SUCCESS```**')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, name):
        t = time.perf_counter()
        try:
            cog_name = 'cogs.%s' % name if not name.startswith('cogs.') else name

            def unload_load():
                self.bot.unload_extension(cog_name)
                self.bot.load_extension(cog_name)

            await self.bot.loop.run_in_executor(self.bot.threadpool, unload_load)
        except Exception as e:
            await ctx.send('``Could not reload %s because of an error\n%s``' % (name, e))
        else:
            await ctx.send('``Reloaded {} in {:.0f}ms``'.format(name, (time.perf_counter() - t) * 1000))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def leave(self, ctx, guild=None):
        if guild is None:
            await ctx.guild.leave()
        else:
            toleave = self.bot.get_guild(int(guild))
            await toleave.leave()
            await ctx.channel.send(f"I left {toleave.name}")



    @commands.command(hidden=True)
    @commands.is_owner()
    async def update_bot(self, ctx, *, options=None):
        cmd = 'git pull'.split(' ')
        if options:
            cmd.extend(shlex.split(options))

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = await self.bot.loop.run_in_executor(self.bot.threadpool, p.communicate)
        out = out.decode('utf-8')
        if err:
            out = err.decode('utf-8') + out

        files = re.findall(r'(cogs/\w+)(?:.py *|)', out)

        if len(out) > 2000:
            out = out[:1996] + '...'

        await ctx.send(out)

        if files:
            files = [f.replace('/', '.') for f in files]
            def do_reload():
                messages = []
                for file in files:
                    try:
                        self.bot.unload_extension(file)
                        self.bot.load_extension(file)
                    except Exception as e:
                        messages.append('Failed to load extension {}\n{}: {}'.format(file, type(e).__name__, e))
                    else:
                        messages.append(f'Reloaded {file}')
                return messages
            messages = await self.bot.loop.run_in_executor(self.bot.threadpool, do_reload)
            if messages:
                await ctx.send('\n'.join(messages))
           
    @commands.command(hidden=True)
    @commands.is_owner()
    async def serverlist(self, ctx):
        servers = list(self.bot.guilds)
        await ctx.channel.send("Connected on " + str(len(self.bot.guilds)) + " servers:")
        for x in range(len(servers)):
            await ctx.channel.send(f'{servers[x].name}')
            await ctx.channel.send(f'{servers[x].id}')
            
    @commands.command(hidden=True)
    @commands.is_owner()
    async def status(self, ctx, *args):
        stat = ' '.join(args)
        await self.bot.change_presence(game=discord.Game(name=stat))
        emb = discord.Embed(description=f"{ctx.author.name} has changed my status to {stat}", colour=0xa15606)
        await ctx.channel.send(embed=emb)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
