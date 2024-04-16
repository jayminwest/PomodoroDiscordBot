import discord
from datetime import datetime
import asyncio
from config import supabase
from database.utils import add_time_tracking_row
from time_tracking.utils import convert_seconds
from commands import bot, tasks, timers
from typing import List
from database.utils import update_time_tracking_row, get_data, update_paused_at
from time_tracking.utils import convert_seconds, format_datetime

# Command to pause tracking time
@bot.command(name='pause')
async def pause(ctx):
    """
    Pause tracking time.

    This function pauses the time tracking process and updates the chat with a message indicating that the timer is paused.
    
    Parameters:
        ctx (Context): The context of the command invocation.

    Returns:
        None

    Raises:
        ValueError: If no active timer is found.
        Exception: If there's an error while pausing the timer or updating the chat.
    """
    try:
        # Check if a task is currently running
        # if not tasks or ctx.author.id not in timers:
        #     raise ValueError("No active timer found! Please start a timer first")

        timer = timers[ctx.author.id]
        await timer.pause()

        # update_paused_at(timer.user_id, timer.start_time, datetime.now())

        # Cancel the current task
        for task in tasks:
            task.cancel()
        tasks.clear()

        await ctx.send(f"Time tracking paused at {format_datetime(datetime.now())}. To resume, use !resume.")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")