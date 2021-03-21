import discord
from discord.ext import commands
from config import token

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Cutting LOGS'))
    print("[Bot Status] Bot is now ON.")

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