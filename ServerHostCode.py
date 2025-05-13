import subprocess
import os
from os.path import join
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from discord import Member
import shutil
import requests
import time
from threading import Thread
import sys
from mcstatus import JavaServer
from datetime import datetime
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
Intents=discord.Intents.default()#Sets all bot perms to the Default, but is reccomended to tweak after
Intents.members = True#Gives the bot the ability to see when a user joins or leaves a server.
Intents.presences = True
Intents.message_content = True
Intents.bans = True
Intents.guild_typing = True
client = discord.Client(intents=Intents)#gives the client the Intents selected

def foldercopy(srcdir, destdir):
    currtime = datetime.now()
    currtime = currtime.strftime("@%Y-%m-%d@%H-%M")
    destdir = f"{destdir}{currtime}"
    shutil.copytree(srcdir, destdir)
    return(destdir)

def startbat():
    global p1
    filepath = r"fullstart.bat"
    p1=subprocess.Popen(filepath, shell=True,stdin = subprocess.PIPE)
    stdout, stderr = p1.communicate()
def serverstart():
    batthread = Thread(target=startbat)
    batthread.start()
    ip = 'I AINT LEAKING TS!'
    return(ip)
def stopbat():
    global p2
    filepath = r"serverstop.bat"
    p2=subprocess.Popen(filepath, shell=True,stdin = subprocess.PIPE)
    stdout, stderr = p2.communicate()
def serverstop():
    batthread = Thread(target=stopbat)
    batthread.start()
def stopServerSequence():
    stopThread = Thread(target=stopSequence)
    stopThread.start()
def stopSequence():
    serverstop()
    time.sleep(5)
    x = True
    while x == True:
        time.sleep(3)
        try:
            current_server = JavaServer.lookup('127.0.0.1:25565')
            current_online = current_server.status().players.online
            current_version = current_server.status().version.name
        except:
            x = False
            writemessage = f'server stopped'
            logEvent(writemessage)
            srcdir = r'\fabric server'
            destdir = r'\Discord Bots\Server Backups\backup'
            foldercopy(srcdir, destdir)
        else:
            writemessage = f'Server stop failed'
            logEvent(writemessage)
            serverstop()

def logEvent(message):
    now = datetime.now()
    the_time = now.strftime("%H:%M:%S")
    with open(r"C:\Users\Prasad\Desktop\Discord Bots\FHS Monkeys\logfile.txt",'a') as logfile: logfile.write(f'{message} at {the_time} \n')

async def status_task():
    message = "Minecraft 1.21.4"
    changeStatus = True
    while True:
        await asyncio.sleep(8)
        try:
            current_server = JavaServer.lookup('127.0.0.1:25565')
            current_online_names = []
        except:
            if changeStatus == True:
                await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="IDLE FAN NOISE"))
        else:

            try:
                for i in current_server.status().players.sample:
                    current_online_names.append(i.name)
            except:
                if message != "Minecraft 1.21.4":
                    message = "Minecraft 1.21.4"
                    await client.change_presence(activity=discord.Game(name=message))
            else:
                newMessage = "Minecraft 1.21.4 \n Online:"
                for i in current_online_names:
                    key = None
                    for user, player in usernames.items():
                        if player == i:
                            key = user
                    if key != None:
                        newMessage = newMessage + "\n" + key
                    else:
                        newMessage = newMessage + "\n" + i
                if message != newMessage:
                    message = newMessage
                    await client.change_presence(activity=discord.Game(name=message))

@client.event
async def on_ready():#Runs when the bot is ready on Discord
        writemessage = f'{client.user} has connected to discord!'
        print(writemessage)#Tells you when the bot is up and running!
        logEvent(writemessage)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = "IDLE FAN NOISE"))
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        client.loop.create_task(status_task())

