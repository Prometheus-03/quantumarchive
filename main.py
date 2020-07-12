import os
from functools import partial
import aiohttp
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
from dbwrapper import DB
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont
from io import BytesIO


def isbeta():
    return __file__ in [r"C:\Users\user\Desktop\Discord Bot\main.py", r"C:/Users/user/Desktop/Discord Bot/main.py"]


if isbeta():
    bot = commands.Bot(description='The official KhAnubis Discord server bot',
                       command_prefix=commands.when_mentioned_or("k>", "K>"))
else:
    bot = commands.Bot(description='The official KhAnubis Discord server bot',
                       command_prefix=commands.when_mentioned_or('k!', 'K!'))


@bot.event
async def on_message(message):
    # add stuff here when you want to
    await bot.process_commands(message)
    if (isbeta()) or message.author.bot or (message.guild.get_member(message.author.id) is None) or (
            message.channel.id in [728630861171261551, 626183225449906177, 685952333959659552, 536271017426026506]):
        return
    if "hmm" in message.content and message.author.id==702420055786389555:
        return
    users = DB("UserProfiles")
    users.set_collection("users")
    auth = await users.find(author_id=message.author.id)
    if auth:
        guy = auth[0]
        if 'cooldown' not in guy.keys():
            cooldown = int(datetime.datetime.now().timestamp())
            xp = 5
            await users.update(guy["_id"], cooldown=cooldown, xp=xp)
        elif int(datetime.datetime.now().timestamp()) - guy['cooldown'] >= 60:
            cooldown = int(datetime.datetime.now().timestamp())
            rewards = {15: message.guild.get_role(663461450626367508), 25: message.guild.get_role(663461777576558594),
                       35: message.guild.get_role(663462503413579788), 45: message.guild.get_role(663462321078796289)}
            xp = guy['xp'] + 5
            await users.update(guy["_id"], cooldown=cooldown, xp=xp)

            def fromlevel(level):
                """Get XP needed to reach level"""
                return math.floor(7.02 * level ** 2.13)

            def fromxp(xp):
                """Get level from XP"""
                return math.floor(((xp + 1) / 7.02) ** (1 / 2.13))

            if xp - fromlevel(fromxp(xp)) < 5:
                # level up
                await message.channel.send(f"Good work, {message.author.mention}! You're now level {fromxp(xp)}!",
                                           delete_after=5)
                if fromxp(xp) in rewards.keys():
                    await message.channel.send(f"You've gotten a new rank: `{rewards[fromxp(xp)].name}`!",
                                               delete_after=5)
                    await message.author.add_roles(rewards[fromxp(xp)])
        else:
            pass
    else:
        await users.insert(author_id=message.author.id, cooldown=int(datetime.datetime.now().timestamp()), xp=5)


@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)


@bot.event
async def on_command_error(ctx, error):
    if type(error) == commands.errors.CommandOnCooldown:
        await ctx.send(
            embed=discord.Embed(title="Woah woah slow down!", description=error.args[0], colour=discord.Colour.red()))
    elif type(error) == commands.MissingPermissions:
        m = "\n".join(error.missing_perms)
        emb = discord.Embed(title="You do not have the needed permissions", description=m, colour=discord.Colour.red())
        await ctx.send(embed=emb)
    else:
        embed = discord.Embed(title=str(type(error))[8:-2], description=str(error),
                              colour=discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255),
                                                             random.randint(0, 255)))
        await ctx.send("***Roses are red, violets are blue, there is an error when the command is used by you***",
                       embed=embed, delete_after=15)
        for i in (traceback.format_exception(None, error, error.__traceback__)):
            print(i, end="")


