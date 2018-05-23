import asyncio,discord,math,random,time,datetime,aiohttp,functools,inspect,re
from discord.ext import commands
import urllib.request
import urllib.parse
from googlesearch import search
blacklisted=[]
def tdm(td):
        return ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)

owner_id=360022804357185537
bot_id=384623978028859392
prefixes=('q!', 'q>', 'q<', 'q+', 'q-', 'q*', 'q/', 'q?', 'q.', 'q,', 'q:', 'q;','Q!', 'Q>', 'Q<', 'Q+', 'Q-', 'Q*', 'Q/', 'Q?', 'Q.', 'Q,', 'Q:', 'Q;', 'quantum ', 'quantuM ', 'quantUm ', 'quantUM ', 'quanTum ', 'quanTuM ', 'quanTUm ', 'quanTUM ', 'quaNtum ', 'quaNtuM ', 'quaNtUm ', 'quaNtUM ', 'quaNTum ', 'quaNTuM ', 'quaNTUm ', 'quaNTUM ', 'quAntum ', 'quAntuM ', 'quAntUm ', 'quAntUM ', 'quAnTum ', 'quAnTuM ', 'quAnTUm ', 'quAnTUM ', 'quANtum ', 'quANtuM ', 'quANtUm ', 'quANtUM ', 'quANTum ', 'quANTuM ', 'quANTUm ', 'quANTUM ', 'qUantum ', 'qUantuM ', 'qUantUm ', 'qUantUM ', 'qUanTum ', 'qUanTuM ', 'qUanTUm ', 'qUanTUM ', 'qUaNtum ', 'qUaNtuM ', 'qUaNtUm ', 'qUaNtUM ', 'qUaNTum ', 'qUaNTuM ', 'qUaNTUm ', 'qUaNTUM ', 'qUAntum ', 'qUAntuM ', 'qUAntUm ', 'qUAntUM ', 'qUAnTum ', 'qUAnTuM ', 'qUAnTUm ', 'qUAnTUM ', 'qUANtum ', 'qUANtuM ', 'qUANtUm ', 'qUANtUM ', 'qUANTum ', 'qUANTuM ', 'qUANTUm ', 'qUANTUM ', 'Quantum ', 'QuantuM ', 'QuantUm ', 'QuantUM ', 'QuanTum ', 'QuanTuM ', 'QuanTUm ', 'QuanTUM ', 'QuaNtum ', 'QuaNtuM ', 'QuaNtUm ', 'QuaNtUM ', 'QuaNTum ', 'QuaNTuM ', 'QuaNTUm ', 'QuaNTUM ', 'QuAntum ', 'QuAntuM ', 'QuAntUm ', 'QuAntUM ', 'QuAnTum ', 'QuAnTuM ', 'QuAnTUm ', 'QuAnTUM ', 'QuANtum ', 'QuANtuM ', 'QuANtUm ', 'QuANtUM ', 'QuANTum ', 'QuANTuM ', 'QuANTUm ', 'QuANTUM ', 'QUantum ', 'QUantuM ', 'QUantUm ', 'QUantUM ', 'QUanTum ', 'QUanTuM ', 'QUanTUm ', 'QUanTUM ', 'QUaNtum ', 'QUaNtuM ', 'QUaNtUm ', 'QUaNtUM ', 'QUaNTum ', 'QUaNTuM ', 'QUaNTUm ', 'QUaNTUM ', 'QUAntum ', 'QUAntuM ', 'QUAntUm ', 'QUAntUM ', 'QUAnTum ', 'QUAnTuM ', 'QUAnTUm ', 'QUAnTUM ', 'QUANtum ', 'QUANtuM ', 'QUANtUm ', 'QUANtUM ', 'QUANTum ', 'QUANTuM ', 'QUANTUm ', 'QUANTUM ')
bot = commands.Bot(description='Tune in to lots of fun with this bot!', command_prefix=prefixes)
class Math:
    '''for mathematical fun'''
    @commands.command()
    async def add(self, ctx,*,nums):
        '''returns sum of numbers separated with spaces'''
        try:
            await ctx.send(str(sum([int(i) for i in nums.split()])))
        except:
            await ctx.send("You didn't give the correct arguments.")
 
    @commands.command()
    async def mul(self, ctx,*,nums):
        '''returns product of arguments separated with spaces'''
        try:
            m=lambda x,y:x*y
            await ctx.send(str(functools.reduce(m,[int(i) for i in nums.split()])))
        except:
            await ctx.send("You didn't give the correct arguments.")
 
    @commands.command()
    async def factorial(self,ctx,num:int):
            '''returns the factorial of the given input'''
            try:
                    await ctx.send(embed=discord.Embed(title="%d! is equal to..."%num,description=str(math.factorial(num))))
            except Exception as p:
                    await ctx.send(embed=discord.Embed(title=type(p)+" raised!",description=p.args[1]))
