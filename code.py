#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
from discord.ext import commands
import urllib.request
import urllib.parse
import discord
import math
import random
import time
import datetime
import aiohttp
import functools
import inspect
import re
import io
import contextlib
import traceback
import sys
import subprocess
import asyncio
from googletrans import Translator

from databasestuff import GuildDB
from paginator import HelpPaginator
from simplepaginator import SimplePaginator
import utils
blacklisted = []
last_invoked=None

# configs

class Information:
    def __init__(self):
        self.owner_id = 360022804357185537
        self.bot_id = 384623978028859392
        self.dict_app_id = 'ebbdd492'
        self.prefixes = (
        'q!', 'q>', 'q<', 'q+', 'q-', 'q*', 'q/', 'q?', 'q.', 'q,', 'q:', 'q;', 'Q!', 'Q>', 'Q<', 'Q+', 'Q-', 'Q*',
        'Q/', 'Q?', 'Q.', 'Q,', 'Q:', 'Q;')
        self.dict_app_key = 'b9942f0306456037953c7481b7f036ca'
        self.languages = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
                          'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian',
                          'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano',
                          'ny': 'chichewa', 'zh-cn': 'chinese (simplified)',
                          'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech',
                          'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto',
                          'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian',
                          'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek',
                          'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew',
                          'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic',
                          'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese',
                          'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer',
                          'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin',
                          'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish',
                          'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese',
                          'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)',
                          'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish',
                          'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian',
                          'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona',
                          'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian',
                          'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish',
                          'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish',
                          'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh',
                          'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino',
                          'he': 'Hebrew'}
info=Information()

async def getprefix(bot,message:discord.Member):
    bot.db.set_collection("guilds")
    m = await bot.db.find(length=2,id=message.guild.id)
    if m:
        m=[m[0]["prefix"]]
    return commands.when_mentioned_or(*(list(info.prefixes)+m))(bot,message)

bot = commands.Bot(description='Tune in to lots of fun with this bot!',
                   command_prefix=getprefix)
bot.db=GuildDB()

class MemberInThisGuild(commands.Converter):
    async def convert(self, ctx, argument):
        if not ctx.guild:
            raise commands.CheckError('This can only be run in a guild')
        member = None
        try:
            id = int(argument)
            member = ctx.guild.get_member(id)
        except ValueError:
            match = re.match("<!?@(\d+)>", argument)
            if match:
                id = int(match.group(1))
                member = ctx.guild.get_member(id)
            else:
                member = ctx.guild.get_member_named(argument)
                if member is None:
                    raise commands.BadArgument('Unrecognised member')
        return member

# commands
class Math:
    '''for mathematical fun'''

    @commands.command()
    async def add(self, ctx, *, numbers):
        '''returns sum of numbers separated with spaces'''
        try:
            await ctx.send(str(sum([int(i) for i in numbers.split()])))
        except:
            await ctx.send("You didn't give the correct arguments.")

    @commands.command()
    async def mul(self, ctx, *, numbers):
        '''returns product of arguments separated with spaces'''
        try:
            m = lambda x, y: x * y
            await ctx.send(str(functools.reduce(m, [int(i) for i in numbers.split()])))
        except:
            await ctx.send("You didn't give the correct arguments.")

    @commands.command()
    async def factorial(self, ctx, num: int):
        '''returns the factorial of the given input'''
        try:
            await ctx.send(embed=discord.Embed(title="%d! is equal to..." % num, description=str(math.factorial(num))))
        except Exception as p:
            await ctx.send(embed=discord.Embed(title=type(p) + " raised!", description=p.args[1]))

    @commands.command()
    async def collatz(self, ctx, num: int):
        '''dedicated to the famous conjecture, will return the steps from input to 1'''
        nums = [num]
        last = num
        while last > 1:
            if last % 2 == 0:
                last //= 2
            else:
                last = last * 3 + 1
            nums.append(last)
        nums = list(map(str, nums))
        ranhex = random.randint(0, 255)
        await ctx.send(embed=discord.Embed(title="Collatzing your way through %d" % num, description=",".join(nums),
                                           colour=discord.Colour.from_rgb(ranhex, ranhex, ranhex)))


class Admin:
    '''for administrative purposes'''

    @commands.command()
    async def kick(self, ctx, member: MemberInThisGuild):
        '''Kick members from your server'''
        try:
            await member.kick(reason=f'{ctx.author} banned {member}')
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command()
    async def ban(self, ctx, member: MemberInThisGuild):
        '''Ban toxic members from your server'''
        try:
            await member.ban(reason=f'{ctx.author} banned {member}')
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command(aliases=['ar', 'updaterole'])
    async def changerole(self, ctx, member: MemberInThisGuild, role: discord.Role):
        '''to add/remove a role from a person'''
        try:
            if role not in member.roles:
                await ctx.author.add_roles(role)
            else:
                await ctx.author.remove_roles(role)
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')


class General:
    '''commands available for everyone'''
    @commands.command(aliases=['how2makebots','howtomakebot','how2makebot'])
    async def howtomakebots(self,ctx):
        '''For people who want to make discord bots'''
        await ctx.send(embed=discord.Embed(title="Join this server",
                                           colour=discord.Colour.dark_blue(),
                                           description="This server teaches how to make Discord Bots using Python or Javascript.\nClick Here --> [Bot Tutorial Server](https://discord.gg/GWdhBSp)").set_thumbnail(
            url="https://images-ext-1.discordapp.net/external/3Nz9MrHwWr8gwkV8c7LBTioqIr4pX7akzwufLBQoMEM/%3Fsize%3D1024/https/cdn.discordapp.com/icons/265828729970753537/88327d2afd3b45a0e08cbd81caabf357.webp"))

    @commands.command()
    async def ping(self, ctx):
        '''checks the time taken for the bot to respond'''
        start = time.monotonic()
        msg = await ctx.send("Pinging... 🕒")
        millis = (time.monotonic() - start) * 1000
        heartbeat = ctx.bot.latency * 1000
        await msg.edit(content=f'Heartbeat: {heartbeat:,.2f}ms Response: {millis:,.2f}ms. ⏲️')

    @commands.command()
    async def say(self, ctx, *, text='Quantum Bot here!!'):
        '''The bot becomes your copycat='''
        await ctx.send(text)
        await ctx.message.delete()

    @commands.command()
    async def now(self, ctx):
        '''Get current date and time'''
        m = str(datetime.datetime.now()).split()
        embed = discord.Embed(title="Date-time information", color=eval(hex(ctx.author.color.value)))
        embed.add_field(name="Date", value="{}".format(m[0]))
        embed.add_field(name="Time", value="{}GMT".format(m[1]))
        await ctx.send(embed=embed)


