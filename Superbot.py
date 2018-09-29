from features.ytsearch import getSearch
from features.music import create_media 
from discord.ext import commands
from itertools import cycle
import youtube_dl
import datetime
import discord
import asyncio
import random
import time

#-----------------------------------------------------------------------------------------------------------------

TOKEN = "NDYxNjU2Nzk0NTYxNzczNTg4.DhWe_Q.ngqoRy0rniOJr79BNXfdAVdTC5c" # add your bot TOKEN

client = commands.Bot(command_prefix="$") #choose the prefix you want yo use
servers_list = {}
searches = {}

HEADS = "**Heads**"
TAILS = "**Tails**"

RESUME = ":play_pause: **RESUMING**"
REMOVE = "**SONGS REMOVED**"
PAUSE = " :pause_button: **PAUSED**"
STOP = ":stop_button: **STOPING MUSIC**"
SKIP = ":track_next: **SONG SKIPED**"
NO_PLAYING = "**NO SONGS PLAYING** :x:"
LS_SKIPED = ":track_next: **LAST SONG SKIPED**"
RANDOM = ":twisted_rightwards_arrows: **STIR QUEUE**"

NOT_ALLOWED = "**You are not allowed to use that command** :exclamation:"
BOT_NOT_IN_VOICE_CHANNEL = "**Im not in voice channel** :exclamation:"
BOT_IN_VOICE_CHANNEL = "**Im allready in a voice channel** :exclamation:"
USER_NOT_IN_VOICE_CHANNEL = "**You are not in a voice channel** :exclamation:"
MSG_ALERT = "__You can olny delete up to 14 days old messages__"
FAILED_SEARCH = "**Could not find the song. Try with Search command**"

'''client.remove_command('help')''' 

#-----------------------------------------------------------------------------------------------------------------

def in_channel(server, channel):

    """Check if commands are from the bot voice channel"""

    if channel in servers_list[server]:

        return True

    else:
        return False

#-----------------------------------------------------------------------------------------------------------------

async def search_time_out():

    '''Change bot status in a loop'''

    global urlTitle

    await client.wait_until_ready()

    while not client.is_closed:

        unix = time.time()
        DATE = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))

        #obtener solo la hora

        await asyncio.sleep(5)

