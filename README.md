# Loggers
<img src="https://i.kym-cdn.com/photos/images/newsfeed/001/936/731/94b.png" width = 250>

Discord bot to gather every message from a text channel

## Commands
Prefix : .

+ servers : sends the name of each server the bot is in
+ channelsOf servName : sends the name of each text channel the bot can access on a given server
+ loggers servName chanName (txt=False) (l=1000) : sends the last l (default : 1000) messages from a given channel of a given server. Supports embeds and media. The txt argument is a boolean : will send a txt file instead of sending messages (slowly but surely !)

## Requirements

+ discord.py
+ filling up the config.py file