@client.event
async def on_member_join(member):
    await member.create_dm()#Creates a DM with user
    writemessage = f'Hello {member.name}, welcome to {member.guild.name}! Make sure to check #rules and have fun!'
    await member.dm_channel.send(writemessage)#Sends "hi *user name*, welcome to my Discord Server!" to the User in the DM
    logEvent(writemessage)
@client.event
async def on_message(message):
    global current_ip
    if message.content == '!help' or message.content == '!Help' or message.content == '!commands' or message.content == '!Commands':
        await message.channel.send(f'!Gamer - gives the role "Gamer" to you')
        await message.channel.send(f'!status - Gives information about the server')
        await message.channel.send(f'!start - starts the MC server, and gives IP')
        await message.channel.send(f'!stop - stops MC server, only available to moderators')
        await message.channel.send(f'!softstop - stops MC server, only if nobody is online')
        await message.channel.send(f'!online - Lists the names of players that are online.')
        await message.channel.send(f'!logs - Sends log in DM, only available to moderators.')
        await message.channel.send(f'!logsdelete - Deletes log file, only available to moderators.')
        await message.channel.send(f'!serverlogs - Sends server log in DM, only available to moderators.')
        writemessage = f'!Help used successfully by {message.author.name}'
        logEvent(writemessage)
    if message.content == '!Gamer' or message.content == '!gamer':
        role = message.author.guild.get_role(roles['gamer'])
        await message.author.add_roles(role)
        await message.channel.send(f'{message.author.name} was given the role of {role.name}')
        writemessage = f'!Gamer used successfully by {message.author.name}'
        logEvent(writemessage)
    if message.content =='!status' or message.content == '!Status':
        try:
            current_server = JavaServer.lookup('127.0.0.1:25565')
            current_online = current_server.status().players.online
            current_version = current_server.status().version.name
        except:
            await message.channel.send(f'The server seems to be offline. Use !start to start the server!')
            writemessage = f'!status used successfully by {message.author.name}'
            logEvent(writemessage)
        else:    
            await message.channel.send(f'There are {current_online} player(s) online. The server is on version {current_version}.')
            writemessage = f'!status used successfully by {message.author.name}'
            logEvent(writemessage)
    if message.content == '!online':
        try:
            current_server = JavaServer.lookup('127.0.0.1:25565')
            current_online_names = []
        except:
            await message.channel.send(f'The server seems to be offline. Use !start to start the server!')
            writemessage = f'!online used successfully by {message.author.name}'
            logEvent(writemessage)      
        else:
            try:
                for i in current_server.status().players.sample:
                    current_online_names.append(i.name)
            except:
                await message.channel.send(f'The server is currently empty')
                writemessage = f'!online used successfully by {message.author.name}'
                logEvent(writemessage)
            else:
                newMessage = "Online players:"
                for i in current_online_names:
                    key = None
                    for user, player in usernames.items():
                        if player == i:
                            key = user
                    if key != None:
                        newMessage = newMessage + "\n" + key
                    else:
                        newMessage = newMessage + "\n" + i
                await message.channel.send(f'{newMessage}')
                writemessage = f'!online used successfully by {message.author.name}'
                logEvent(writemessage)
    if message.content == '!start' or message.content == '!Start':
        await message.channel.send(f'Server is starting, it may take a minute or two...')
        the_ip = serverstart()
        current_ip = the_ip
        await message.channel.send(f'IP:    {the_ip}')
        await client.change_presence(activity=discord.Game(name="Minecraft 1.21.4"))
        writemessage = f'!start used successfully by {message.author.name}'
        logEvent(writemessage)
    if message.content == '!stop' or message.content == '!Stop':
        writemessage = f'!stop attempted by {message.author.name}'
        logEvent(writemessage)
        role = discord.utils.get(message.author.guild.roles, name="Moderator")
        if role in message.author.roles:
            stopServerSequence()
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="IDLE FAN NOISE"))
            await message.channel.send(f'Server is shutting down. All online players will be kicked.')
            await message.author.create_dm()#Creates a DM with user
            await message.author.dm_channel.send(file=discord.File(r'C:\Users\Prasad\Desktop\fabric server\logs\latest.log'))
            writemessage = f'!stop used successfully by {message.author.name}'
            logEvent(writemessage)
        if message.content == '!softstop':
        writemessage = f'!softstop attempted by {message.author.name}'
        logEvent(writemessage)
        try:
            current_server = JavaServer.lookup('127.0.0.1:25565')
            current_status = current_server.status
            current_online = current_server.status().players.online
            current_version = current_server.status().version.name
        except:
            await message.channel.send(f'The server seems to be offline. Use !start to start the server!')
            writemessage = f'!softstop(offline) used by {message.author.name}'
            logEvent(writemessage)
        else:
            if current_online == 0:
                await message.channel.send('Nobody is Online. The server is stopping now.')
                stopServerSequence()
                writemessage = f'!softstop used successfully by {message.author.name}'
                logEvent(writemessage)
            else:          
                await message.channel.send(f'There are {current_online} player(s) online.')
                writemessage = f'!softstop(denied) used by {message.author.name}'
                logEvent(writemessage)
    if "!user" in message.content:
        if message.author == client.user:
            return
        parts = message.content.split(" ")
        if len(parts) != 2:
            await message.channel.send(f'Sorry, that is an invalid use. Please use "!user <username>" to set your Minecraft username.')
            message = ""
        else:
            if parts[1] in usernames.values():
                await message.channel.send(f'Sorry, {parts[1]} is already used by another user. Check for spelling mistakes and try again.')
            else:
                parts[1]
                usernames[message.author.name] = parts[1]
                with open(r"C:\Users\Prasad\Desktop\Discord Bots\FHS Monkeys\UserSave.txt",'a') as userFile: userFile.write(f'{message.author.name};{parts[1]} \n')
                await message.channel.send(f'Successfuly saved {parts[1]} as your username.')
    if message.content == '!logs':
        now = datetime.now()
        the_time = now.strftime("%H:%M:%S")
        role = discord.utils.get(message.author.guild.roles, name="Moderator")
        writemessage = f'Logs requested by {message.author.name}'
        logEvent(writemessage)
        if role in message.author.roles:
            await message.channel.send(f'Logs will be sent directly')
            await message.author.create_dm()#Creates a DM with user
            await message.author.dm_channel.send(file=discord.File(r"C:\Users\Prasad\Desktop\Discord Bots\FHS Monkeys\logfile.txt"))
            writemessage = f'Logs sent to {message.author.name} at {the_time}'
            logEvent(writemessage)
    if message.content == '!logsdelete':
        writemessage = f'Log deletion requested by {message.author.name}'
        role = discord.utils.get(message.author.guild.roles, name="Moderator")
        if role in message.author.roles:
            await message.author.create_dm()#Creates a DM with user
            await message.author.dm_channel.send(file=discord.File(r"C:\Users\Prasad\Desktop\Discord Bots\FHS Monkeys\logfile.txt"))
            open(r"C:\Users\Prasad\Desktop\Discord Bots\FHS Monkeys\logfile.txt",'w').close()
            await message.channel.send(f'Logs have been deleted.')
            writemessage = f'Log files deleted by {message.author.name}'
            logEvent(writemessage)
    if message.content == '!serverlogs':
        role = discord.utils.get(message.author.guild.roles, name="Moderator")
        writemessage = f'Server logs requested by {message.author.name}'
        logEvent(writemessage)
        if role in message.author.roles:
            await message.channel.send(f'Server logs will be sent directly as .txt')
            await message.author.create_dm()#Creates a DM with user
            await message.author.dm_channel.send(file=discord.File(r'C:\Users\Prasad\Desktop\fabric server\logs\latest.log'))
            writemessage = f'Server logs sent to {message.author.name}'
            logEvent(writemessage)
client.run(TOKEN)