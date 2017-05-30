import discord
import asyncio
from datetime import datetime
import time, asyncio
import types
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

basin_respawn = 2580
time_left = 0
svrs = dict()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for s in client.servers:
        print(s.name)
        svrs[s.name] = types.SimpleNamespace()
        svrs[s.name].next_boss = [0]*6

async def errmsg(message):
    await client.send_message(message.channel, 'Incorrect usage, use !basin help')

async def usage(message):
    s = "```Markdown\nUsage\n\nNew Usage options!\nCheck time for next Boss: !basin [Server group number]\nSet time for Basin Boss: !basin set [Server group number] [Minutes since last boss spawn]```\n"
    await client.send_message(message.channel, s)
   
async def basin(message, ar):

    if ar[1] == 'help':
        await usage(message)
        return

    s_name = str(message.server.name)
    if len(ar) == 2:
        s_num = int(ar[1]) - 1
    else:
        s_num = int(ar[2]) - 1

    if ar[1] == 'set' and len(ar) == 4:

        logger.warning("Time set for group " + str(s_num+1) + " by " + message.author.name + " for " + s_name)

        bos_time = int(ar[3]) * 60
        time_left = basin_respawn - bos_time 
        svrs[s_name].next_boss[s_num] = time.mktime(time.localtime()) + time_left
        await client.send_message(message.channel, 'Time left for boss = ' + str(int(time_left/60)) + ' minutes')

    elif len(ar) == 2:
        if svrs[s_name].next_boss[s_num] == 0:
            await client.send_message(message.channel, 'Respawn time isnt set for this server group!')
            return
        time_left = time.mktime(time.localtime()) - svrs[s_name].next_boss[s_num]
        time_left = basin_respawn - time_left%basin_respawn
        at = int(time_left / 60)
        await client.send_message(message.channel, 'Approximate time left for Server Group ' + str(s_num+1) + ' = ' + str(at) + ' minutes')
    else:
        await errmsg(message)

@client.event
async def on_message(message):
    s_name = message.server.name
    if s_name not in svrs:
        svrs[s_name] = types.SimpleNamespace()
        svrs[s_name].next_boss = [0]*6

    if message.author == client.user:
        return
    if message.content.startswith('!dg_bot'):
        await usage(message)
    if message.content.startswith('!basin'):
        ar = message.content.split()
        if len(ar) < 2:
            await client.send_message(message.channel, 'No command entered!') 
        
        if len(ar) == 2 or len(ar) == 4:
            try:
                await basin(message,ar)
            except ValueError:
                await errmsg(message)
        else: 
            await usage(message)


client.run('MzE0ODQzNDI0NzAyNTk1MDcz.C_-EWg.uqP7cMBYbAupzIgqBniJQM32Ugs')
