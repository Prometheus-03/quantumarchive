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
from paginator import *
from simplepaginator import SimplePaginator
from quantumutils import *
from dbwrapper import DB

def fromlevel(level):
    """Get XP needed to reach level"""
    return math.floor(7.02*level**2.13)
def fromxp(xp):
    """Get level from XP"""
    return math.floor(((xp+1)/7.02)**(1/2.13))
class Leveling(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.cooldown(rate=1,per=5)
    @commands.command(aliases=["getxp","rank"])
    async def level(self,ctx,*,author:discord.Member=None):
        '''Returns the XP you've earned'''
        if author==None:
            author=ctx.author
        rewards = {15: ctx.guild.get_role(663461450626367508), 25: ctx.guild.get_role(663461777576558594),
                   35: ctx.guild.get_role(663462503413579788), 45: ctx.guild.get_role(663462321078796289)}
        async with ctx.typing():
            db = DB("UserProfiles")
            db.set_collection("users")
            user = (await db.find(author_id=author.id))[0]
            if 'xp' in user.keys():
                xp = user['xp']
            else:
                xp = 0
            level = fromxp(xp)
            try:
                target = min(list(filter(lambda x:x>level,rewards.keys())))
                tar = f"Level {target}"
                tarlevel = f"{rewards[target].mention}"
                currind = (list(rewards.keys()).index(target)-1)
                xpleft = fromlevel(target) - xp
                if currind==-1:
                    cur = f"No level\nroles"
                else:
                    cur = f"{rewards[list(rewards.keys())[currind]].mention}"
            except ValueError:
                xpleft = "No more"
                tar = "None"
                tarlevel = "None"
                cur = f"{rewards[list(rewards.keys())[-1]].mention}"
            embed=discord.Embed(title=f"{author.name}'s XP",colour=author.colour)
            embed.set_thumbnail(url=author.avatar_url)
            embed.add_field(name="Level",value=f"Level {fromxp(xp)}")
            embed.add_field(name="Current level\nrole",value=cur)
            embed.add_field(name="XP",value=f"{xp} XP")
            embed.add_field(name="\u200b",value="\u200b",inline=False)
            embed.add_field(name="Next level\nw/ reward",value=tar)
            embed.add_field(name="Next level\nrole",value=tarlevel)
            embed.add_field(name="XP for\nnext role",value=f"{xpleft} XP")
            embed.add_field(name="\u200b",value="\u200b",inline=False)
            embed.add_field(name="XP progress\nto next level",value=f"{xp-fromlevel(level)}/{fromlevel(level+1)-fromlevel(level)} XP ({int(100*(xp-fromlevel(level))/(fromlevel(level+1)-fromlevel(level)))}%)")
            await ctx.send(embed=embed)

    @commands.cooldown(rate=1,per=7)
    @commands.group(aliases=["lb"])
    async def leaderboard(self,ctx):
        '''Checks the top users of the server by XP, top <number> returns the top <number> members'''
        if ctx.invoked_subcommand is not None:
            return
        users = []
        descs = []
        ranks = ["🥇", "🥈", "🥉", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", "🔟"]
        emb = discord.Embed(title="Server Leaderboard", colour=ctx.author.colour)
        async with ctx.typing():
            db = DB("UserProfiles")
            db.set_collection("users")
            for i in (await db.find()):
                if "xp" in i.keys() and ctx.guild.get_member(i["author_id"]) != None:
                    users.append([i["author_id"], i["xp"]])
            users.sort(key=lambda x: x[1], reverse=True)
            emb.set_footer(text=f"Total: {len(users)} members")
            if ctx.author.id not in [x[0] for x in users]:
                users = users[:10]
            else:
                n = [x[0] for x in users].index(ctx.author.id)
                emb.title+=f" (Your rank: {n+1})"
                if n < 5:
                    users = users[:9]
                elif n < 14:
                    users = users[n - 4:n + 5]
                    ranks = ranks[n - 4:] + list(map(str, range(11, n + 6)))
                elif n > (len(users) - 6):
                    ranks = list(map(str, range(len(users) - 9, len(users))))
                    users = users[-9:]
                else:
                    users = users[n - 4:n + 5]
                    ranks = list(range(n - 3, n + 6))
            for i in range(9):
                descs.append(
                    f"**{ranks[i]}** {ctx.guild.get_member(users[i][0]).mention} (**XP**: {users[i][1]} XP, **Level**: {fromxp(users[i][1])})")
            emb.description = "\n".join(descs)
        await ctx.send(embed=emb)

    @commands.cooldown(rate=1,per=5)
    @leaderboard.command()
    async def top(self,ctx,number:int=10):
        '''Get the top [number] members'''
        users = []
        descs = []
        ranks = ["🥇", "🥈", "🥉", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", "🔟"]
        emb = discord.Embed(title="Server Leaderboard", colour=ctx.author.colour)
        async with ctx.typing():
            db = DB("UserProfiles")
            db.set_collection("users")
            for i in (await db.find()):
                if "xp" in i.keys() and ctx.guild.get_member(i["author_id"])!=None:
                    users.append([i["author_id"], i["xp"]])
            users.sort(key=lambda x: x[1], reverse=True)
            emb.set_footer(text=f"Total: {len(users)} members")
            if number<10:
                number=10
            elif number>len(users):
                number=len(users)
            users = users[:number]
            def chunks(lst, n):
                """Yield successive n-sized chunks from lst."""
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]
            reorder = list(chunks(users,10))
            embs = []
            counter=0
            for k in reorder:
                descs=[]
                l = emb.copy()
                for i in range(len(k)):
                    descs.append(
                    f"**{ranks[i]}** {ctx.guild.get_member(users[10*counter+i][0]).mention} (**XP**: {users[10*counter+i][1]} XP, **Level**: {fromxp(users[10*counter+i][1])})")
                l.description = "\n".join(descs)
                embs.append(l)
                counter+=1
                if counter<len(reorder):
                    ranks.clear()
                    ranks.extend(list(map(str,range(10*counter+1,10*counter+1+len(reorder[counter])))))
            await SimplePaginator(extras=embs).paginate(ctx)

    @commands.check(important)
    @commands.command()
    async def setxp(self,ctx,xp:int,*,author:discord.Member=None):
        '''For the owner to set your XP, is for helping to migrate Gaius Play XP'''
        if author==None:
            author = ctx.author
        async with ctx.typing():
            db = DB("UserProfiles")
            db.set_collection("users")
            search = (await db.find(author_id=author.id))
            if search:
                await db.update(search[0]["_id"],xp=xp)
            else:
                await db.insert(author_id=author.id,xp=xp)
        await ctx.message.add_reaction("✅")

    @commands.cooldown(rate=1,per=7)
    @commands.command(aliases=["mbr","rankmembers"])
    async def membersbyrank(self,ctx):
        """For you to see which members are in a particular role rank"""
        choices = discord.Embed(title="Choose the level rank",colour=discord.Colour.dark_teal())
        rewards = {15: ctx.guild.get_role(663461450626367508), 25: ctx.guild.get_role(663461777576558594),
                   35: ctx.guild.get_role(663462503413579788), 45: ctx.guild.get_role(663462321078796289)}
        reactions = ["🇦","🇧","🇨","🇩"]
        choices.description="\n".join(reactions[i]+" "+list(rewards.values())[i].mention for i in range(len(rewards)))
        mes = await ctx.send(embed=choices)
        def checker(reaction,member):
            return (member.id==ctx.author.id) and (reaction.emoji in reactions) and (reaction.message.id==mes.id)
        try:
            for reaction in reactions:
                await mes.add_reaction(reaction)
            reaction, user = await self.bot.wait_for("reaction_add",timeout=15,check=checker)
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(title="No options chosen",description="Please choose a role",colour=discord.Colour.red()))
            return
        role = list(rewards.values())[reactions.index(reaction.emoji)]
        if role == list(rewards.values())[-1]:
            people = role.members
        else:
            people = list(set(role.members) - set(list(rewards.values())[reactions.index(reaction.emoji)+1].members))
        async with ctx.typing():
            db = DB("UserProfiles")
            db.set_collection("users")
            users = [(await db.find(author_id=i))[0] for i in list(map(lambda x:x.id, people))]
            users.sort(key=lambda x:x["xp"],reverse=True)
            message = "\n".join(f"**{i+1})** {ctx.guild.get_member(users[i]['author_id']).mention}: {users[i]['xp']} XP" for i in range(len(people)))
        await ctx.send(embed=discord.Embed(title=f"List of all {role.name} members",description=(message or "None so far"),colour=discord.Colour.dark_teal()))

def setup(bot):
    bot.add_cog(Leveling(bot))