class Feedback:
    '''feedback related commands'''

    @commands.command(aliases=['fb'])
    async def feedback(self, ctx, *, message):
        '''My bot is not very good, feedback is appreciated!'''
        author = ctx.message.author.name + " said in " + "'" + ctx.guild.name + "'"
        await bot.get_guild(413290013254615041).get_channel(413631317272690688).send(
            embed=discord.Embed(color=eval(hex(ctx.author.color.value)), title=author,
                                description="#" + ctx.channel.name + ":\n" + message))
        await ctx.message.add_reaction('\u2705')

    @commands.command()
    async def suggest(self, ctx, command, *, description):
        '''suggest commands I should work on, and follow by a short description on how it works'''
        author = ctx.message.author.name
        m = await bot.get_guild(413290013254615041).get_channel(413631317272690688).send(
            embed=discord.Embed(title=author + " suggested a command '" + command + "'", description=description,
                                color=ctx.author.color))
        await m.add_reaction("\u2705")
        await m.add_reaction("\u274C")
        r = await bot.wait_for('reaction_add', check=lambda reaction, author: (author.id == info.owner_id) and (
                    reaction.emoji in ["\u2705", "\u274C"]))
        if r[0].emoji == "\u2705":
            await ctx.author.send("Your command {} has been accepted by the owner.".format(command))
            await m.edit(embed=discord.Embed(title="Command to work on: " + command, description=description))
        elif r[0].emoji == "\u274C":
            await ctx.author.send("Your command {} has been rejected by the owner.".format(command))
            await m.delete()


class Information:
    '''To know more about the bot'''

    @commands.command()
    async def botinfo(self, ctx):
        '''some stats about the bot'''
        serv = len(bot.guilds)
        membs = len(bot.users)
        creator = "Pegasus#4022"
        date = f"{bot.user.created_at: %B %d, %Y at %H:%M:%S GMT}"
        await ctx.send(embed=discord.Embed(title="Some bot statistics",
                                           description="```Servers streaming: {}\nUsers streaming: {}\nCreator: {}\nCreation date: {}\nBot Owner: {}```".format(
                                               serv, membs, creator, date, "Dark Angel#4022"), color=ctx.author.colour))

    @commands.command()
    async def prefix(self, ctx):
        '''list of all prefixes my bot uses'''
        prefixlist = tuple(["@Quantum Bot"] + list(info.prefixes))
        await ctx.send("```" + ",".join(list(prefixlist)) + "```" + '\n' + str(len(prefixlist)) + " prefixes")

    @commands.command()
    async def invite(self, ctx):
        '''link to invite my bot elsewhere'''
        await ctx.send(embed=discord.Embed(title="Some bot related links",
                                           description="This is my bot invite:\nhttps://discordapp.com/api/oauth2/authorize?client_id=384623978028859392&permissions=335932630&scope=bot\nPlease consider joining this server too:https://discord.gg/ngaC2Bh\nCheck out Quantum Bot's official site:http://quantum-bot.me",
                                           color=eval(hex(ctx.author.color.value))))

    @commands.command()
    async def getpeople(self, ctx, *, rolename=None):
        '''find all people with a particular role name,bolding means that that is the user's top role'''
        people = []
        role = discord.utils.get(ctx.guild.roles, name=rolename)
        for i in role.members:
            if i.top_role == role:
                people.append("**" + i.name + "**")
            else:
                people.append(i.name)
        if len(people) > 80:
            content = "More than 80 people have this role. I'd rather not state all the people with this role"
        else:
            content = ",".join(people)
        await ctx.send(
            embed=discord.Embed(title="People with the role '%s'" % role.name, color=eval(hex(ctx.author.color.value)),
                                description=content))

    @commands.command()
    async def serverinfo(self, ctx):
        '''get more info on the server'''
        members = len(ctx.guild.members)
        owner = ctx.guild.owner
        created = f"{ctx.guild.created_at: %B %d, %Y at %H:%M:%S GMT}"
        server = ctx.guild.name
        sid = ctx.guild.id
        ver = ["None", "Low", "Medium", "High", "Ultra High"][ctx.guild.verification_level]
        region = ctx.guild.region
        embed = discord.Embed(color=discord.Color(0x000000), title="Server Info:", description="""Server Name:{}\nServer Id:{}\n
Server Region:{}\nMember count:{}\nOwner:{}\nCreated On:{}\nNumber of text channels:{}\nNumber of voice channels:{}\nVerification Level={}""".format(
            server, sid, region, members, owner, created, len(ctx.guild.text_channels), len(ctx.guild.voice_channels),
            ver))
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def perms(self, ctx, user: discord.Member = None):
        '''find what you can do on this server'''
        user = ctx.message.author if user is None else user
        if not user:
            user = ctx.author
        mess = []
        for i in user.guild_permissions:
            if i[1]:
                mess.append("\u2705 {}".format(i[0]))
            else:
                mess.append("\u274C {}".format(i[0]))
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0xFF0000), title=user.name + " guild permissions",
                                           description="\n".join(mess)))

    @commands.command()
    async def roleperms(self, ctx, role: discord.Role = None):
        '''gets the server permissions of a role'''
        role = ctx.author.top_role if role is None else role
        mess = []
        for i in role.permissions:
            if i[1]:
                mess.append("\u2705 {}".format(i[0]))
            else:
                mess.append("\u274C {}".format(i[0]))
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0xFF0000), title=role.name + " guild permissions",
                                           description="\n".join(mess)))

    @commands.command()
    async def permcheck(self, ctx, perm='all_perms', user: discord.Member = None):
        '''checks specific permissions,type all_perms/leave empty for full list'''
        user = ctx.message.author if user is None else user
        permlist = dict(user.guild_permissions)
        if perm == 'all_perms':
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x000000), title="All permissions listed",
                                               description="\n".join(dict(user.guild_permissions).keys())))
            return "\n".join(dict(user.guild_permissions).keys())
        await ctx.send(permlist[perm] * "\u2705" + (1 - permlist[perm]) * "\u274C")
        return permlist[perm]

    @commands.command(name='help')
    async def _help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = bot.get_cog(command) or bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(traceback.format_exception(None, e, e.__traceback__))