class Admin:
    '''for administrative purposes'''
    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        '''Kick members from your server'''
        try:
                await member.kick()
                await ctx.message.add_reaction('\u2705')
        except:
                await ctx.message.add_reaction('\u274C')
    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        '''Ban toxic members from your server'''
        try:
                await member.ban()
                await ctx.message.add_reaction('\u2705')
        except:
                await ctx.message.add_reaction('\u274C')
 
    @commands.command(aliases=['ar','updaterole'])
    async def changerole(self,ctx,member:discord.Member,role:discord.Role):
        '''to add/remove a role from a person'''
        try:
            if role not in member.roles:await ctx.author.add_roles(role)
            else:await ctx.author.remove_roles(role)
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')
class General:
    '''commands available for everyone'''           
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        '''Call the bot'''
        msg = await ctx.send('Pong!')
        res = msg.created_at - ctx.message.created_at
        res = tdm(res)
        lat = bot.latency*1000
        await msg.edit(content='Pong! :ping_pong: Bot response time: {}ms\nDiscord latency: {}ms'.format(res,round(lat,1)))
 
    @commands.command()
    async def say(self, ctx, *, something='Quantum Bot here!!'):
        '''The bot becomes your copycat'''
        await ctx.send(something)
        await ctx.message.delete()
 
    @commands.command()
    async def now(self, ctx):
        '''Get current date and time'''
        m = str(datetime.datetime.now()).split()
        embed=discord.Embed(title="Date-time information",color=eval(hex(ctx.author.color.value)))
        embed.add_field(name="Date",value="{}".format(m[0]))
        embed.add_field(name="Time",value="{}GMT".format(m[1]))
        await ctx.send(embed=embed)
 
    @commands.command(aliases=['fb'])
    async def feedback(self,ctx,*,message):
        '''My bot is not very good, feedback is appreciated!'''
        author=ctx.message.author.name+" said in "+"'"+ctx.guild.name+"'"
        await bot.get_guild(413290013254615041).get_channel(413631317272690688).send(embed=discord.Embed(color=eval(hex(ctx.author.color.value)),title=author,description="#"+ctx.channel.name+":\n"+message))
        await ctx.message.add_reaction('\u2705')

    @commands.command(aliases=['p'])
    async def poll(self,ctx,*,question):
        '''whenever you need opinions, use this!'''
        await ctx.send('This command will work in the future :)')
