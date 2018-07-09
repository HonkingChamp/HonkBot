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
    @command.command(hidden=True)
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
            return await ctx.send('Could not reload %s because of an error\n%s' % (name, e))

        await ctx.send('Reloaded {} in {:.0f}ms'.format(name, (time.perf_counter()-t)*1000))

    @command.command(hidden=True)
    @commands.is_owner()
    async def reload_all(self, ctx):
        t = time.time()
        self.bot._unload_cogs()
        errors = await self.bot.loop.run_in_executor(self.bot.threadpool, partial(self.bot._load_cogs, print_err=False))
        t = (time.time() - t) * 1000
        for error in errors:
            await ctx.send(error)
        await ctx.send('Reloaded all default cogs in {:.0f}ms'.format(t))

    @command.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog):
        cog_name = 'cogs.%s' % cog if not cog.startswith('cogs.') else cog
        t = time.perf_counter()
        try:
            await self.bot.loop.run_in_executor(self.bot.threadpool,
                                                self.bot.load_extension, cog_name)
        except Exception as e:
            return await ctx.send('Could not reload %s because of an error\n%s' % (cog_name, e))

        await ctx.send('Loaded {} in {:.0f}ms'.format(cog_name, (time.perf_counter() - t) * 1000))

    @command.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog):
        cog_name = 'cogs.%s' % cog if not cog.startswith('cogs.') else cog
        t = time.perf_counter()
        try:
            await self.bot.loop.run_in_executor(self.bot.threadpool,
                                                self.bot.unload_extension, cog_name)
        except Exception as e:
            return await ctx.send('Could not reload %s because of an error\n%s' % (cog_name, e))

        await ctx.send('Unloaded {} in {:.0f}ms'.format(cog_name, (time.perf_counter() - t) * 1000))

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
    async def shutdown(self, ctx):
        try:
            await ctx.send('Shutting down')
        except HTTPException:
            pass

        try:
            pending = asyncio.Task.all_tasks(loop=self.bot.loop)
            gathered = asyncio.gather(*pending, loop=self.bot.loop)
            try:
                gathered.cancel()
                self.bot.loop.run_until_complete(gathered)

                # we want to retrieve any exceptions to make sure that
                # they don't nag us about it being un-retrieved.
                gathered.exception()
            except:
                pass

        except:
            pass
        finally:
            await self.bot.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
     async def update_bot(self, ctx, *, options=None):
        """Does a git pull"""
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
            await ctx.send(f'Do you want to reload files `{"` `".join(files)}`')
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

def setup(bot):
    bot.add_cog(OwnerCog(bot))
