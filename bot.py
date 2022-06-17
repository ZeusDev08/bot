from importlib.resources import path
import discord
from discord.ext import commands, tasks
import requests
import os
from os import system
import subprocess
import shutil
from flask import Flask
from threading import Thread
from itertools import cycle

app = Flask('')

@app.route('/')
def main():
    return "El bot esta listo"
def run():
    app.run(host="1.0.1.0", port=8090)
def keep_alive():
    server = Thread(target=run)
    server.start()

token = os.environ['DISCORD_TOKEN']

channel_id = 987361729933635667

bot = commands.Bot(command_prefix='!')
bot.remove_commadn('help')

def obfuscation(path, author):
    copy = f".//obfuscated//{author}.lua"
    
    # borra duplicados
    if os.path.exists(copy):
        os.remove(copy)
    
    # copia los archivos subidos para realizar operaciones
    shutil.copyfile(path, copy)
    
    text_file = open(f".//obfuscated//{author}.lua", "r")
    data = text_file.read()
    text_file.close()
    f = open(copy, "a")
    f.truncate(0)
    f.write(data)
    f.close()
    
    originalupload = open(path, "r")
    originalupload_data = originalupload.read()
    originalupload.close()
    
    with open(copy, "r") as in_file:
        buf = in_file.readlines()
    with open(copy, "w") as out_file:
        for line in buf:
            if line == "--SCRIPT\n":
                line = line + originalupload_data + '\n'
            out_file.write(line)
    output = subprocess.getoutput(f'bin/luvit {copy}')
    
    if os.path.exists(f".//obfuscated//{author}.lua"):
        os.remove(f".//obfuscated//{author}--oculto.lua", "a")
    
    f = open(f".//obfuscated//{author}--oculto.lua", "a")
    f.write(output)
    f.close()
    
status = cycle([
    'para .lua archivos para ocultar.', 'para .lua archivos para ocultar..', 'para .lua archivos para ocultar...',
])
    
@bot.event
async def on_ready():
    change_status.start()
    print(f"{bot.user} esta listo!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@bot.event
async def on_message(message):
    channel = str(message.channel)
    author = str(message.author)
    channel = bot.get_channel(channel_id)
    
    try:
        url = message.attachments[0].url
        if not message.author.bot:
            if message.channel.type is discord.ChannelType.private:
                if '.lua' not in url:
                    embed = discord.Embed(
                        title="Error, no es .lua",
                        description = "Solo esta permitido archivos .lua",
                        color = 0xFF3357)
                    message = await channel.send(embed=embed)
                    dm = await message.author.create_dm()
                    await dm.send(embed=embed)
                else:
                    uploads_dir = f".//uploads//"
                    obfuscated_dir = f".//obfuscated//"
                    
                    if not os.path.exists(uploads_dir):
                        os.makedirs(uploads_dir)
                    if not os.path.exists(obfuscated_dir):
                        os.makedirs(obfuscated_dir)
                    
                    print(f'\nNuevo script recivido de {author}')
                    print(f'Enlace adjunto: {message.attachments[0].url}\n')
                    response = requests.get(url)
                    path = f".//uploads//{author}.lua"
                    if os.path.exists(path):
                        os.remove(path)
                    
                    open(path, "wb").write(response.content)
                    obfuscation(path, author)
                    embed = discord.Embed(title="El archivo ha sido ocultado correctamente!")
                    
                    await channel.send(
                        embed=embed,
                        file=discord.File(f".//obfuscated//{author}--oculto.lua")
                    )
    except:
        pass
bot.run(token)