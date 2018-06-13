import asyncio,discord,math,random,time,datetime,aiohttp,functools,inspect,re
from discord.ext import commands
import urllib.request
import urllib.parse
from googlesearch import search
blacklisted=[]
#my own utilities
def tdm(td):
        return ((td.days * 86400000) + (td.seconds * 1000)) + (td.microseconds / 1000)

def find(substring, string):
    """ 
    Generate indices of where substring begins in string

    >>> list(find_substring('me', "The cat says meow, meow"))
    [13, 19]
    """
    last_found = -1  # Begin at -1 so the next position to search from is 0
    while True:
        # Find next index of substring, by starting after its last known position
        last_found = string.find(substring, last_found + 1)
        if last_found == -1:  
            break  # All occurrences have been found
        yield last_found

async def getjson(url):
        """
        This command helps get the json automatically without extra code
        """
        async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                        f = await response.json(encoding='utf8')
        return f
#configs
owner_id=360022804357185537
bot_id=384623978028859392
prefixes=('q!', 'q>', 'q<', 'q+', 'q-', 'q*', 'q/', 'q?', 'q.', 'q,', 'q:', 'q;','Q!', 'Q>', 'Q<', 'Q+', 'Q-', 'Q*', 'Q/', 'Q?', 'Q.', 'Q,', 'Q:', 'Q;', 'quantum ', 'quantuM ', 'quantUm ', 'quantUM ', 'quanTum ', 'quanTuM ', 'quanTUm ', 'quanTUM ', 'quaNtum ', 'quaNtuM ', 'quaNtUm ', 'quaNtUM ', 'quaNTum ', 'quaNTuM ', 'quaNTUm ', 'quaNTUM ', 'quAntum ', 'quAntuM ', 'quAntUm ', 'quAntUM ', 'quAnTum ', 'quAnTuM ', 'quAnTUm ', 'quAnTUM ', 'quANtum ', 'quANtuM ', 'quANtUm ', 'quANtUM ', 'quANTum ', 'quANTuM ', 'quANTUm ', 'quANTUM ', 'qUantum ', 'qUantuM ', 'qUantUm ', 'qUantUM ', 'qUanTum ', 'qUanTuM ', 'qUanTUm ', 'qUanTUM ', 'qUaNtum ', 'qUaNtuM ', 'qUaNtUm ', 'qUaNtUM ', 'qUaNTum ', 'qUaNTuM ', 'qUaNTUm ', 'qUaNTUM ', 'qUAntum ', 'qUAntuM ', 'qUAntUm ', 'qUAntUM ', 'qUAnTum ', 'qUAnTuM ', 'qUAnTUm ', 'qUAnTUM ', 'qUANtum ', 'qUANtuM ', 'qUANtUm ', 'qUANtUM ', 'qUANTum ', 'qUANTuM ', 'qUANTUm ', 'qUANTUM ', 'Quantum ', 'QuantuM ', 'QuantUm ', 'QuantUM ', 'QuanTum ', 'QuanTuM ', 'QuanTUm ', 'QuanTUM ', 'QuaNtum ', 'QuaNtuM ', 'QuaNtUm ', 'QuaNtUM ', 'QuaNTum ', 'QuaNTuM ', 'QuaNTUm ', 'QuaNTUM ', 'QuAntum ', 'QuAntuM ', 'QuAntUm ', 'QuAntUM ', 'QuAnTum ', 'QuAnTuM ', 'QuAnTUm ', 'QuAnTUM ', 'QuANtum ', 'QuANtuM ', 'QuANtUm ', 'QuANtUM ', 'QuANTum ', 'QuANTuM ', 'QuANTUm ', 'QuANTUM ', 'QUantum ', 'QUantuM ', 'QUantUm ', 'QUantUM ', 'QUanTum ', 'QUanTuM ', 'QUanTUm ', 'QUanTUM ', 'QUaNtum ', 'QUaNtuM ', 'QUaNtUm ', 'QUaNtUM ', 'QUaNTum ', 'QUaNTuM ', 'QUaNTUm ', 'QUaNTUM ', 'QUAntum ', 'QUAntuM ', 'QUAntUm ', 'QUAntUM ', 'QUAnTum ', 'QUAnTuM ', 'QUAnTUm ', 'QUAnTUM ', 'QUANtum ', 'QUANtuM ', 'QUANtUm ', 'QUANtUM ', 'QUANTum ', 'QUANTuM ', 'QUANTUm ', 'QUANTUM ')
bot = commands.Bot(description='Tune in to lots of fun with this bot!', command_prefix=commands.when_mentioned_or(*prefixes))
#commands
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

    @commands.command()
    async def collatz(self,ctx,num:int):
        '''dedicated to the famous conjecture, will return the steps from input to 1'''
        nums=[num]
        last=num
        while last>1:
            if last%2==0:last//=2
            else:last=last*3+1
            nums.append(last)
        nums=list(map(str,nums))
        ranhex=random.randint(0,255)
        await ctx.send(embed=discord.Embed(title="Collatzing your way through %d"%num,description=",".join(nums),colour=discord.Colour.from_rgb(ranhex,ranhex,ranhex)))
        
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
        await msg.edit(content='Pong! :ping_pong:\nBot response time: {}ms\nDiscord latency: {}ms'.format(res,round(lat,1)))
 
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
        
