import discord
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
    em.add_field(name = "servers", value = "Usage : .servers | sends the name of each server the bot is in")
    em.add_field(name = "channelsOf", value = "Usage : .channelsOf servName | sends the name of each text channel the bot can access on a given server")
    em.add_field(name = "loggers", value = "loggers servName chanName (l=1000) | sends the last l (default : 1000) messages from a given channel of a given server. Supports embeds and media")
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
async def loggers(ctx, servName, chanName, l=1000):
    if ctx.author.id not in userId:
        return
    else:
        for server in client.guilds:
            if server.name == servName:
                srv = server
        for chan in srv.text_channels:
            if chan.name == chanName:
                msgList = []
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

client.run(token)