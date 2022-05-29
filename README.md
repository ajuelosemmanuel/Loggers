# Loggers

<img src="https://i.kym-cdn.com/photos/images/newsfeed/001/936/731/94b.png" width = 250>

Discord bot to gather every message from a text channel.

It can be used for logging (by either creating txt files or writing everything in a new channel).

Another usage could be some "spying" on channels you can't read as a user : if your bot has more permissions than you, you may run this one with your bot's api key and then "read" the content of hidden channels.

## Requirements

In order to run the bot properly, you must :
+ Have [Python](https://www.python.org/downloads/) installed on your machine
+ Install the `Pycord` package :
  + On Linux : `pip install -U py-cord --pre`
  + On Windows : `python -m pip install -U py-cord --pre`
+ Fill the `config.py` file

## Commands

The available commands are :
+ `servers` :
  + Sends the name of each server to which the bot is connected.

+ `channels_of`
  + Arguments :
    + `serv_name` : Name of the server.
  + Sends a list of the textual channels to which the bot has access.

+ `channels_of`
  + Arguments :
    + `serv_name` : Name of the server.
    + `chan_name` : Name of the channel
    + `txt` : Boolean - if set to `True`, send a txt file instead of sending messages (takes some time)
    + `l` : Number of messages to gather (Default : 1000)
  + Sends the last l messages from a given channel of a given server. Supports embeds and media (if `txt` is set to false.)
