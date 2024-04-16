import discord
from datetime import datetime
import asyncio
from config import supabase
from database.utils import add_time_tracking_row
from time_tracking.utils import convert_seconds
from commands import bot, tasks, timers
from typing import List
from time_tracking.timer import Timer

@bot.command(name='start')
async def start_time_tracking(ctx: discord.ext.commands.Context) -> None:
    """
    Start tracking time.

    This command starts tracking time for the user who invoked it.
    It adds a new row to the database with the current start-time,
    and then creates a task that updates a timer in the chat every second
    with the elapsed time since starting.

    Parameters:
    ctx (discord.ext.commands.Context): The context of the command invocation.

    Returns:
    None
    """
    try:
        start_time = datetime.now()
    
        message = await ctx.send(f"Time tracking started at {start_time}")

        # Create new timer:
        timer = Timer(user_id=ctx.author.id, start_time=start_time, message=message)
        timers[timer.user_id] = timer

        await timers[timer.user_id].start()

    except Exception as e:
        await ctx.send(f"Failed to add time tracking row: {str(e)}")
        return

    if ctx.author.id not in tasks:
        tasks[ctx.author.id] = []
    task = bot.loop.create_task(timer.start())
    tasks[ctx.author.id].append(task)