class Fun:
    '''have fun with these commands'''
    @commands.command()
    async def reinvoke(self, ctx):
        '''reinvokes the last used command'''
        global last_invoked
        try:
            await last_invoked.reinvoke()
        except:
            await ctx.send("Some error occurred.")
        return

    @commands.command()
    async def dice(self, ctx, times=1):
        '''Roll a dice as many times as you like'''
        total = []
        for i in range(times):
            total.append(random.randint(1, 6))
        botmessage = (('Numbers:' + ','.join([str(i) for i in total])) + '\nTheir sum:') + str(sum(total))
        await ctx.send(botmessage)

    @commands.command()
    async def think(self, ctx):
        '''let the bot think for a while'''
        await ctx.message.delete()
        await ctx.send(discord.utils.get(bot.emojis, name='fidgetthink'))

    @commands.command()
    async def morse(self, ctx, *, message):
        '''Converts your ENGLISH message to morse. And vice versa.\nAdd an e to say it's English and m to say it's morse.'''

        CODE = {'A': '.-', 'B': '-...', 'C': '-.-.',
                'D': '-..', 'E': '.', 'F': '..-.',
                'G': '--.', 'H': '....', 'I': '..',
                'J': '.---', 'K': '-.-', 'L': '.-..',
                'M': '--', 'N': '-.', 'O': '---',
                'P': '.--.', 'Q': '--.-', 'R': '.-.',
                'S': '...', 'T': '-', 'U': '..-',
                'V': '...-', 'W': '.--', 'X': '-..-',
                'Y': '-.--', 'Z': '--..',

                '0': '-----', '1': '.----', '2': '..---',
                '3': '...--', '4': '....-', '5': '.....',
                '6': '-....', '7': '--...', '8': '---..',
                '9': '----.',

                ' ': '/', '.': '.-.-.-', ',': '--..--',
                ':': '---...', '?': '..--..', "'": '.----.',
                '-': '-....-', '/': '-..-.', '@': '.--.-.',
                '=': '-...-', '(': '-.--.', ')': '-.--.-',
                '+': '.-.-.'}

        REVERSE_CODE = {CODE[i]: i for i in CODE}
        a = ""
        scope = ""
        if message[1] != "|" or message[0].lower() not in "me":
            await ctx.send(embed=discord.Embed(title="Morse conversion failed!",
                                               description="You did not specify whether you want it Morse or English",
                                               colour=discord.Colour.red()))
        else:
            await ctx.send(message[2:])
            if message[0].lower() == "m":
                for i in message[2:].upper():
                    if i not in CODE.keys():
                        await ctx.send(embed=discord.Embed(title="Morse conversion failed!",
                                                           description="Unidentified character spotted!",
                                                           colour=discord.Colour.red()))
                        break
                    else:
                        a += CODE[i]
            else:
                for i in message[2:]:
                    scope += i
                    if scope in REVERSE_CODE.keys():
                        a += REVERSE_CODE[scope]
                        scope = ""
                    elif i not in r"\-.":
                        await ctx.send(embed=discord.Embed(title="Morse conversion failed!",
                                                           description="Unidentified character spotted!",
                                                           colour=discord.Colour.red()))
                        break
                    elif len(scope) > 6:
                        await ctx.send(title="Morse conversion failed!", description="Unidentified character spotted!",
                                       colour=discord.Colour.red())
                        break
        m = len(a) // 1900
        for x in range(m):
            await ctx.send(embed=discord.Embed(title="Page {}/{} of Morse Translation".format(x + 1, m + 1),
                                               description="```\n" + a[1900 * x:1900 * (x + 1)] + "```",
                                               colour=discord.Colour.dark_gold()))
        await ctx.send(embed=discord.Embed(title="Page {}/{} of Morse Translation".format(m + 1, m + 1),
                                           description="```\n" + a[1900 * m:] + "```",
                                           colour=discord.Colour.dark_gold()))

    @commands.command()
    async def emojify(self, ctx, *, text='Hello'):
        '''all *English* letters and numbers turn into emojis!'''
        nums = {'0': ':zero:', '1': ':one:', '2': ':two:', "3": ":three:", "4": ":four:", "5": ":five:", "6": ":six:",
                "7": ":seven:", "8": ":eight:", "9": ":nine:", "!": ":grey_exclamation:", "?": ":grey_question:"}
        said = ''
        for i in text:
            if i.isalpha():
                said += (':regional_indicator_' + i.lower()) + ':'
            elif i in nums:
                said += nums[i]
            else:
                said += i
        await ctx.send(said)

    @commands.command()
    async def emojirep(self, ctx, emoji: discord.Emoji, number=1):
        '''[WIP] repeats a given emoji with input'''
        try:
            if number < 1 or number > 10:
                await ctx.send("Stop being enthusiastic!")
            else:
                await ctx.send((discord.Emoji(emoji.id)) * number)
        except:
            await ctx.send("Error ocurred!")

    @commands.command(aliases=["f", "respect"])
    async def rip(self, ctx, member: discord.Member = None):
        '''Rest in piece, my comrade'''
        if member is None:
            member = ctx.author
        elif member.id == info.owner_id or member.id == info.bot_id:
            member = ctx.author
        embed = discord.Embed(title="RIP {}{}".format(member.name, discord.utils.get(bot.emojis, name="rip")),
                              description="Press :regional_indicator_f: to pay your respects",
                              colour=discord.Colour.from_rgb(255, 255, 255))
        embed.set_thumbnail(url=member.avatar_url)
        p = await ctx.send(embed=embed)
        await p.add_reaction(discord.utils.get(bot.emojis, name="f_"))

    @commands.command()
    async def playing(self, ctx):
        '''returns the current bot status'''
        async with ctx.typing():
            embed = discord.Embed(title="Quantum Bot's status:",
                                  description=ctx.guild.get_member(info.bot_id).activity.name)
            embed.set_thumbnail(url=ctx.guild.get_member(info.bot_id).avatar_url)
        await ctx.send(embed=embed)


