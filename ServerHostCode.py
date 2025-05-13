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
@client.event
async def on_ready():#Runs when the bot is ready on Discord
        writemessage = f'{client.user} has connected to discord!'
        print(writemessage)#Tells you when the bot is up and running!
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

@client.event
async def on_message(message):
    if message.content == '!start' or message.content == '!Start':
        await message.channel.send(f'Server is starting, it may take a minute or two...')
        the_ip = serverstart()
        current_ip = the_ip
        await message.channel.send(f'IP:    {the_ip}')
client.run(TOKEN)