#-----------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():

    '''Log when bot is online'''

    print("Bot is ready and working\n")

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def ping(ctx):

    '''Pong!'''

    author = ctx.message.author.id
    channel = ctx.message.channel

    await client.send_message(channel, "<@{}> Pong!".format(author))

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def say(ctx, *args): 

    '''Command to echo what user said'''

    channel = ctx.message.channel

    args = " ".join(args)
    await client.send_message(channel, "{}".format(args))

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def clear(ctx, amount=99):

    '''Delete messages up to 99'''

    channel = ctx.message.channel
    messages = []
    amount += 1
    
    if amount > 99:
        amount = 99

    try:
        async for message in client.logs_from(channel, limit=int(amount)):
            messages.append(message)
        
        await client.delete_messages(messages)

    except:
        #await client.say("You can only delete messages that are under 14 days old.")
        await client.send_message(channel, MSG_ALERT)

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def flip(ctx):

    '''50% chance of Head or Tail'''

    channel = ctx.message.author.voice.voice_channel

    flip = (HEADS, TAILS)
    #await client.say(random.choice(flip))
    await client.send_message(channel, random.choice(flip))

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def join(ctx):

    '''Join bot to a voice channel'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server not in servers_list:

        await client.join_voice_channel(channel)

        aux_sv = create_media(server, channel)  

        servers_list [server] = [channel, aux_sv]

    else:

        await client.send_message(text_channel, BOT_IN_VOICE_CHANNEL)
    
#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def leave(ctx):

    '''Leave bot from voice channel'''
    
    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server in servers_list and in_channel(server, channel):

        voice_client = client.voice_client_in(server)

        servers_list[server][1].stop()
        servers_list.pop(server) #, None

        await voice_client.disconnect()

    else:
        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)
    
#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def play(ctx, *args):

    '''Play/add music to Playlist'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    error = False

    urls = []
    url = " ".join(args)

    if server not in servers_list:

        try:
            await client.join_voice_channel(channel)
        
        except:
            await client.send_message(text_channel, USER_NOT_IN_VOICE_CHANNEL)
            error = True

    elif not in_channel(server, channel):

        error = True
        await client.send_message(text_channel, NOT_ALLOWED)        
        

    if not error and url != "":
        
        voice_client = client.voice_client_in(server)

        urls.append(list(getSearch(url))) #call ytsearch to get video link and title

        for i in urls:

            if urls[0][0] != "ERROR" and urls[0][1] != "ERROR":

                url = urls[0][0]
                title = urls[0][1]
                
                print("url: ", url)
                print("Title: ", title)
                
                urls.pop(0)

                if server not in servers_list:

                    aux_sv = create_media(server, channel)  

                    servers_list [server] = [channel, aux_sv]

                    player = await voice_client.create_ytdl_player(url, after=lambda: servers_list[server][1].playlist_queue())

                    servers_list[server][1].play(player, title)

                else:

                    if in_channel(server, channel):

                        player = await voice_client.create_ytdl_player(url, after=lambda: servers_list[server][1].playlist_queue())

                        servers_list[server][1].play(player, title)

                    else:

                        await client.send_message(text_channel, NOT_ALLOWED)

            else:
                await client.send_message(text_channel, FAILED_SEARCH + ": {}".format(url))

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def search(ctx, *args):

    '''Search a song options to choose'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    author = ctx.message.author
    text_channel = ctx.message.channel

    search = []
    search = " ".join(args)

    if in_channel(server, channel):

        embed_search = getSearch(search, embed_search=True)

        embed = discord.Embed(

        title = "Search list",
        #description = "Search list",
        color = discord.Color.red()

        )

        for i in range(len(embed_search)):

            embed.add_field(name=str(i + 1) + ": ", value= embed_search[i][1], inline=False)

        await client.send_message(text_channel, embed = embed)

        unix = time.time()
        DATE = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        
        searches[server] = [channel, author, text_channel, embed_search, DATE]
     
    else:

        await client.send_message(text_channel, NOT_ALLOWED)

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def choose(ctx, *args):

    '''Let user choose a song from Search commad'''

    global servers_list

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    author = ctx.message.author
    text_channel = ctx.message.channel
    voice_client = client.voice_client_in(server)

    songs = []
    print(args)
    songs = " ".join(args)

    if server in searches:

        if channel in searches[server]:

            if author in searches[server]:

                if text_channel in searches[server]:

                    for i in songs:

                        try:
                            
                            i = int(i)
                            i -= 1

                        except:
                            continue

                        url = searches[server][3][i][0]
                        title = searches[server][3][i][1]

                        if server not in servers_list:

                            aux_sv = create_media(server, channel) 
                            servers_list [server] = [channel, aux_sv]

                            player = await voice_client.create_ytdl_player(url, after=lambda: servers_list[server][1].playlist_queue())

                            servers_list[server][1].play(player, title)

                        else:

                            player = await voice_client.create_ytdl_player(url, after=lambda: servers_list[server][1].playlist_queue())

                            servers_list[server][1].play(player, title)

                else:

                    await client.send_message(text_channel, "You must be in the same channel that search request")

        else:

            await client.send_message(text_channel, "You must be in the same channel that Superbot")

    else:

        await client.send_message(text_channel, "Use $search to get a list of song to choose")


#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def pause(ctx):

    '''Pause current song'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server in servers_list:
        
        if in_channel(server, channel):

            if not servers_list[server][1].isEmpty():

                if servers_list[server][1].isPlaying():

                    servers_list[server][1].pause()

                    await client.send_message(text_channel, PAUSE)

                else:
                    await client.send_message(text_channel, "Music allready paused")

            else:
                await client.send_message(text_channel, NO_PLAYING)

        else:

            await client.send_message(text_channel, NOT_ALLOWED)

    else:

        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def resume(ctx):

    '''Resume current song'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server in servers_list:

        if in_channel(server, channel):

            if not servers_list[server][1].isEmpty:

                if servers_list[server][1].isPlaying():

                    await client.send_message(text_channel, "Music allready playing")

                else:

                    servers_list[server][1].resume()

                    await client.send_message(text_channel, RESUME)

            else:
                await client.send_message(text_channel, NO_PLAYING)

        else:

            await client.send_message(text_channel, NOT_ALLOWED)
    
    else:

        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)            
    

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def stop(ctx):

    '''Stop Playlist'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server in servers_list:

        if in_channel(server, channel):

            if not servers_list[server][1].isEmpty():

                servers_list[server][1].stop()
                await client.send_message(text_channel, STOP)

            else:
                await client.send_message(text_channel, NO_PLAYING)

        else:

            await client.send_message(text_channel, NOT_ALLOWED)

    else:

        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)    


