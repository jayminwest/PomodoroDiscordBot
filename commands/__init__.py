import discord
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

tasks = []