class Information:
    '''To know more about the bot'''
    @commands.command()
    async def botinfo(self, ctx):
        '''some stats about the bot'''
        serv = len(bot.guilds)
        membs = len(bot.users)
        creator = "Pegasus#4022"
        date = f"{bot.user.created_at: %B %d, %Y at %H:%M:%S GMT}"
        await ctx.send("Servers streaming: {}\nUsers streaming: {}\nCreator: {}\nCreation date: {}".format(serv,membs,creator,date))
 
    @commands.command()
    async def prefix(self, ctx):
        '''list of all prefixes my bot uses'''
        await ctx.send("```"+",".join(prefixes)+"```")
        await ctx.send(str(len(prefixes))+" prefixes! :joy:")
 
    @commands.command()
    async def invite(self, ctx):
        '''link to invite my bot elsewhere'''
        await ctx.send(embed=discord.Embed(title="Bot invite+Official server",description="This is my bot invite:\nhttps://discordapp.com/oauth2/authorize?client_id=384623978028859392&scope=bot&permissions=2146958591\nPlease consider joining this server too:https://discord.gg/ngaC2Bh",color=eval(hex(ctx.author.color.value))))
 
    @commands.command()
    async def getpeople(self,ctx,*,rolename=None):
            '''find all people with a particular role name,bolding means that that is the user's top role'''
            people=[]
            role=discord.utils.get(ctx.guild.roles,name=rolename)
            for i in role.members:
                if i.top_role==role:
                    people.append("**"+i.name+"**")
                else:
                    people.append(i.name)
            if len(people)>80:
                content="More than 80 people have this role. I'd rather not state all the people with this role"
            else:
                content=",".join(people)
            await ctx.send(embed=discord.Embed(title="People with the role '%s'"%role.name,color=eval(hex(ctx.author.color.value)),description=content))
 
    @commands.command()
    async def serverinfo(self,ctx):
            '''get more info on the server'''
            members=len(ctx.guild.members)
            owner=ctx.guild.owner
            created=f"{ctx.guild.created_at: %B %d, %Y at %H:%M:%S GMT}"
            server=ctx.guild.name
            sid=ctx.guild.id
            ver=["None","Low","Medium","High","Ultra High"][ctx.guild.verification_level]
            region=ctx.guild.region
            await ctx.send(embed=discord.Embed(color=discord.Color(0x000000),title="Server Info:",description="""Server Name:{}\nServer Id:{}\n
Server Region:{}\nMember count:{}\nOwner:{}\nCreated On:{}\nVerification Level={}""".format(server,sid,region,members,owner,created,ver)))
             
    @commands.command(pass_context=True)
    async def perms(self,ctx,user:discord.Member=None):
        '''find what you can do on this server'''
        user =  ctx.message.author if user is None else user
        if not user:
                user=ctx.author
        mess=[]
        for i in user.guild_permissions:
                if i[1]:
                        mess.append("\u2705 {}".format(i[0]))
                else:
                        mess.append("\u274C {}".format(i[0]))
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0xFF0000),title=user.name+" guild permissions",description="\n".join(mess)))
     
    @commands.command()
    async def roleperms(self,ctx,role:discord.Role=None):
        '''gets the server permissions of a role'''
        role=ctx.author.top_role if role is None else role
        mess=[]
        for i in role.permissions:
            if i[1]:
                    mess.append("\u2705 {}".format(i[0]))
            else:
                    mess.append("\u274C {}".format(i[0]))
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0xFF0000),title=role.name+" guild permissions",description="\n".join(mess)))
 
    @commands.command()    
    async def permcheck(self,ctx,perm='all_perms',user:discord.Member=None):
        '''checks specific permissions,type all_perms/leave empty for full list'''
        user=ctx.message.author if user is None else user
        permlist=dict(user.guild_permissions)
        if perm=='all_perms':
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x000000),title="All permissions listed",description="\n".join(dict(user.guild_permissions).keys())))
                return "\n".join(dict(user.guild_permissions).keys())
        await ctx.send(permlist[perm]*"\u2705"+(1-permlist[perm])*"\u274C")
        return permlist[perm]
 
    @commands.command(aliases=["h"])
    async def help(self,ctx):
        '''bot help message'''
        command_list={}
        message={}
        for i in bot.cogs.keys():
                if i!='REPL':command_list.update({i:(m for m in dir(bot.get_cog(i))[26:])})
                else:command_list.update({'REPL':('exec','repl')})
        for i in bot.commands:
                f=inspect.getsource(bot.get_command(str(i)).callback)
                message.update({str(i):f.split("\n")[2].strip()[3:-3]})
        em=discord.Embed(title="Quantum Bot Help Message",color=eval(hex(ctx.author.color.value)))
        for i in command_list.keys():
                em.add_field(name=i+" help",value="\n".join(["**_"+m+"_**"+": "+message[m] for m in command_list[i]]),inline=False)
        await ctx.send(embed=em)
        
    @commands.command(aliases=["chelp","ch"])
    async def coghelp(self,ctx,cog:str=None):
        '''to get specific help messages from specific cogs'''
        command_list={}
        message={}
        for i in bot.cogs.keys():
                if i!='REPL':command_list.update({i:(m for m in dir(bot.get_cog(i))[26:])})
                else:command_list.update({'REPL':('exec','repl')})
        for i in bot.commands:
                f=inspect.getsource(bot.get_command(str(i)).callback)
                message.update({str(i):f.split("\n")[2].strip()[3:-3]})
        if cog.lower() in list(map(lambda x:x.lower(),list(bot.cogs.keys()))):
                em=discord.Embed(title=cog+" Help Message",color=eval(hex(ctx.author.color.value)),description="\n".join([("**_"+m+"_**"+": "+message[m] if m!="_eval" else "**_exec_**"+": "+message[m]) for m in dir(bot.get_cog(cog))[26:]]),inline=False)
        elif cog==None:
                em=discord.Embed(title="List of cogs",color=eval(hex(ctx.author.color.value)),description="\n".join([i for i in bot.cogs.keys()]))
        else:
                em=discord.Embed(title="Invalid Arguments passed",color=eval(hex(ctx.author.color.value)),description="No such cog called '"+cog+"' found.")
        await ctx.send(embed=em)
             