class Owner:
    '''commands only the bot owner can use, besides repl and exec'''

    @commands.command(pass_context=True)
    async def shutdown(self, ctx):
        '''for me to close the bot'''
        if ctx.message.author.id != info.owner_id:
            await ctx.send("You're not the bot owner!")
        else:
            await ctx.send("Shutting down...")
            await bot.logout()

    @commands.command()
    async def clear(self, ctx, number=1, author: discord.Member = None):
        '''[WIP] clears messages from a channel, if you're allowed'''
        allowed = [360022804357185537, 270149861398151169]
        if ctx.author.id in allowed or ctx.author.guild_permissions.manage_messages:
            if author is not None:
                check = lambda x: x.author == author
                await ctx.channel.purge(limit=number + 1, check=check)
                await ctx.send("Purged %d messages from %s" % (number, author), delete_after=3)
            else:
                await ctx.channel.purge(limit=number + 1)
                await ctx.send("Purged %d messages in this channel" % number, delete_after=3)
        else:
            await ctx.send("You're not approved by the bot owner to delete stuff!")

    @commands.command()
    async def getsource(self, ctx, command):
        '''getting the code for command'''
        if ctx.author.id == info.owner_id:
            a = inspect.getsource(bot.get_command(command).callback)
            m = len(a) // 1900
            embedlist=[]
            for x in range(m):
                embedlist.append(discord.Embed(title="Page {}/{} of '{}' command".format(x + 1, m + 1, command),
                                                   description="```py\n" + a[1900 * x:1900 * (x + 1)] + "```",
                                                   colour=discord.Colour.dark_gold()))
            embedlist.append(discord.Embed(title="Page {}/{} of '{}' command".format(m + 1, m + 1, command),
                                               description="```py\n" + a[1900 * m:] + "```",
                                               colour=discord.Colour.dark_gold()))
            await SimplePaginator(extras=embedlist).paginate(ctx)
        else:
            await ctx.send(embed=discord.Embed(title="Access denied!",
                                               description="This command can only be used by the bot owner!",
                                               colour=discord.Colour.red()))

    @commands.command(pass_context=True)
    async def warn(self, ctx, member: discord.Member, serious: bool, *, reason):
        '''for owner to issue warnings'''
        if ctx.author.id == info.owner_id:
            if serious:
                await ctx.guild.get_member(member.id).send(embed=discord.Embed(title="Warning! [SERIOUS]",
                                                                               description="**My bot owner warned your because**:{}".format(
                                                                                   reason),
                                                                               colour=discord.Colour(0xFF0000)))
            else:
                await ctx.guild.get_member(member.id).send(embed=discord.Embed(title="Warning!",
                                                                               description="**My bot owner warned your because**:{}".format(
                                                                                   reason),
                                                                               colour=discord.Colour(0xFFFF00)))
            await ctx.message.add_reaction('\u2705')


