import discord
from discord.ext import commands
from config import TOKEN

tasks = []
timers = {}

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())