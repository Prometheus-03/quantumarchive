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
import quantumutils as utils

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def roll(self,ctx):
        '''Roll the dice, get the output'''
        ops = {
            1:"⚀ One",
            2:"⚁ Two",
            3:"⚂ Three",
            4:"⚃ Four",
            5:"⚄ Five",
            6:"⚅ Six"
        }
        op = random.randint(1,6)
        emb = embed=discord.Embed(title="Dice Rolled",colour=ctx.author.colour)
        emb.add_field(name="The output",value=ops[op])
        await ctx.send(embed=emb)

    @commands.command(aliases=["m8b","eightball"])
    async def magic8ball(self, ctx, *, message="Can I ask something?"):
        '''The answers to your questions, take the responses with a grain of salt though'''
        responses =  ["As I see it, yes.","Ask again later.","Better not tell you now.","Cannot predict now.",
                      "Concentrate and ask again.","Don’t count on it.","It is certain.","It is decidedly so.",
                      "Most likely.","My reply is no.","My sources say no.","Outlook not so good.",
                      "Outlook good.","Reply hazy, try again.","Signs point to yes.","Very doubtful.",
                      "Without a doubt.","Yes.","Yes – definitely.","You may rely on it."]
        response = random.choice(responses)
        embed = discord.Embed(title=message,description=response,colour=discord.Colour.from_rgb(random.randint(0, 255),
                            random.randint(0, 255),random.randint(0, 255)))
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name+" asks:")
        await ctx.send(embed=embed)

    @commands.command()
    async def rps(self, ctx, number=1):
        '''The classic rock-paper-scissors game, play at most 10 rounds'''
        s = "✂"
        p = "📄"
        r = list(filter(lambda x:x.name=="stone",ctx.guild.emojis))[0]
        emb = discord.Embed(title="Rock Paper Scissors match!",description="Round 1: Make your choice",colour=discord.Colour.light_grey())
        mes = await ctx.send(embed=emb)
        you = 0
        bot = 0
        try:
            number=int(number)
        except:
            number=1
        if number==0:number=1
        elif number<0:number=abs(number)
        if number>10:number=10
        for round in range(1,number+1):
            for i in [r,p,s]:
                await mes.add_reaction(i)
            def valid(reaction,user):
                return user.id==ctx.author.id and reaction.emoji in [r,p,s] and reaction.message.id==mes.id
            try:
                reaction , user = await self.bot.wait_for("reaction_add",timeout=10,check=valid)
                choice = [r,p,s].index(reaction.emoji)
                bchoice= random.randint(0,2)
                if choice==bchoice:
                    message="It's a draw! Better luck next time!"
                    col = discord.Colour.gold()
                elif (choice+1)%3==bchoice:
                    bot+=1
                    message="You lose! Better luck next time!"
                    col = discord.Colour.red()
                else:
                    message="You win! I'll do better next time!"
                    you+=1
                    col = discord.Colour.dark_green()
            except asyncio.TimeoutError:
                message = "You surrendered! Bot wins!"
                bot+=1
                col = discord.Colour.red()
                bmoji = "🚫"
                emoji = "🚫"
            except:
                print("Error!")
            else:
                bmoji =  [str(r),p,s][bchoice]+[" Rock"," Paper"," Scissors"][bchoice]
                emoji =  [str(r),p,s][ choice]+[" Rock"," Paper"," Scissors"][ choice]
            newbed = discord.Embed(title="Rps match result",description=message,colour=col)
            newbed.add_field(name="You",value=emoji)
            newbed.add_field(name="Bot",value=bmoji)
            if round!=number:
                newbed.add_field(name="You vs Bot (Overall)",value=f"{you}:{bot}",inline=False)
                newbed.set_footer(text="Next round starting in a while...")
                await mes.remove_reaction(reaction,ctx.author)
                await mes.edit(embed=newbed)
                await asyncio.sleep(5)
                emb.description=f"Round {round+1}: Make your choice"
                await mes.edit(embed=emb)
            else:
                newbed.add_field(name="Final score (you vs bot)",value=f"{you}:{bot}",inline=False)
                mess = "You"
                if you>bot:mess+=" win!"
                elif you<bot:mess+=" lose!"
                else:mess+=" drawed!"
                newbed.add_field(name="Match summary",value=mess)
                await mes.edit(embed=newbed)

def setup(bot):
    bot.add_cog(Fun(bot))