class Pystuff():
    '''commands that relate to Python coding'''

    @commands.command()
    async def pydir(self, ctx, *, command=None):
        '''list of methods of a given object'''
        if ctx.message.author.id != info.owner_id:
            await ctx.send(embed=discord.Embed(title="Error message", color=eval(hex(ctx.author.color.value)),
                                               description="Not allowed!"))
        else:
            if command is None:
                await ctx.send("Argument [command name] must be provided!")
            else:
                try:
                    dire = []
                    a = eval("dir(" + command + ")")
                    for i in a:
                        if i[0] != "_":
                            dire.append("**" + i + "**")
                        elif i[1] != "_":
                            dire.append(i)
                    content = ",".join(dire)
                except NameError:
                    content = "Object %s is not found!" % command
            await ctx.send(embed=discord.Embed(title="Useful methods for object '%s'" % command,
                                               color=eval(hex(ctx.author.color.value)), description=content))

    @commands.command()
    async def pyhelp(self, ctx, *, command=None):
        '''the Python help message for a given object'''
        if ctx.message.author.id != info.owner_id:
            await ctx.send(embed=discord.Embed(title="Error message", color=eval(hex(ctx.author.color.value)),
                                               description="Not allowed!"))
        else:
            if command is None:
                await ctx.send("Argument [command name] must be provided!")
            else:
                try:
                    embeds = []
                    sio = io.StringIO()
                    with contextlib.redirect_stdout(sio):
                        help(command)
                    sio.seek(0)
                    a = sio.getvalue()
                    sio = None
                    for i in range(1, len(a) // 1950 + 1):
                        embeds.append(discord.Embed(title="Python help Page [%d/%d]" % (i, len(a) // 1950 + 1),
                                                    description="```{}```".format(a[1950 * (i - 1):1950 * i]),
                                                    color=ctx.author.color))
                    embeds.append(
                        discord.Embed(title="Python help Page [%d/%d]" % (len(a) // 1950 + 1, len(a) // 1950 + 1),
                                      description="```{}```".format(a[1950 * (len(a) // 1950):]),
                                      color=ctx.author.color))
                    await SimplePaginator(extras=embeds).paginate(ctx)
                except NameError:
                    await ctx.send(
                        embed=discord.Embed(title="Error raised!", description="Object %s is not found!" % command))

    @commands.command()
    async def pypi(self, ctx, search):
        '''searches information about the PyPI for the module you want'''
        base = "https://pypi.org/pypi/{}/json".format(urllib.request.pathname2url(search))
        try:
            f = await utils.getjson(base)
            embed = discord.Embed(title="Details about the PyPI module {}".format(search),
                                  colour=discord.Colour.dark_gold())
            author = f['info']['author']
            email = f['info']['author_email']
            homepage = f['info']['home_page']
            project = f['info']['project_url']
            required_version = f['info']['requires_python']
            module_version = f['info']['version']
            embed.add_field(name="Author", value=author)
            embed.add_field(name="Author's Email", value=email)
            embed.add_field(name="Module's Homepage", value=f"[Homepage]({homepage})")
            embed.add_field(name="Project Url", value="[{}, version {}]({})".format(search, module_version, project))
            embed.add_field(name="Minimum Python version required", value=required_version[2:])
            await ctx.send(embed=embed)
        except aiohttp.client_exceptions.ContentTypeError:
            await ctx.send(embed=discord.Embed(title="Module Cannot Be Found!",
                                               description=f"The module with the name **{search}** does not exist.",
                                               colour=discord.Colour.red()))
        except discord.errors.HTTPException:
            await ctx.send(embed=discord.Embed(title="Module Information Cannot Be Obtained",
                                               description=f"The module with the name **{search}** does not have a complete description, if one even exists.",
                                               colour=discord.Colour.red()))

    @commands.command()
    async def pypisearch(self, ctx, module):
        '''gets a list of PyPI modules with roughly similar names'''
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pypi.org/search/?" + urllib.parse.urlencode({"q": module})) as response:
                f = await response.text()
        indicess = list(utils.find('<h3 class="package-snippet__title">', f))
        indicese = list(utils.find('</h3>', f))
        modules = []
        for i in range(len(indicess)):
            e = (f[indicess[i]:indicese[i]])
            namestart = list(utils.find('<span class="package-snippet__name">', e))[0] + 36
            verstart = list(utils.find('<span class="package-snippet__version">', e))[0] + 39
            spans = list(utils.find('</span>', e))
            modules.append(f"{e[namestart:spans[0]]}: v{e[verstart:spans[1]]}")
        send = discord.Embed(title=f"PyPI search results for {module}", colour=ctx.author.colour,
                             description="```" + "\n".join(modules) + "```")
        await ctx.send(embed=send)


class Media:
    '''commands that help you get various media'''

    @commands.command(passcontext=True)
    async def youtube(self, ctx, *, youtube):
        '''Searches youtube videos with inputted queries'''
        embed = discord.Embed(title="Youtube search for " + youtube, color=eval(hex(ctx.author.color.value)))
        try:
            query_string = urllib.parse.urlencode({'search_query': youtube, })
            html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall('href=\\"\\/watch\\?v=(.{11})', html_content.read().decode())
            if len(search_results) >= 3:
                embed.add_field(name="Top result", value='http://www.youtube.com/watch?v=' + search_results[0])
                embed.add_field(name="Other results", value='http://www.youtube.com/watch?v=' + search_results[
                    1] + "\n" + 'http://www.youtube.com/watch?v=' + search_results[2])
            else:
                embed.add_field(name="Top result", value='http://www.youtube.com/watch?v=' + search_results[0])
        except:
            embed.add_field(name="Error",
                            value="Your request did not produce any output. Perhaps try searching a different query?")
        finally:
            await ctx.send(embed=embed)

    @commands.command()
    async def google(self, ctx, *, query):
        '''Search Google for something'''
        content = []
        async with ctx.typing():
            m = await utils.getjson("http://api.tanvis.xyz/search/" + urllib.request.pathname2url(query))
        for i in m:
            content.append(i['link'])
        embed = discord.Embed(title="'%s' search results:" % query, description="\n".join(content),
                              colour=discord.Colour.from_rgb(66, 133, 244))
        embed.set_footer(text="using tanvis.xyz API")
        await ctx.send(embed=embed)

    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *, anything):
        '''look through wikipedia for what you want'''
        wew = urllib.request.pathname2url(anything)
        f = await utils.getjson(
            f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&indexpageids=1&redirects=1&explaintext=1&exsectionformat=plain&titles={wew}")
        query = f['query']
        pageids = query['pageids']
        title = list(query['pages'].values())[0]['title']
        extract = list(query['pages'].values())[0]['extract']
        texts=utils.partition(extract,1000)
        embedlist=[discord.Embed(title=title+" Page {}/{}".format(i+1,len(texts)),description=texts[i],colour=discord.Colour.lighter_grey()).set_thumbnail(url="https://images-ext-1.discordapp.net/external/CYCtSp1meQ0f_ZFd5y0T14UlI_xvqqLWPjUJ2gINt58/https/en.wikipedia.org/static/images/project-logos/enwiki.png") for i in range(len(texts))]
        await SimplePaginator(extras=embedlist).paginate(ctx)

    @commands.command()
    async def xkcd(self, ctx, num: int = None):
        '''read the famous comic strip, leaving blank gets random comic'''
        try:
            async with ctx.typing():
                if num is None: num = random.randint(1, 1996)
                url = f'https://xkcd.com/{num}/info.0.json'
                f = await utils.getjson(url)
                m = discord.Embed(colour=discord.Color.from_rgb(245, 245, 220),
                                  title="xkcd #{}:{}".format(str(f['num']), f['safe_title']),
                                  description=f['transcript'], timestamp=datetime.datetime.now())
                m.set_image(url=f['img'])
                m.add_field(name="Links", value=f['img'] + '\nhttps://xkcd.com/' + str(f['num']))
                m.add_field(name="Publication date:", value=f['day'] + '/' + f['month'] + '/' + f['year'], inline=False)
            await ctx.send(embed=m)
        except:
            if num == 404:
                m = discord.Embed(title="xkcd #404: Think again, does it exist?",
                                  description="This came between Monday and Wednesday, 2 consecutive days of xkcd comic publication. This can be considered an April Fools prank or a reference to the 404 Error: Not Found")
                m.set_image(url='https://www.explainxkcd.com/wiki/images/9/92/not_found.png')
            else:
                await ctx.send("Fetching your a random xkcd comic...", delete_after=2)
                async with ctx.typing():
                    num = random.randint(1, 1996)
                    url = f'https://xkcd.com/{num}/info.0.json'
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            f = await response.json(encoding='utf8')
                    m = discord.Embed(colour=discord.Color.from_rgb(245, 245, 220),
                                      title="xkcd #{}:{}".format(str(f['num']), f['safe_title']),
                                      description=f['transcript'], timestamp=datetime.datetime.now())
                    m.set_image(url=f['img'])
                    m.add_field(name="Links", value=f['img'] + '\nhttps://xkcd.com/' + str(f['num']))
                    m.add_field(name="Publication date:", value=f['day'] + '/' + f['month'] + '/' + f['year'],
                                inline=False)
            await ctx.send(embed=m)

    @commands.cooldown(rate=1, per=8, type=commands.BucketType.guild)
    @commands.command()
    async def weather(self, ctx, *, location):
        '''to get the weather of a given location'''
        try:
            async with ctx.typing():
                url = "http://api.tanvis.xyz/weather/" + urllib.request.pathname2url(location)
                f = await utils.getjson(url)
                if 'error' in f:
                    await ctx.send(embed=discord.Embed(title="An error occurred",
                                                       description="I could not find your given location",
                                                       colour=discord.Colour.red()))
                else:
                    embed = discord.Embed(title="Weather information gathered", colour=discord.Colour.dark_orange(),
                                          description="Here is your result, " + ctx.author.mention)
                    embed.add_field(name="Location", value=f['name'], inline=False);
                    embed.add_field(name="Temperature in °C", value=f['celsius'])
                    embed.add_field(name="Temperature in °F", value=f['fahrenheit']);
                    embed.add_field(name="Weather", value=f['weather'])
                    embed.add_field(name="Wind Speed", value=f['windSpeed']);
                    embed.set_thumbnail(url=f['icon'])
                    embed.set_footer(text="using **tanvis.xyz** API")
                    await ctx.send(embed=embed)
        except:
            await ctx.send("An error occurred. Please try again.", delete_after=3)

    @commands.cooldown(rate=1, per=8, type=commands.BucketType.guild)
    @commands.command(aliases=['define', 'def', 'dict'])
    async def dictionary(self, ctx, word):
        '''search Oxford Dictionaries to get the definition you need'''
        language = 'en'
        word_id = word
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
        r = __import__("requests").get(url, headers={'app_id': info.dict_app_id, 'app_key': info.dict_app_key})
        definitions = {}
        status_code = {
            200: 'Success!',
            400: 'The request was invalid or cannot be otherwise served.',
            403: 'The request failed due to invalid credentials.',
            404: 'No entry is found.',
            500: 'Something is broken. Please contact the Oxford Dictionaries '
                 'API team to investigate.',
            502: 'Oxford Dictionaries API is down or being upgraded.',
            503: 'The Oxford Dictionaries API servers are up, but overloaded '
                 'with requests. Please try again later.',
            504: 'The Oxford Dictionaries API servers are up, but the request '
                 'couldn’t be serviced due to some failure within our stack. '
                 'Please try again later.'
        }
        if r.status_code == 200:
            for i in r.json()["results"]:
                for j in i["lexicalEntries"]:
                    for k in j["entries"]:
                        for v in k["senses"]:
                            deff = v["definitions"][0]
                            examples = []
                            try:
                                for f in v["examples"]:
                                    examples += ["- " + "".join(f["text"])]
                                definitions[deff] = "\n".join(examples)
                            except KeyError:
                                definitions[deff] = "(no examples)"
            embed = discord.Embed(title="Definitions for the word %s" % word, colour=discord.Colour.blue())
            desc_text = []
            for key in definitions:
                temp = "***{}. {}***".format(len(desc_text) + 1, key)
                exam = definitions[key]
                desc_text += [temp + "\n**Examples:**\n" + exam]
            embed.description = "\n".join(desc_text)
            embed.set_footer(text="Using **Oxford Dictionaries** API")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="An error occurred while processing your request!", colour=discord.Colour.red())
            embed.add_field(name="Error Code {}".format(r.status_code), value=status_code[r.status_code])
            await ctx.send(embed=embed)

    @commands.command()
    async def qrcode(self, ctx, *, message="Please provide an argument"):
        '''Generate a QR Code'''
        try:
            async with ctx.typing():
                url = "http://api.qrserver.com/v1/create-qr-code/?"
                add = urllib.parse.urlencode({'size': '300x300', 'data': message})
                send = (url + add).replace(' ', '')
                embed = discord.Embed(title=ctx.author.name + ", here is your QR Code!", colour=ctx.author.colour)
                embed.set_footer(text="Used **api.qrserver.com** API")
                embed.set_image(url=send)
            await ctx.send(embed=embed)
        except:
            await ctx.send("An error occurred. Please try again.", delete_after=3)

    @commands.cooldown(rate=1, per=8, type=commands.BucketType.guild)
    @commands.command(aliases=["trans"])
    async def translate(self, ctx, *, message="Hello"):
        '''Uses google translate to translate given message, opens an interactive support'''
        try:
            m = await ctx.send(
                ctx.author.mention + ", please choose your source language. Can be its name or its code. Anything not detected defaults to auto.")
            src = await bot.wait_for('message', check=lambda x: x.author == ctx.author, timeout=60)
            await m.delete()
            m = await ctx.send(
                ctx.author.mention + ", please choose your destination language. Can be its name or its code. Anything not detected defaults to en,English.")
            dest = await bot.wait_for('message', check=lambda x: x.author == ctx.author, timeout=60)
            await m.delete()
            src = src.content
            dest = dest.content
            if src not in list(info.languages.keys()) + list(info.languages.values()):
                src = "auto"
            if dest not in list(info.languages.keys()) + list(info.languages.values()):
                dest = "en"
            async with ctx.typing():
                translator = Translator()
                f = translator.translate(message, dest=dest, src=src)
                sourcelang = info.languages[f.src] + "({})".format(f.src)
                destlang = info.languages[f.dest] + "({})".format(f.dest)
                embed = discord.Embed(title="Translation output", colour=discord.Colour.from_rgb(79, 255, 176))
                embed.add_field(name="Input [ {} ]:".format(sourcelang), value=f.origin, inline=False)
                embed.add_field(name="Result [ {} ]:".format(destlang), value=f.text)
                embed.set_footer(text="Using the google translate API", icon_url=bot.user.avatar_url)
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            await ctx.send(
                embed=discord.Embed(title="Error", description="You haven't filled up necessary data! Try again!",
                                    colour=discord.Colour.red()))


class Images:
    '''commands dedicated to sending some image'''

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        '''Need a hug? Quantum Bot to the rescue!'''
        embed = discord.Embed(colour=discord.Colour.from_rgb(245, 245, 14))
        embed.set_footer(text="Credits to Google Image Search Results",
                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1000px-Google_%22G%22_Logo.svg.png")
        with open("Images/hugs.txt") as hugs:
            image = random.choice(hugs.readlines())
        embed.set_image(url=image)
        if member == None:
            embed.title = "Hey {}, here yougo, a hug!".format(ctx.author)
        elif member == bot.user:
            embed.title = "Thank you {} for the hug! I appreaciate your love! :)".format(ctx.author)
        else:
            embed.title = "Hey {}, {} has hugged you!".format(member, ctx.author)
        await ctx.send(embed=embed)

    @commands.command(aliases=["cat", "kitten", "kitty"])
    async def cats(self, ctx):
        '''Who doesn't love images of these furries? Let's see a picture of them!'''
        embed = discord.Embed(title="{}, here's your cute furball".format(ctx.author), colour=discord.Colour.teal())
        embed.set_footer(text="Credits to Google Image Search Results",
                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/1000px-Google_%22G%22_Logo.svg.png")
        embed.description = random.choice(
            ["Awww, how cute!", "These cuties melt my heart!", "So adorable!", "Meowr!", "Kittens for life!", "Purrr!"])
        with open("Images/cats.txt") as cats:
            embed.set_image(url=random.choice(cats.readlines()))
        await ctx.send(embed=embed)

class Data:
    '''these commands store data'''
    @commands.cooldown(rate=1,per=5)
    @commands.command()
    async def bump(self,ctx,member:discord.Member=None):
        '''bump Quantum Bot up, see your bump statistics'''
        bot.db.set_collection("bumps")
        if member is None and not ctx.author.bot:
            async with ctx.typing():
                authorbump=await bot.db.find(author=str(ctx.author.id))
                if len(authorbump)==0:
                    await bot.db.insert(author=str(ctx.author.id),bumps=1)
                else:
                    currauthor=authorbump[0]
                    currcount=currauthor["bumps"]
                    await bot.db.delete(author=currauthor["author"])
                    await bot.db.insert(author=str(ctx.author.id),bumps=(currcount+1))
            await ctx.send(embed=discord.Embed(title="Bumping successful!",colour=discord.Colour.dark_green()))
        else:
            async with ctx.typing():
                member_ent=await bot.db.find(author=str(member.id))
                if len(member_ent)==0:
                    num="0"
                else:
                    num=str(member_ent[0]["bumps"])
            await ctx.send(embed=discord.Embed(title=f"Number of times {member.display_name} bumped",description=num,colour=discord.Colour.blue()))

    @commands.cooldown(rate=1, per=5)
    @commands.command()
    async def bumpboard(self, ctx):
        '''to see the top 10 bumps leaderboard'''
        async with ctx.typing():
            people = await bot.db.find(length=10)
            people.sort(key=lambda x: x["bumps"], reverse=True)
            count = 0
            sendembed = discord.Embed(title="Bump Leaderboards", colour=discord.Colour.darker_grey())
            for person in people:
                count += 1
                sendembed.add_field(name="#%d, with %d bumps" % (count, person["bumps"]),
                                value=discord.utils.get(bot.users, id=int(person["author"])))
        await ctx.send(embed=sendembed)

    @commands.cooldown(rate=1, per=5)
    @commands.command()
    async def customprefix(self, ctx, prefix: str = None):
        '''sets the custom bot prefix for your guild, sets the prefix if you specified any, provided no spaces'''
        bot.db.set_collection("guilds")
        async with ctx.typing():
            res = await bot.db.find(length=1, id=ctx.guild.id)
            if res:
                res = res[0]
                if prefix == None:
                    try:
                        customprefix = res["prefix"]
                    except KeyError:
                        embed = discord.Embed(title="This guild's custom prefix", description="Not set yet",
                                              colour=discord.Colour.dark_gold())
                    else:embed = discord.Embed(title="This guild's custom prefix", description=customprefix,
                                               colour=discord.Colour.dark_gold())
                else:
                    if ctx.author.guild_permissions.manage_guild or ctx.author.id == info.owner_id:
                        await bot.db.delete(id=ctx.guild.id)
                        await bot.db.insert(id=ctx.guild.id, prefix=prefix)
                        embed = discord.Embed(title="Successfully set this guild's custom prefix!",
                                              colour=discord.Colour.dark_green())
                    else:
                        embed = discord.Embed(title="Operation failed!",
                                              description="You couldn't change this guild's custom prefix!",
                                              colour=discord.Colour.red())
            else:
                if prefix == None:
                    customprefix = "None set yet"
                    embed = discord.Embed(title="This guild's custom prefix", description=customprefix,
                                          colour=discord.Colour.dark_gold())
                else:
                    if ctx.author.guild_permissions.manage_guild or ctx.author.id == info.owner_id:
                        await bot.db.insert(id=ctx.guild.id, prefix=prefix)
                        embed = discord.Embed(title="Successfully set this guild's custom prefix!",
                                              description="This is the first time you're setting my custom prefix!!",
                                              colour=discord.Colour.dark_green())
                    else:
                        embed = discord.Embed(title="Operation failed!",
                                              description="You couldn't change this guild's custom prefix!",
                                              colour=discord.Colour.red())
        await ctx.send(embed=embed)

class Beta:
    '''for commands in testing'''

    @commands.cooldown(rate=1, per=5)
    @commands.command()
    async def autorole(self,ctx,*,rolename:str=None):
        bot.db.set_collection("guilds")
        await ctx.send("In-dev")


# everything from here onwards are bot events

@bot.event
async def on_member_join(member):
    if member.guild.id == 413290013254615041:
        embed = discord.Embed(title="Member join",
                              description="Welcome to Quantum Bot and Pegasus server, " + member.name + "! Please read the rules in " + member.guild.get_channel(
                                  444443837482532867).mention + " before you proceed :)",
                              colour=discord.Colour.from_rgb(87, 242, 87))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Bot", value=member.bot)
        embed.add_field(name="Member id", value=member.id)
        await member.guild.get_channel(413303508289454081).send(embed=embed)
    elif member.guild.id == 470430655872892928:
        embed = discord.Embed(title="Welcome to Bot Emotes Inc.",
                              description="Welcome " + member.mention + "! Please read the " + member.guild.get_channel(
                                  470431050649305098).mention + " and react with \u2705 to confirm that you agree to the rules.",
                              colour=discord.Colour.dark_gold())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Member count", value=len(member.guild.members))
        embed.add_field(name="Bot", value=member.bot)
        await member.guild.get_channel(470431623079264258).send(embed=embed)


@bot.event
async def on_member_remove(member):
    if member.guild.id == 413290013254615041:
        embed = discord.Embed(title="Member leave",
                              description="We're sad to see you leave, " + member.name + "! We wish you could return :(",
                              colour=discord.Colour.from_rgb(242, 23, 33))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Bot", value=member.bot)
        embed.add_field(name="Member id", value=member.id)
        await member.guild.get_channel(413303508289454081).send(embed=embed)
    elif member.guild.id == 470430655872892928:
        embed = discord.Embed(title="Goodbye from Bot Emotes Inc.",
                              description="Goodbye " + member.name + "! We hope you had a nice stay and had fun!",
                              colour=discord.Colour.red())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Member count", value=len(member.guild.members))
        embed.add_field(name="Bot", value=member.bot)
        await member.guild.get_channel(470431623079264258).send(embed=embed)


@bot.event
async def on_raw_reaction_add(reaction):
    if reaction.channel_id == 470431050649305098:
        member = discord.utils.get(bot.get_guild(reaction.guild_id).roles, name="Member")
        await bot.get_guild(reaction.guild_id).get_member(reaction.user_id).add_roles(member)
    elif reaction.channel_id == 475197039974678530:
        member = discord.utils.get(bot.get_guild(reaction.guild_id).roles, name="Access Granted")
        print(member)
        await bot.get_guild(reaction.guild_id).get_member(reaction.user_id).add_roles(member)

@bot.event
async def on_command(ctx):
    global last_invoked
    last_invoked=ctx
    if ctx.command.name not in "execrepl":print("Invocation of "+ctx.command.name+" by "+ctx.author.name)

@bot.event
async def on_command_error(ctx, error):
    if type(error) == discord.ext.commands.errors.CommandOnCooldown:
        await ctx.send(
            embed=discord.Embed(title="Woah woah slow down!", description=error.args[0], colour=discord.Colour.red()))
    else:
        embed = discord.Embed(title=str(type(error))[8:-2], description=str(error),
                              colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255),
                                                             random.randint(0, 255)))
        await ctx.send("***Roses are red, violets are blue, there is an error when the command is used by you***",
                       embed=embed, delete_after=15)
        for i in (traceback.format_exception(None, error, error.__traceback__)):
            print(i, end="")


@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(title="Guild joined!", colour=discord.Colour.green())
    embed.add_field(name=guild.name, value="Owner:%s" % guild.owner)
    await bot.get_guild(413290013254615041).get_channel(463261256355282944).send(embed=embed)


@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(title="Guild left :(", colour=discord.Colour.red())
    embed.add_field(name=guild.name, value="Owner:%s" % guild.owner)
    await bot.get_guild(413290013254615041).get_channel(463261256355282944).send(embed=embed)


@bot.event
async def on_message(message):
    # add stuff here when you want to
    await bot.process_commands(message)


@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)


@bot.event
async def on_ready():
    bot.remove_command('help')
    bot.load_extension('code2')
    bot.add_cog(Owner())
    bot.add_cog(Pystuff())
    bot.add_cog(Information())
    bot.add_cog(Admin())
    bot.add_cog(Math())
    bot.add_cog(General())
    bot.add_cog(Feedback())
    bot.add_cog(Fun())
    bot.add_cog(Media())
    bot.add_cog(Images())
    bot.add_cog(Data())
    bot.add_cog(Beta())
    await bot.change_presence(activity=discord.Game(name='Type [q?help] for help', type=2), status=discord.Status.dnd)
    f = bot.get_guild(413290013254615041).get_channel(436548366088798219)
    await bot.db.add_collection("bumps")
    await bot.db.add_collection("guilds")
    if __file__ == r"C:/Users/vengat/Desktop/Bot/Quantum Bot/code.py":
        await f.send(embed=discord.Embed(title="Beta Bot Update tested on:",
                                         description=f"{datetime.datetime.utcnow(): %B %d, %Y at %H:%M:%S GMT}",
                                         colour=discord.Colour.blue()))
    else:
        await f.send(embed=discord.Embed(title="Bot Updated on:",
                                         description=f"{datetime.datetime.utcnow(): %B %d, %Y at %H:%M:%S GMT}",
                                         colour=discord.Colour.dark_gold()))
    print("Bot works, go on.")

    async def change_activities():
        timeout = 5  # Here you can change the delay between changes
        while True:
            possb = 'Type [{}help] for help'.format(random.choice(info.prefixes))
            await bot.change_presence(activity=discord.Game(possb, status=discord.Status.dnd))
            await asyncio.sleep(timeout)
    bot.loop.create_task(change_activities())


bot.run('Mzg0NjIzOTc4MDI4ODU5Mzky.DZecOA.rekvrUSZL8q9QVzlIlnoS0lNYVI')
# ok