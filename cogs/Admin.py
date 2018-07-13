import discord
from discord.ext import commands
import asyncio
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

def setup(bot):
    bot.add_cog(AdminCogs(bot))
