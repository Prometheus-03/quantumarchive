import gspread
from oauth2client.service_account import ServiceAccountCredentials as Setup
from discord.ext import commands
import time
import datetime
import math
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
ownerid = 360022804357185537

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = Setup.from_json_keyfile_name("quantumbase-ca2e03e56485.json",scope)
client = gspread.authorize(creds)
sheet = client.open("Dataspread").sheet1

class Database:
  def __init__(self,bot):
    self.bot=bot
    self.sheet=sheet

  @commands.command()
  @commands.cooldown(rate=1,per=8,type=commands.BucketType.guild)
  async def bump(self,ctx,member:discord.Member=None):
    '''A command for you to use to make your mark
  Usage:
  q!bump --> adds a bump
  q!bump <member mention or id> --> gets the number of times you have bumped'''
    if member==None:
      try:
        author=self.sheet.find(str(ctx.author.id))
        cell=self.sheet.cell(author.row,author.col+1)
        self.sheet.update_cell(cell.row,cell.col,str(int(cell.value)+1))
        await ctx.send(ctx.author.mention+", you have successfully bumped!")
      except gspread.exceptions.CellNotFound:
        self.sheet.append_row([ctx.author.name,str(ctx.author.id),'1','0','0'])
        await ctx.send(ctx.author.mention+", you have successfully bumped for the first time!")
    else:
      try:
        author=self.sheet.find(str(member.id))
        cell=self.sheet.cell(author.row,author.col+1)
        await ctx.send(ctx.author.mention+", "+member.name+" has bumped "+cell.value+" times.")
      except gspread.exceptions.CellNotFound:await ctx.send(ctx.author.mention+", "+member.name+" has bumped 0 times.")

  @commands.command(aliases=['daily'])
  @commands.cooldown(rate=1,per=8,type=commands.BucketType.default)
  async def dailies(self,ctx):
    '''Claim your daily credits
  Usage:
  q![dailies|daily]'''
    async with ctx.typing():
      try:
        author=self.sheet.find(str(ctx.author.id))
        cell=self.sheet.cell(author.row,author.col+2)
        self.sheet.update_cell(cell.row,cell.col,str(int(cell.value)+200))
        a=datetime.datetime.now().timestamp()
        if a-float(self.sheet.cell(author.row,author.col+3).value)>43200:
          await ctx.send("You have claimed your 200 dailies! \U0001F4B0 \nClaim your dailies in 12 hours!")
          self.sheet.update_cell(author.row,author.col+3,str(a))
        else:
          temp_time=datetime.datetime.now().timestamp()-float(self.sheet.cell(author.row,author.col+3).value)
          time_left=int(43200-temp_time)
          await ctx.send("Please wait {} hours, {} minutes and {} seconds to collect your dailies!".format(time_left//3600,(time_left//60-time_left//3600*60),(time_left%60)),delete_after=4)
      except gspread.exceptions.CellNotFound:
        self.sheet.append_row([ctx.author.name,str(ctx.author.id),'0','200','0'])
        await ctx.send("You have claimed your 200 dailies! \U0001F4B0 \nClaim your dailies in 12 hours!")
    
def setup(bot):
    bot.add_cog(Database(bot))