#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def remove(ctx, *args):

    '''Remove specific song from queue'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    lista = list(args)
    
    if server in servers_list:

        if in_channel(server, channel):

            if not servers_list[server][1].isEmpty:

                servers_list[server][1].remove(lista)
                await client.send_message(text_channel, REMOVE)

            else:
                await client.send_message(text_channel, NO_PLAYING)

        else:

            await client.send_message(text_channel, NOT_ALLOWED)

    else:

        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)
    

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def skip(ctx):
    
    '''Skip the current song'''

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel 

    if server in servers_list: # check if server has a bot playing

        if in_channel(server, channel):

            if not servers_list[server][1].isEmpty():

                servers_list[server][1].skip()
                await client.send_message(text_channel, SKIP)                

            else:
                await client.send_message(text_channel, NO_PLAYING)

        else:

            await client.send_message(text_channel, NOT_ALLOWED)

    else:

        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)
            
#-----------------------------------------------------------------------------------------------------------------
@client.command(pass_context=True)
async def sort(ctx):

    """Sort queue"""

    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server in servers_list: # check if server has a bot playing

        if in_channel(server, channel): # check if user are in bot's channel 

            if not servers_list[server][1].isEmpty(): # check if the playlist is Empty

                servers_list[server][1].sort() # sort queue

                await client.send_message(text_channel, RANDOM)

            else:
                await client.send_message(text_channel, NO_PLAYING) #if playlist is empty, dysplay alert message

        else:
            await client.send_message(text_channel, NOT_ALLOWED) # if user are not in bot's channel, dysplay alert message

    else:
        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL) # if bot is not in a voice channel, dysplay alert

#-----------------------------------------------------------------------------------------------------------------

@client.command(pass_context=True)
async def queue(ctx):

    '''Show queue'''


    server = ctx.message.server
    channel = ctx.message.author.voice.voice_channel
    text_channel = ctx.message.channel

    if server in servers_list:

        if in_channel(server, channel):

            if not servers_list[server][1].isEmpty():

                playlist = servers_list[server][1].queue()

                embed = discord.Embed(

                    #title = "",
                    description = "\n",
                    color = discord.Color.red()

                    )

                #embed.set_author(name= "Queue List")
                #embed.set_footer(text= "This is a fotter")

                embed.add_field(name= "Current playing: ", value= playlist[0][1], inline=False)

                if len(playlist) > 1:

                    count = 1

                    for i in range(len(playlist)):

                        embed.add_field(name= str(count) + ": ", value= playlist[count][1], inline=False)
                        count += 1

                await client.send_message(text_channel, embed = embed)

            else:
                await client.send_message(text_channel, NO_PLAYING)

        else:
            await client.send_message(text_channel, NOT_ALLOWED)

    else:
        await client.send_message(text_channel, BOT_NOT_IN_VOICE_CHANNEL)




client.loop.create_task(search_time_out())
client.run(TOKEN)