import config
import discord, time, os

intents = discord.Intents.default()
intents.message_content = True

class Loggers(discord.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
        await self.change_presence(status=discord.Status.idle, activity=discord.Game('CUTTING LOGS'))

bot = Loggers(intents=intents)

@bot.slash_command(description="Description of the bot and a link to the github repo")
async def help(
        ctx : discord.ApplicationContext
):
    em = discord.Embed(title = "Help", description = "Get your logs with loggers !")
    em.set_thumbnail(url="https://camo.githubusercontent.com/c8371bbfb15c624f16412966cd39a59bb30c29286ceb66f3e03677ca410f65af/68747470733a2f2f692e6b796d2d63646e2e636f6d2f70686f746f732f696d616765732f6e657773666565642f3030312f3933362f3733312f3934622e706e67")
    em.add_field(name = "Full info at", value = "https://github.com/ajuelosemmanuel/Loggers")
    await ctx.respond(embed = em)

@bot.slash_command(description="Sends the name of each server to which the bot is connected")
async def servers(
        ctx : discord.ApplicationContext
):
        if ctx.author.id not in config.userId:
            await ctx.respond("You are not allowed to use this command...")
        elif len(bot.guilds) == 0:
            await ctx.respond("The bot isn't connected to any server")
        else:
            ans = "Connected on : \n"
            for s in bot.guilds :
                ans += s.name+"\n"
            await ctx.respond(ans)

@bot.slash_command(description="Sends a list of the textual channels to which the bot has access")
async def channels_of(
        ctx : discord.ApplicationContext,
        serv_name : discord.Option(str, "Name of the server")
):
    if ctx.author.id not in config.userId:
        await ctx.respond("You are not allowed to use this command...")
    else:
        srv = None
        for server in bot.guilds:
            if server.name == serv_name:
                srv = server
        if srv is None:
            await ctx.respond("Couldn't find the server. Make sure you typed it correctly, or that the bot is connected to it.")
        elif len(srv.text_channels) == 0:
                await ctx.respond("Couldn't find any textual channel in the server. Maybe the bot isn't allowed to have access to those.")
        else:
            ans = "Channels of " + srv.name + " : \n"
            for chan in srv.text_channels :
                ans += chan.name+"\n"
            await ctx.respond(ans)

@bot.slash_command(description="Sends the last l messages from a given channel of a given server. Supports embeds and media")
async def loggers(
        ctx : discord.ApplicationContext,
        serv_name : discord.Option(str, "Name of the server"),
        chan_name : discord.Option(str, "Name of the channel"),
        txt : discord.Option(bool, "Send a txt file instead of sending messages (slowly but surely !)", default=False) = False,
        l : discord.Option(int, "Number of messages to gather", default=1000, min_value=1, max_value= 1000) = 1000
    ):
    l=int(l)
    if ctx.author.id not in config.userId:
        await ctx.respond("You are not allowed to use this command...")
    else:
        srv = None
        for server in bot.guilds:
            if server.name == serv_name:
                srv = server
        if srv is None:
            await ctx.respond("Couldn't find the server. Make sure you typed it correctly, or that the bot is connected to it.")
        elif len(srv.text_channels) == 0:
            await ctx.respond("Couldn't find any textual channel in the server. Maybe the bot isn't allowed to have access to those.")
        else:
            for chan in srv.text_channels:
                if chan.name == chan_name:
                    msgList = []
                    if not txt:
                        await ctx.respond("-----------------------------------------------") 
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
                        await ctx.respond(file=discord.File('./logs.txt'))
                        os.remove("logs.txt")

bot.run(config.token)
