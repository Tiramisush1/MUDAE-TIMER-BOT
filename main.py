import os
import discord
from datetime import datetime, time, timedelta
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

suspended_channels = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('%hello'):
        await message.channel.send('Hola, ¿cómo están?')

    if message.content.startswith('%suspender'):
        command_args = message.content.split()

        if len(command_args) != 3:
            await message.channel.send('El formato del comando es: %suspender <hora_inicio> <hora_fin>')
            return

        try:
            hora_inicio = datetime.strptime(command_args[1], '%H:%M').time()
            hora_fin = datetime.strptime(command_args[2], '%H:%M').time()

            suspended_channels[message.channel.id] = (hora_inicio, hora_fin)
            role = discord.utils.get(message.guild.roles, name='Spider (Full Time)')
            await message.channel.set_permissions(role, send_messages=False, add_reactions=False)
            await message.channel.send(f'El canal ha sido suspendido desde {hora_inicio} hasta {hora_fin}.')
        except ValueError:
            await message.channel.send('El formato de hora debe ser HH:MM.')

    elif message.content.startswith('%reactivar'):
        if message.channel.id in suspended_channels:
            del suspended_channels[message.channel.id]
            role = discord.utils.get(message.guild.roles, name='Spider (Full Time)')
            await message.channel.set_permissions(role, send_messages=True, add_reactions=True)
            await message.channel.send('El canal ha sido reactivado.')
        else:
            await message.channel.send('El canal no está suspendido.')

    if message.channel.id in suspended_channels:
        current_time = datetime.now().time()
        start_time, end_time = suspended_channels[message.channel.id]
        if start_time <= current_time <= end_time:
            await message.delete()
            await message.channel.send('Este canal está suspendido temporalmente.')

client.run(TOKEN)