def checkmod(payload):
    return 569237216627261488 in [i.id for i in bot.get_guild(payload.guild_id).get_member(payload.user_id).roles]


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    try:
        channel = bot.get_guild(payload.guild_id).get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if payload.channel_id == 720574680792301609 and message.embeds and message.embeds[0].title[
                                                                           :10] == "Suggestion" and (
                payload.user_id == 586426079078514700 or checkmod(payload)):
            rcs = message.reactions
            ok = 0
            no = 0
            seen = 0
            ok_l = list(filter(lambda x: x.emoji == "✅", rcs))
            no_l = list(filter(lambda x: x.emoji == "❌", rcs))
            seen_l = list(filter(lambda x: x.emoji == "👀", rcs))
            if ok_l: ok = ok_l[0].count
            if no_l: no = no_l[0].count
            if seen_l: seen = seen_l[0].count
            if seen:
                emb = message.embeds[0]
                emb.colour = discord.Colour.teal()
                emb.title = "Implemented suggestion"
                await message.edit(embed=emb)
                await message.unpin()
                emb_cont = emb.description
                author = bot.get_guild(payload.guild_id).get_member(int(re.search(r'\d+',emb_cont).group()))
                await author.send(embed=emb)
            elif ok <= no:
                # reject
                emb = message.embeds[0]
                emb.colour = discord.Colour.red()
                emb.title = "Suggestion rejected"
                await message.edit(embed=emb)
                await message.unpin()
                emb_cont = emb.description
                author = bot.get_guild(payload.guild_id).get_member(int(re.search(r'\d+',emb_cont).group()))
                await author.send(embed=emb)
            else:
                # accept
                emb = message.embeds[0]
                emb.colour = discord.Colour.dark_green()
                emb.title = "Suggestion considered"
                await message.edit(embed=emb)
                await message.pin()
                emb_cont = emb.description
                author = bot.get_guild(payload.guild_id).get_member(int(re.search(r'\d+',emb_cont).group()))
                await author.send(embed=emb)
    except discord.errors.NotFound:
        print(f"Message with id {payload.message_id} not found")

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    try:
        channel = bot.get_guild(payload.guild_id).get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if payload.channel_id == 720574680792301609 and message.embeds and message.embeds[0].title[
                                                                           :10] == "Suggestion" and (
                payload.user_id == 586426079078514700 or checkmod(payload)):
            rcs = message.reactions
            ok = 0
            no = 0
            seen = 0
            ok_l = list(filter(lambda x: x.emoji == "✅", rcs))
            no_l = list(filter(lambda x: x.emoji == "❌", rcs))
            seen_l = list(filter(lambda x: x.emoji == "👀", rcs))
            if ok_l: ok = ok_l[0].count
            if no_l: no = no_l[0].count
            if seen_l: seen = seen_l[0].count
            if seen:
                emb = message.embeds[0]
                emb.colour = discord.Colour.teal()
                emb.title = "Implemented suggestion"
                await message.edit(embed=emb)
                await message.unpin()
                emb_cont = emb.description
                author = bot.get_guild(payload.guild_id).get_member(int(re.search(r'\d+',emb_cont).group()))
                await author.send(embed=emb)
            elif ok <= no:
                # reject
                emb = message.embeds[0]
                emb.colour = discord.Colour.red()
                emb.title = "Suggestion rejected"
                await message.edit(embed=emb)
                await message.unpin()
                emb_cont = emb.description
                author = bot.get_guild(payload.guild_id).get_member(int(re.search(r'\d+',emb_cont).group()))
                await author.send(embed=emb)
            else:
                # accept
                emb = message.embeds[0]
                emb.colour = discord.Colour.dark_green()
                emb.title = "Suggestion considered"
                await message.edit(embed=emb)
                await message.pin()
                emb_cont = emb.description
                author = bot.get_guild(payload.guild_id).get_member(int(re.search(r'\d+',emb_cont).group()))
                await author.send(embed=emb)
    except discord.errors.NotFound:
        print(f"Message with id {payload.message_id} not found")