class Fun:
    '''have fun with these commands'''
    @commands.command()
    async def dice(self, ctx, times=1):
        '''Roll a dice as many times as you like'''
        total = []
        for i in range(times):
            total.append(random.randint(1, 6))
        botmessage = (('Numbers:' + ','.join([str(i) for i in total])) + '\nTheir sum:') + str(sum(total))
        await ctx.send(botmessage)
        
    @commands.command()
    async def xkcd(self, ctx, num=None):
        '''read the famous comic strip'''
        try:
            async with ctx.typing():
                if num is None:num=random.randint(1,1996)
                url = f'https://xkcd.com/{num}/info.0.json'
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        f = await response.json(encoding='utf8')
                m=discord.Embed(colour=discord.Color.from_rgb(245,245,220),title="xkcd #{}:{}".format(str(f['num']),f['safe_title']),description=f['transcript'],timestamp=datetime.datetime.now())
                m.set_image(url=f['img'])
                m.add_field(name="Links",value=f['img']+'\nhttps://xkcd.com/'+str(f['num']))
                m.add_field(name="Publication date:",value=f['day']+'/'+f['month']+'/'+f['year'],inline=False)
            await ctx.send(embed=m)
        except:
            if num=404:await ctx.send("Think again, does it exist?")
            else:
                await ctx.send("Fetching your a random xkcd comic...",delete_after=2)
                async with ctx.typing():
                    num=random.randint(1,1996)
                    url = f'https://xkcd.com/{num}/info.0.json'
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            f = await response.json(encoding='utf8')
                    m=discord.Embed(colour=discord.Color.from_rgb(245,245,220),title="xkcd #{}:{}".format(str(f['num']),f['safe_title']),description=f['transcript'],timestamp=datetime.datetime.now())
                    m.set_image(url=f['img'])
                    m.add_field(name="Links",value=f['img']+'\nhttps://xkcd.com/'+str(f['num']))
                    m.add_field(name="Publication date:",value=f['day']+'/'+f['month']+'/'+f['year'],inline=False)
                await ctx.send(embed=m)

    @commands.command()
    async def think(self,ctx):
        '''let the bot think for a while'''
        await ctx.message.delete()
        await ctx.send(discord.utils.get(bot.emojis,name='fidgetthink'))

        
    @commands.command()
    async def emojify(self, ctx, *, text='Hello'):
        '''all *English* letters and numbers turn into emojis!'''
        nums={'0':':zero:','1':':one:','2':':two:',"3":":three:","4":":four:","5":":five:","6":":six:","7":":seven:","8":":eight:","9":":nine:","!":":grey_exclamation:","?":":grey_question:"}
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
    async def emojirep(self, ctx,emoji:discord.Emoji ,number=1):
        '''[WIP] repeats a given emoji with input'''
        try:
                if number<1 or number>10:await ctx.send("Stop being enthusiastic!")
                else:await ctx.send((discord.Emoji(emoji.id))*number)
        except:await ctx.send("Error ocurred!")

    @commands.command(aliases=["f","respect"])
    async def rip(self, ctx, member:discord.Member=None):
        '''Rest in piece, my comrade'''
        if member is None:member=ctx.author
        elif member.id==owner_id or member.id==bot_id:member=ctx.author
        embed=discord.Embed(title="RIP {}{}".format(member.name,discord.utils.get(bot.emojis,name="rip")),description="Press :regional_indicator_f: to pay your respects",colour=discord.Colour.from_rgb(255,255,255))
        embed.set_thumbnail(url=member.avatar_url)
        p=await ctx.send(embed=embed)
        await p.add_reaction(discord.utils.get(bot.emojis,name="f_"))

    @commands.command()
    async def playing(self, ctx):
        '''returns the current bot status'''
        async with ctx.typing():
            embed=discord.Embed(title="Quantum Bot's status:",description=ctx.guild.get_member(bot_id).activity.name)
            embed.set_thumbnail(url=ctx.guild.get_member(bot_id).avatar_url)
        await ctx.send(embed=embed)
        