class Feedback: 
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

    @commands.command()
    async def suggest(self,ctx,command,*,description):
        '''suggest commands I should work on, and follow by a short description on how it works'''
        author=ctx.message.author.name
        m=await bot.get_guild(413290013254615041).get_channel(413631317272690688).send(embed=discord.Embed(title=author+" suggested a command '"+command+"'",description=description,color=ctx.author.color))
        await m.add_reaction("\u2705")
        await m.add_reaction("\u274C")
        r=await bot.wait_for('reaction_add',check=lambda reaction,author:(author.id==owner_id) and (reaction.emoji in ["\u2705","\u274C"]))
        if r[0].emoji=="\u2705":
            await ctx.author.send("Your command {} has been accepted by the owner.".format(command))
            await m.edit(embed=discord.Embed(title="Command to work on: "+command,description=description))
        elif r[0].emoji=="\u274C":
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
        await ctx.send("Servers streaming: {}\nUsers streaming: {}\nCreator: {}\nCreation date: {}".format(serv,membs,creator,date))
 
    @commands.command()
    async def prefix(self, ctx):
        '''list of all prefixes my bot uses'''
        prefixlist=tuple(["@Quantum Bot"]+list(prefixes))
        await ctx.send("```"+",".join(list(prefixlist))+"```"+'\n'+str(len(prefixlist))+" prefixes! :joy:")
 
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
            embed=discord.Embed(color=discord.Color(0x000000),title="Server Info:",description="""Server Name:{}\nServer Id:{}\n
Server Region:{}\nMember count:{}\nOwner:{}\nCreated On:{}\nNumber of text channels:{}\nNumber of voice channels:{}\nVerification Level={}""".format(server,sid,region,members,owner,created,len(ctx.guild.text_channels),len(ctx.guild.voice_channels),ver))
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
             
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
        embeds=[]
        for i in bot.cogs.keys():
                if i!='REPL':command_list.update({i:(m for m in dir(bot.get_cog(i))[26:])})
                else:command_list.update({'REPL':('exec','repl')})
        for i in bot.commands:
                f=inspect.getsource(bot.get_command(str(i)).callback)
                m=list(find("'''",f))
                message.update({str(i):f[m[0]+3:m[1]]})
        em=discord.Embed(title="Quantum Bot Help Message",color=eval(hex(ctx.author.color.value)))
        for i in command_list.keys():
                embed=discord.Embed(title=i+" help",inline=False,colour=ctx.author.colour)
                for m in command_list[i]:
                      embed.add_field(name=m,value=message[m],inline=False)
                embeds.append(embed)
        #till now we got the embeds, now for paginator
        info_embed=discord.Embed(title="Quantum Bot help message",description="""Please press:
        \u23EA to view the very first help message.
        \u25C0 to scroll backward
        \u23F9 to stop looking through the commands
        \u25B6 to scroll forward
        \u23E9 to view the very last help message
        \U0001f522 to search by page 
        \u2139 to view this help message""",colour=ctx.author.colour)
        curr=0
        reactions=['\u23EA','\u25C0','\u23F9','\u25B6','\u23E9','\U0001f522','\u2139']
        mess=await ctx.send(embed=info_embed)
        cogc=len(list(bot.cogs.keys()))-1
        for i in reactions:
            await mess.add_reaction(i)
        while True:
            try:
                waiting=await bot.wait_for('reaction_add',check=lambda reaction,user:(user.id==ctx.author.id) and (reaction.emoji in reactions),timeout=60)
                if waiting[0].emoji=="\u23EA":
                        curr=0
                        await mess.edit(embed=embeds[0])
                elif waiting[0].emoji=="\u25C0":
                        if curr==0:curr=cogc
                        else:curr-=1
                        await mess.edit(embed=embeds[curr])
                elif waiting[0].emoji=="\u23F9":
                        break
                elif waiting[0].emoji=="\u25B6":
                        if curr==cogc:curr=0
                        else:curr+=1
                        await mess.edit(embed=embeds[curr])
                elif waiting[0].emoji=="\u23E9":
                        curr=cogc
                        await mess.edit(embed=embeds[cogc])
                elif waiting[0].emoji=="\U0001f522":
                        await ctx.send("Select your page number (from 1 to %d)"%(cogc+1))
                        num=await bot.wait_for('message',check=lambda message:(message.content in [str(i+1) for i in range(cogc+1)]) and (message.author.id==ctx.author.id),timeout=60)
                        curr=int(num.content)-1
                        await mess.edit(embed=embeds[curr])
                elif waiting[0].emoji=="\u2139":
                        await mess.edit(embed=info_embed)
            except asyncio.TimeoutError:
                break
        await mess.edit(embed=discord.Embed(title="You have just used Quantum Bot's help message",description="Thank you!",colour=ctx.author.colour))
                 
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
            m=len(a)//1900
            for x in range(m):
                await ctx.send(embed=discord.Embed(title="Page {}/{} of '{}' command".format(x+1,m+1,command),description="```py\n"+a[1900*x:1900*(x+1)]+"```",colour=discord.Colour.dark_gold()))
            await ctx.send(embed=discord.Embed(title="Page {}/{} of '{}' command".format(m+1,m+1,command),description="```py\n"+a[1900*m:]+"```",colour=discord.Colour.dark_gold()))
        else:
            await ctx.send(embed=discord.Embed(title="Access denied!",description="This command can only be used by the bot owner!",colour=discord.Colour.red()))
         
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
            '''Search Google for something, experimental'''
            content=[]
            async with ctx.typing():
                m=await getjson("http://api.tanvis.xyz/search/"+urllib.request.pathname2url(anything))
            for i in m:
                content.append(i['link'])
            embed=discord.Embed(title="'%s' search results:"%anything,description="\n".join(content),colour=discord.Colour.from_rgb(66, 133, 244))
            embed.set_footer(text="using tanvis.xyz API")
            await ctx.send(embed=embed)

    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *, anything):
            '''look through wikipedia for what you want'''
            wew=urllib.request.urlencode(anything)
            f=getjson(f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&indexpageids=1&redirects=1&explaintext=1&exsectionformat=plain&titles={wew}")
            await ctx.send(embed=discord.Embed(title=f['title'],description=f['extract'][:max(list(filter(lambda x:x<1980,find(". ",f['extract']))))],colour=ctx.author.colour))

    @commands.command()
    async def xkcd(self, ctx, num:int=None):
        '''read the famous comic strip'''

        try:
            async with ctx.typing():
                if num is None:num=random.randint(1,1996)
                url = f'https://xkcd.com/{num}/info.0.json'
                f = await getjson(url)
                m=discord.Embed(colour=discord.Color.from_rgb(245,245,220),title="xkcd #{}:{}".format(str(f['num']),f['safe_title']),description=f['transcript'],timestamp=datetime.datetime.now())
                m.set_image(url=f['img'])
                m.add_field(name="Links",value=f['img']+'\nhttps://xkcd.com/'+str(f['num']))
                m.add_field(name="Publication date:",value=f['day']+'/'+f['month']+'/'+f['year'],inline=False)
            await ctx.send(embed=m)
        except:
            if num==404:
                m=discord.Embed(title="xkcd #404: Think again, does it exist?",description="This came between Monday and Wednesday, 2 consecutive days of xkcd comic publication. This can be considered an April Fools prank or a reference to the 404 Error: Not Found")
                m.set_image(url='https://www.explainxkcd.com/wiki/images/9/92/not_found.png')
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

    @commands.cooldown(rate=1,per=8,type=commands.BucketType.guild)
    @commands.command()
    async def weather(self,ctx,*,location):
        '''to get the weather'''
        try:
            async with ctx.typing():
                url="http://api.tanvis.xyz/weather/"+urllib.request.pathname2url(location)
                f=await getjson(url)
                if 'error' in f:
                    await ctx.send(embed=discord.Embed(title="An error occurred",description="I could not find your given location",colour=discord.Colour.red()))
                else:
                    embed=discord.Embed(title="Weather information gathered",colour=discord.Colour.dark_orange(),description="Here is your result, "+ctx.author.mention)
                    embed.add_field(name="Location",value=f['name'],inline=False);embed.add_field(name="Temperature in °C",value=f['celsius'])
                    embed.add_field(name="Temperature in °F",value=f['fahrenheit']);embed.add_field(name="Weather",value=f['weather'])
                    embed.add_field(name="Wind Speed",value=f['windSpeed']);embed.set_thumbnail(url=f['icon'])
                    embed.set_footer(text="using **tanvis.xyz** API")
                    await ctx.send(embed=embed)
        except:
                await ctx.send("An error occurred. Please try again.",delete_after=3)
# everything from here onwards are bot events

@bot.event
async def on_ready():
    bot.remove_command('help')
    bot.load_extension('code2')
    bot.add_cog(Owner())
    bot.add_cog(Information())
    bot.add_cog(Admin())
    bot.add_cog(Math())
    bot.add_cog(General())
    bot.add_cog(Feedback())
    bot.add_cog(Fun())
    bot.add_cog(Media())
    await bot.change_presence(activity=discord.Game(name='Type [q?help] for help', type=2),status=discord.Status.dnd)
    f=bot.get_guild(413290013254615041).get_channel(436548366088798219)
    await f.send(embed=discord.Embed(title="Bot reawakened at: ",description=f"{datetime.datetime.utcnow(): %B %d, %Y at %H:%M:%S GMT}"))
    async def change_activities():
        timeout = 5 #Here you can change the delay between changes 
        while True:
            possb='Type [{}help] for help'.format(random.choice(prefixes))
            await bot.change_presence(activity=discord.Game(possb,status=discord.Status.dnd))
            await asyncio.sleep(timeout)
    bot.loop.create_task(change_activities())

@bot.event
async def on_member_join(member):
    if member.guild.id==413290013254615041:
        embed=discord.Embed(title="Member join",description="Welcome to Quantum Bot and Pegasus server, "+member.name+"! Please read the rules in "+member.guild.get_channel(444443837482532867).mention+" before you proceed :)",colour=discord.Colour.from_rgb(87,242,87))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Bot",value=member.bot)
        embed.add_field(name="Member id",value=member.id)
        await member.guild.get_channel(413303508289454081).send(embed=embed)
        
@bot.event
async def on_member_remove(member):
    if member.guild.id==413290013254615041:
        embed=discord.Embed(title="Member leave",description="We're sad to see you leave, "+member.name+"! We wish you could return :(",colour=discord.Colour.from_rgb(242,23,33))
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Bot",value=member.bot)
        embed.add_field(name="Member id",value=member.id)
        await member.guild.get_channel(413303508289454081).send(embed=embed)

@bot.event
async def on_command_error(ctx,error):
    embed=discord.Embed(title=str(type(error))[8:-2],description=str(error),colour=discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    await ctx.send("***Roses are red, violets are blue, there is an error when the command is used by you***",embed=embed,delete_after=15)

@bot.event
async def on_message(message):
        #add stuff here when you want to
        await bot.process_commands(message)

@bot.event
async def on_message_edit(before,after):
        await bot.process_commands(after)
bot.run('Mzg0NjIzOTc4MDI4ODU5Mzky.DZecOA.rekvrUSZL8q9QVzlIlnoS0lNYVI')
#ok
