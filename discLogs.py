import discord, time, os
from discord.ext import commands
from config import token, userId

client = commands.Bot(command_prefix = '.')
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Cutting LOGS'))
    print("[Bot Status] Bot is now ON.")

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Prefix : . ")
    em.set_thumbnail(url="https://camo.githubusercontent.com/c8371bbfb15c624f16412966cd39a59bb30c29286ceb66f3e03677ca410f65af/68747470733a2f2f692e6b796d2d63646e2e636f6d2f70686f746f732f696d616765732f6e657773666565642f3030312f3933362f3733312f3934622e706e67")
    em.add_field(name = "servers", value = "Usage : .servers")
    em.add_field(name = "channelsOf", value = "Usage : .channelsOf servName")
    em.add_field(name = "loggers", value = "loggers servName chanName (txt=False) (l=1000)")
    em.add_field(name = "Full info at", value = "https://github.com/ajuelosemmanuel/Loggers")
    await ctx.send(embed = em)

@client.command()
async def servers(ctx):
    for s in client.guilds :
        await ctx.send(f"Connected on : {s.name}")

@client.command()
async def channelsOf(ctx, servName):
    for server in client.guilds:
        if server.name == servName:
            srv = server
    await ctx.send(f"Channels of {srv.name}")
    for chan in srv.text_channels:
        await ctx.send(chan.name)

@client.command()
async def loggers(ctx, servName, chanName, txt = False, l=1000):
    if ctx.author.id not in userId:
        return
    else:
        for server in client.guilds:
            if server.name == servName:
                srv = server
        for chan in srv.text_channels:
            if chan.name == chanName:
                msgList = []
                if not txt:
                    await ctx.send("-----------------------------------------------") 
                    async for lm in chan.history(limit=l):
                            msgList.append(lm)
                    msgList.reverse()
                    for lm in msgList:
                        msg =  lm.created_at.strftime("%d/%m/%Y") + ' at ' + lm.created_at.strftime("%H:%M:%S") + ' || ' + lm.author.name + ' : ' + lm.content 
                        await ctx.send(msg) 
                        if len(lm.embeds) != 0:
                            for el in lm.embeds:
                                await ctx.send(embed = el)
                        if len(lm.attachments) != 0:
                            for el in lm.attachments:
                                await ctx.send(el.url)
                else:
                    logFile = open("logs.txt","a")
                    time.sleep(1)
                    async for lm in chan.history(limit=l):
                            msgList.append(lm)
                    msgList.reverse()
                    for lm in msgList:
                        msg =  lm.created_at.strftime("%d/%m/%Y") + ' at ' + lm.created_at.strftime("%H:%M:%S") + ' || ' + lm.author.name + ' : ' + lm.content + '\n'
                        logFile.write(msg)
                        time.sleep(2)
                        if len(lm.attachments) != 0:
                            for el in lm.attachments:
                                logFile.write(el.url)
                                time.sleep(2)
                    time.sleep(10)
                    logFile.close()
                    await ctx.send(file=discord.File('./logs.txt'))
                    os.remove("logs.txt")

client.run(token)