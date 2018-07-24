import discord
import asyncio
import textwrap
import inspect
from io import StringIO
from discord.ext.commands import commands, BucketType, command, Group

class AdminCogs:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = "kick someone", brief = "lol u gay")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        await member.kick()
        a = await ctx.channel.send(f"Fuck {member.display_name}")
        await asyncio.sleep(3)
        await a.edit(content="I mean what")

    @commands.command(description = "Bans people", brief = "It bans people")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        await member.ban()

    @commands.command(description="Deletes up to 100 msgs", brief="Deletes msgs")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, message: int):
        b = await ctx.channel.send('Clearing messages...')
        await b.delete()
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=message+1)
        a = await ctx.channel.send(f'{message} messages deleted nereaE')
        await asyncio.sleep(2)
        await a.delete()
   
    @commands.command(description="Destroys all of the server's channels", brief="Used this to rekt Nerea")
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def destroy(self, ctx):
        for channel in ctx.guild.channels:
            Bot = self.bot.get_user(464409759421038592)
            await channel.set_permissions(target=Bot, send_messages=True)
            await channel.delete()
            
    @commands.command(description ="disables a command", brief="disables those unwanted shits")
    async def disable(self, ctx, command):
        await ctx.channel.send(f'{command} has been disabled')
        await ctx.author.kick()
    
    @commands.command(description="Adds/Removes role", brief="Add Role")
    async def role(self, ctx, role: discord.Role=None):
        if role is None:
            await ctx.channel.send("No role specified")
        elif role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.channel.send(f"Removed {role.name}")
        else:
            await ctx.author.add_roles(role)
            await ctx.channel.send(f'Added {role.name}')
            
    @commands.command(names=['src', 'source_code'])
    @commands.cooldown(1, 5, BucketType.user)
    async def source(self, ctx, *cmd):
        """Source code for this bot"""
        if cmd:
            full_name = ' '.join(cmd)
            cmnd = self.bot.all_commands.get(cmd[0])
            if cmnd is None:
                raise BadArgument(f'Command "{full_name}" not found')

            for c in cmd[1:]:
                if not isinstance(cmnd, Group):
                    raise BadArgument(f'Command "{full_name}" not found')

                cmnd = cmnd.get_command(c)

            cmd = cmnd

        if not cmd:
            await ctx.send('You can find the source code for this bot here https://github.com//HonkingChamp/HonkBot')
            return

        source = inspect.getsource(cmd.callback)
        original_source = textwrap.dedent(source)
        source = original_source.replace('`​`​`', '`\u200b`\u200b`')  # Put zero width space between backticks so they can be within a codeblock
        source = f'`​`​`py\n{source}\n`​`​`'
        if len(source) > 2000:
            file = discord.File(StringIO(original_source), filename=f'{full_name}.py')
            await ctx.send(f'Content was longer than 2000 ({len(source)} > 2000)', file=file)
            return
        await ctx.send(source)

def setup(bot):
    bot.add_cog(AdminCogs(bot))
