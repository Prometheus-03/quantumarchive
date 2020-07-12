from discord.ext import commands
import discord
import inspect
import re
import io
import contextlib
import traceback
import urllib.request
import urllib.parse
import humanfriendly
import math
import random
import time
import datetime
from paginator import *
from simplepaginator import SimplePaginator
import quantumutils as utils

class Info(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(name='help')
    async def _help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send("```"+"\n".join(traceback.format_exception(None, e, e.__traceback__))+"```")

    @commands.command()
    async def ping(self, ctx):
        '''checks the time taken for the bot to respond'''
        start = time.monotonic()
        msg = await ctx.send("Pinging... 🕒")
        millis = (time.monotonic() - start) * 1000
        heartbeat = ctx.bot.latency * 1000
        await msg.edit(content=f'Heartbeat: {heartbeat:,.2f}ms Response: {millis:,.2f}ms. ⏲️')

    @commands.command()
    async def perms(self,ctx,channel:discord.TextChannel=None,*,user:discord.Member=None):
        "checks permissions of member "
        if user is None:
            user=ctx.author
        if channel is None:
            channel=ctx.channel
        a = user.permissions_in(channel)
        out = []
        for m in sorted(a.VALID_FLAGS.keys()):
            if m[0] != "_":
                out.append(m+": "+("✅" if eval("a." + m) else "❌"))
        emb = discord.Embed(title=f"{user.name} permissions")
        emb.add_field(name=f"Channel: {channel.name}",value="\n".join(out))
        await ctx.send(embed=emb)

    @commands.command(aliases=["av"])
    async def avatar(self,ctx,user:discord.Member=None):
        """To get the user's avatar"""
        if user is None:
            user=ctx.author
        emb = discord.Embed(title=f"{user.display_name}'s Avatar",colour=discord.Colour.dark_gold())
        emb.set_image(url=user.avatar_url)
        await ctx.send(embed=emb)

    @commands.command()
    async def profile(self,ctx,user:discord.Member=None):
        """Get to know more about yourself"""
        if user is None:
            user = ctx.author
        embed = discord.Embed(title=user.name+"#"+user.discriminator)
        embed.colour=ctx.guild.get_member(user.id).colour
        embed.set_thumbnail(url=user.avatar_url)
        embed.description="[Avatar]("+str(user.avatar_url)+")"
        embed.add_field(name="Roles",value=" ".join([i.mention for i in user.roles[1:][::-1]]))
        mempluscreate = [(i,i.created_at) for i in ctx.guild.members]
        mempluscreate.sort(key=lambda x:x[1])
        members = [k[0].id for k in mempluscreate]
        position = 1+members.index(user.id)
        if (position==1):
            position=""
        elif (position not in [11,12,13]) and (position%10 in [1,2,3]):
            position=str(position)+["","st ","nd "+"rd "][position%10]
        else:
            position=str(position)+"th "
        createmessage=user.created_at.strftime("%a, %d %B %Y, at %H:%M:%S UTC")+"\n"
        createmessage+=f"({humanfriendly.format_timespan(humanfriendly.coerce_seconds(datetime.datetime.now()-user.created_at))} ago)"+"\n"
        createmessage+=position+"Oldest account on this server."
        embed.add_field(name="Creation date",value=createmessage)
        joinmessage=user.joined_at.strftime("%a, %d %B %Y, at %H:%M:%S UTC")+"\n"
        joinmessage += f"({humanfriendly.format_timespan(humanfriendly.coerce_seconds(datetime.datetime.now() - user.joined_at))} ago)" + "\n"
        joinmessage+=f"{humanfriendly.format_timespan(humanfriendly.coerce_seconds(user.joined_at-ctx.guild.created_at))} after the server was created."
        embed.add_field(name="Join date",value=joinmessage)
        embed.set_footer(text="User ID: {}".format(user.id))
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        '''Returns info about the bot'''
        emb = discord.Embed(colour=discord.Colour.teal(),title="Bot Information",description="**Creator**: Napoleon Bonaparte\n**Library**: discord.py")
        emb.set_footer(text="Made for the KhAnubis discord server")
        emb.set_image(url="https://cdn.discordapp.com/avatars/720216361397387284/fbe88a7770951aab62aec9b5f10384a2.png?size=128")
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Info(bot))