@bot.event
async def on_member_join(member):
    if isbeta(): return
    session = aiohttp.ClientSession(loop=bot.loop)
    try:
        avatar_url = member.avatar_url_as(format="png")

        async with session.get(str(avatar_url)) as response:
            # this gives us our response object, and now we can read the bytes from it.
            avatar_bytes = await response.read()

        def processing(avatar_bytes):
            img1 = Image.open("Resources/welcome_banner.png")
            # img.show()
            prof = Image.open(BytesIO(avatar_bytes))
            prof = prof.resize((300, 300))
            # prof.show()

            img = prof.convert("RGB")
            npImage = np.array(img)
            h, w = img.size

            # Create same size alpha layer with circle
            alpha = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice([0, 0, h, w], 0, 360, fill=255)

            # Convert alpha Image to numpy array
            npAlpha = np.array(alpha)

            # Add alpha layer to RGB
            npImage = np.dstack((npImage, npAlpha))

            # Save with alpha
            final = Image.fromarray(npImage)
            final.save('Output/welcome.png')

            f = Image.open("Output/welcome.png")
            img1.paste(f, ((img1.size[0] - f.size[0]) // 2, 240), f.convert('RGBA'))
            user = member.name + "#" + member.discriminator
            m = ImageDraw.Draw(img1)
            size = 30
            font = ImageFont.truetype(os.path.join(os.getcwd(), "Resources", "LandasansMedium-ALmWA.ttf"), size)
            text = f"Welcome to the KhAnubis Discord Server, {user}"
            no = member.guild.member_count
            count = f"Member number: #{no}"
            while font.getsize(text)[0] < 0.8 * img1.size[0]:
                size += 1
                font = ImageFont.truetype(os.path.join(os.getcwd(), "Resources", "LandasansMedium-ALmWA.ttf"), size)
            m.text(((img1.size[0] - font.getsize(text)[0]) // 2, 570), text, (255, 255, 255), font=font)
            m.text(((img1.size[0] - font.getsize(count)[0]) // 2, 570 + size + 10), count, (255, 255, 255), font=font)
            final_buff = BytesIO()
            img1.save(final_buff, "png")
            final_buff.seek(0)
            return final_buff

        fn = partial(processing, avatar_bytes)

        # this runs our processing in an executor, stopping it from blocking the thread loop.
        # as we already seeked back the buffer in the other thread, we're good to go
        final_buffer = await bot.loop.run_in_executor(None, fn)
        await session.close()

        # prepare the file
        file = discord.File(filename="welcoming.png", fp=final_buffer)

        # send it
        await member.add_roles(member.guild.get_role(559939368303853598))
        # lab rats
        if member.id in [607120805914214421, 722673814659530784]:
            await member.add_roles(member.guild.get_role(721342810573373461))
        await member.guild.get_channel(648718517272707086).send(
            f"Welcome, {member.mention}! Please read the <#493867900592062474> and our <#709028380850389043>. Welcome to the KhAnubis Discord Server!",
            file=file)
    except:
        await session.close()


@bot.event
async def on_member_remove(member):
    if isbeta(): return
    if member.id in [i.user.id for i in (await member.guild.bans())]:
        await member.guild.get_channel(648718517272707086).send(
            f"{member.name + '#' + member.discriminator} has committed heresy. Be gone, heretic."
        )
        return
    if member.id in [607120805914214421, 722673814659530784]:
        await member.guild.get_channel(648718517272707086).send(
            f"{member.name + '#' + member.discriminator} left the server as part of a test.")
        return
    # welcoming channel is 648718517272707086
    await member.guild.get_channel(648718517272707086).send(
        f"{member.name + '#' + member.discriminator} has left us. We shall miss you! 😢")

@bot.event
async def on_member_unban(guild,user):
    if isbeta():return
    await guild.get_channel(648718517272707086).send(
        f"The council has decided to pardon {user.name + '#' + user.discriminator}. We shall await their return."
    )

@bot.event
async def on_ready():
    bot.remove_command("help")
    for i in ["suggestion", "info", "fun", "levelling", "timezone", "repl", "mod"]:
        bot.load_extension(i)
        print("Extension Loaded: " + i)
    await bot.change_presence(activity=discord.Game(name='Type [k!help] for help', type=2), status=discord.Status.dnd)
    print("Okay")
    if not isbeta():
        status = discord.Embed(title="Bot logged on",description="\n".join(["Extensions loaded:```"]+list(bot.extensions.keys())+["```"]))
    else:
        status = discord.Embed(title="Beta bot active",description="\n".join(["Extensions loaded:```"]+list(bot.extensions.keys())+["```"]))
    status.color = discord.Colour.dark_green()
    await bot.get_channel(720574680792301609).send(embed=status)


if isbeta():
    print("Beta bot running")
    bot.run("NzIxMzMzNDAxNDk5NTk4ODQ4.XuTAhA.f-eyAaIl1mKkIT47qhshS065sCo")
else:
    print("Stable bot running")
    bot.run("NzIwMjE2MzYxMzk3Mzg3Mjg0.XuC4Bw.qsbKPjdcSl3E4yq_DGgX4QjCq-g")