class Owner:
    '''commands only the bot owner can use, besides repl and exec'''
    @commands.command(pass_context=True)
    async def shutdown(self, ctx):
        '''for me to close the bot'''
        if ctx.message.author.id!=owner_id:
            await ctx.send("You're not the bot owner!")
        else:
            await ctx.send("Shutting down...")
            await bot.logout()
 
    @commands.command()
    async def clear(self, ctx, number=2, author:discord.Member=None):
        '''[WIP] clears messages from a channel, if you're allowed'''
        allowed = [360022804357185537, 270149861398151169]
        if ctx.author.id in allowed:
            if author is not None:
                    check=lambda x:x.author==author
                    await ctx.channel.purge(limit=number,check=check)
            else:await ctx.channel.purge(limit=number)
        else:
            await ctx.send("You're not approved by the bot owner to delete stuff!")
 
    @commands.command()
    async def getsource(self, ctx, command):
        '''getting the code for command'''
        if ctx.author.id==owner_id:
            a=inspect.getsource(bot.get_command(command).callback)
        else:
            a="You are not the owner! Not allowed!"
        await ctx.send("```"+a+"```")
         
    @commands.command(pass_context=True)
    async def warn(self,ctx,member:discord.Member,serious:bool,*,reason):
            '''for owner to issue warnings'''
            if ctx.author.id==owner_id:
                if serious:
                    await ctx.guild.get_member(member.id).send(embed=discord.Embed(title="Warning! [SERIOUS]",description="**My bot owner warned your because**:{}".format(reason),colour=discord.Colour(0xFF0000)))
                else:
                    await ctx.guild.get_member(member.id).send(embed=discord.Embed(title="Warning!",description="**My bot owner warned your because**:{}".format(reason),colour=discord.Colour(0xFFFF00)))
                await ctx.message.add_reaction('\u2705')
                         
                     
    @commands.command()
    async def blacklist(self,ctx,member:discord.Member=None):
            '''[WIP] to prevent bad people from misusing my bot'''
            global blacklisted
            if member==None:
                    return ("\n".join([f.name for f in blacklisted]) if len(blacklisted)>0 else "Nobody blacklisted yet")
            else:
                    blacklisted.append(member)
    @commands.command()
    async def pydir(self,ctx,command=None):
            '''list of methods of a given object'''
            if ctx.message.author.id!=owner_id:
                await ctx.send(embed=discord.Embed(title="Error message",color=eval(hex(ctx.author.color.value)),description="Not allowed!"))
            else:                
                if command is None:await ctx.send("Argument [command name] must be provided!")
                else:
                    try:
                        dire=[]
                        a=eval("dir("+command+")")
                        for i in a:
                            if i[0]!="_":
                                dire.append("**"+i+"**")
                            elif i[1]!="_":
                                dire.append(i)
                        content=",".join(dire)
                    except NameError:
                        content="Object %s is not found!"%command
                await ctx.send(embed=discord.Embed(title="Useful methods for object '%s'"%command,color=eval(hex(ctx.author.color.value)),description=content))
     
 
