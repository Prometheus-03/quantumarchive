from discord.ext import commands
import discord
import inspect
import re
import io
import contextlib
import traceback
import urllib.request
import urllib.parse
import math
import random
import time
import datetime

import quantumutils
from paginator import *
from simplepaginator import SimplePaginator
import quantumutils as utils
from dbwrapper import DB


tzs = {
    'UTC−12:00': -12.0,
    'UTC−11:00': -11.0,
    'UTC−10:00': -10.0,
    'UTC−09:30': -9.5,
    'UTC−09:00': -9.0,
    'UTC−08:00': -8.0,
    'UTC−07:00': -7.0,
    'UTC−06:00': -6.0,
    'UTC−05:00': -5.0,
    'UTC−04:00': -4.0,
    'UTC−03:30': -3.5,
    'UTC−03:00': -3.0,
    'UTC−02:00': -2.0,
    'UTC−01:00': -1.0,
    'UTC±00:00': 0.0,
    'UTC+01:00': 1.0,
    'UTC+02:00': 2.0,
    'UTC+03:00': 3.0,
    'UTC+03:30': 3.5,
    'UTC+04:00': 4.0,
    'UTC+04:30': 4.5,
    'UTC+05:00': 5.0,
    'UTC+05:30': 5.5,
    'UTC+05:45': 5.75,
    'UTC+06:00': 6.0,
    'UTC+06:30': 6.5,
    'UTC+07:00': 7.0,
    'UTC+08:00': 8.0,
    'UTC+08:45': 8.75,
    'UTC+09:00': 9.0,
    'UTC+09:30': 9.5,
    'UTC+10:00': 10.0,
    'UTC+10:30': 10.5,
    'UTC+11:00': 11.0,
    'UTC+12:00': 12.0,
    'UTC+12:45': 12.75,
    'UTC+13:00': 13.0,
    'UTC+14:00': 14.0,
}


class Time(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.group(invoke_without_command=True)
    async def time(self,ctx,number:int=None):
        '''Choose your timezone and get the time there. Add 'set' behind to set your timezone and 'mine' to check your local time'''
        if number is None or number not in list(range(1,len(tzs)+1)):
            m = quantumutils.partition(list(tzs.keys()),10)
            pages = []
            counter=0
            for i in m:
                text = "**Choose your timezone by typing the corresponding option number.**\n"
                text += "\n".join(["`("+str(10*counter+k+1)+") "+i[k]+"`" for k in range(len(i))])
                pages.append(text)
                counter+=1
            embeds = [discord.Embed(title=f"Make your selection: (Page {i}/{len(m)})",description=pages[i-1]) for i in range(1,len(m)+1)]
            await SimplePaginator(extras=embeds).paginate(ctx)

            #now asking user input
            try:
                def checker(m):
                    return m.content in list(map(str,range(1,len(tzs)+1))) and m.author.id==ctx.author.id and m.channel==ctx.channel
                mes = await self.bot.wait_for('message',check=checker,timeout=20)
                tn = int(str(mes.content))-1
                tz = list(tzs.keys())[tn]
                tzoffset = tzs[tz]
            except:
                await ctx.send("No valid timezone selected. Defaulting to 'UTC±00:00'")
                tz = 'UTC±00:00'
                tzoffset = tzs[tz]
        else:
            tz = list(tzs.keys())[number-1]
            tzoffset = tzs[tz]
        now = datetime.datetime.utcnow()
        now += datetime.timedelta(hours=tzoffset)
        emb = discord.Embed(
            title=f"Time in {tz}",colour=discord.Colour.dark_gold())
        emb.set_author(name="Time now")
        emb.add_field(name="Date", value=now.strftime("%a, %d %B %Y"))
        emb.add_field(name="Time", value=now.strftime("%H:%M:%S"), inline=False)
        await ctx.send(embed=emb)

    @time.command()
    @commands.cooldown(rate=1,per=7)
    async def set(self,ctx):
        '''Set your own timezone'''
        m = quantumutils.partition(list(tzs.keys()), 10)
        pages = []
        counter = 0
        for i in m:
            text = "**Choose your timezone by typing the corresponding option number.\n**"
            text += "\n".join(["`(" + str(10 * counter + k + 1) + ") " + i[k] + "`" for k in range(len(i))])
            pages.append(text)
            counter += 1
        embeds = [discord.Embed(title=f"Make your selection: (Page {i}/{len(m)})", description=pages[i - 1]) for i in
                  range(1, len(m) + 1)]
        await SimplePaginator(extras=embeds).paginate(ctx)

        # now asking user input
        try:
            def checker(m):
                return m.content in list(
                    map(str, range(1, len(tzs) + 1))) and m.author.id == ctx.author.id and m.channel == ctx.channel

            mes = await self.bot.wait_for('message', check=checker, timeout=20)
            tn = int(str(mes.content)) - 1
            tz = list(tzs.keys())[tn]
            tzoffset = tzs[tz]
        except:
            await ctx.send("❌| No valid timezone selected. Please try again.",delete_after=5)
            return
        db = DB("UserProfiles")
        db.set_collection("users")
        user = await db.find(author_id=ctx.author.id)
        if not user:
            await db.insert(author_id=ctx.author.id,tzoffset=tzoffset)
        else:
            await db.update(user[0]["_id"],tzoffset=tzoffset)
        await ctx.send(f"✅| {ctx.author.mention}, your timezone information has been set!",delete_after=5)

    @time.command()
    @commands.cooldown(rate=1,per=7)
    async def mine(self,ctx):
        '''Get your local time'''
        db = DB("UserProfiles")
        db.set_collection("users")
        user = await db.find(author_id=ctx.author.id)
        if (not user) or ("tzoffset" not in user[0].keys()):
            await ctx.send(embed=discord.Embed(title="Your timezone has not been set!",
                                               description="It seems that your timezone has not been set. Use `k!time set` to set your timezone.",
                                               colour=discord.Colour.red()))
        else:
            tz = user[0]["tzoffset"]
            offset = {v: k for k,v in tzs.items()}[tz]
        now = datetime.datetime.utcnow()
        now += datetime.timedelta(hours=tz)
        emb = discord.Embed(
            title=f"Time in {offset}", colour=discord.Colour.dark_gold())
        emb.set_author(name="Time now")
        emb.add_field(name="Date", value=now.strftime("%a, %d %B %Y"))
        emb.add_field(name="Time", value=now.strftime("%H:%M:%S"), inline=False)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Time(bot))