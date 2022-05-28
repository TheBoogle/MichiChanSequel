import json
import os
import platform
import random
import sys

import mysql.connector

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

# load JSON files
LJS = {}

for OFile in os.listdir('JSONFiles'):
	with open("JSONFiles/" + OFile) as file:
		config = json.load(file)
		LJS[OFile.split('.')[0]] = config
	

BotIntents = disnake.Intents.all()

bot = Bot(command_prefix=commands.when_mentioned, intents=BotIntents, help_command=None)

bot.Database = mysql.connector.connect(
	host=LJS['database']['host'],
	user=LJS['database']['user'],
	passwd=LJS['database']['passwd'],
	database=LJS['database']['database'],
)

bot.LJS = LJS
bot.config = LJS['config']

@bot.event
async def on_ready():
	print(f'{bot.user.name} is now online.')

	status_task.start()


	

@tasks.loop(minutes=1.0)
async def status_task():
	await bot.change_presence(activity=disnake.activity.Game(random.choice(LJS['status'])))


def load_commands():
    for file in os.listdir("./Cogs/"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"Cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

if __name__ == "__main__":
	load_commands()

bot.run(LJS['config']['token'])