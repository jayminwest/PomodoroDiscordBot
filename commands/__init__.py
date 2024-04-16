import discord
from discord.ext import commands
from config import TOKEN

"""
tasks: Dict[int, List[asyncio.Task]]
    A dictionary of all the currently running tasks in the bot, where the key is the user ID and the value is a list of tasks for that user.
    This includes tasks such as updating the timer messages, handling user input, etc.
    Each task is an instance of asyncio.Task, which represents a coroutine that is currently being executed.
"""
tasks = {}

"""
timers: Dict[int, Timer]
    A dictionary of all the currently active timers, where the key is the user ID and the value is the corresponding Timer object.
    Each timer represents a timer that is currently running for a user, and is responsible for updating the timer message and handling user input.
"""
timers = {}

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())