class Media:
    @commands.command(passcontext=True)
    async def youtube(self, ctx, *, youtube):
        '''Searches youtube videos with inputted queries'''
        embed=discord.Embed(title="Youtube search for "+youtube,color=eval(hex(ctx.author.color.value)))
        try:
                query_string = urllib.parse.urlencode({'search_query': youtube,})
                html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
                search_results = re.findall('href=\\"\\/watch\\?v=(.{11})', html_content.read().decode())
                if len(search_results)>=3:
                        embed.add_field(name="Top result",value='http://www.youtube.com/watch?v=' + search_results[0])
                        embed.add_field(name="Other results",value='http://www.youtube.com/watch?v=' + search_results[1]+"\n"+'http://www.youtube.com/watch?v=' + search_results[2])
                else:
                        embed.add_field(name="Top result",value='http://www.youtube.com/watch?v=' + search_results[0])
        except:
                embed.add_field(name="Error",value="Your request did not produce any output. Perhaps try searching a different query?")
        finally:
                await ctx.send(embed=embed)
                
    @commands.command()
    async def google(self, ctx, *, anything):
            """: Search Google for something, experimental"""
            content=[]
            async with ctx.typing():
                for url in search(anything, tld='com', lang='en',start=1,stop=10):
                    content.append(url)
            await ctx.send(embed=discord.Embed(title="'%s' search results:'"%anything,description="\n".join(content),colour=discord.Colour.from_rgb(66, 133, 244)))

@bot.event
async def on_ready():
    bot.remove_command('help')
    bot.load_extension('code2')
    bot.add_cog(Owner())
    bot.add_cog(Information())
    bot.add_cog(Admin())
    bot.add_cog(Math())
    bot.add_cog(General())
    bot.add_cog(Fun())
    bot.add_cog(Media())
    await bot.change_presence(activity=discord.Game(name='Type [q?help] for help', type=2),status=discord.Status.dnd)
    f=bot.get_guild(413290013254615041).get_channel(436548366088798219)
    await f.send(embed=discord.Embed(title="Bot reawakened at: ",description=f"{datetime.datetime.now(): %B %d, %Y at %H:%M:%S GMT}"))
    async def change_activities():
        timeout = 10 #Here you can change the delay between changes 
        while True:
            possb='Type [{}help] for help'.format(random.choice(bot.command_prefix))
            await bot.change_presence(activity=discord.Game(possb,status=discord.Status.dnd))
            await asyncio.sleep(timeout)
    bot.loop.create_task(change_activities())
bot.run('Mzg0NjIzOTc4MDI4ODU5Mzky.DZecOA.rekvrUSZL8q9QVzlIlnoS0lNYVI')
#ok
