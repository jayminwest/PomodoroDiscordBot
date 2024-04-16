import discord
from datetime import datetime
import asyncio
from config import supabase
from utils import add_time_tracking_row, convert_seconds
from commands import bot, tasks
from typing import List
from database.utils import update_time_tracking_row, get_data
from time_tracking.utils import convert_seconds

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
        if not tasks:
            raise ValueError("No active timer found! Please start a timer first")

        # Cancel the current task
        for task in tasks:
            task.cancel()
        # tasks.clear()

        # Get the current time
        time_out = datetime.now()

        # Update the chat with a message indicating that the timer is paused
        await ctx.send(f"Time tracking paused at {time_out}. To resume, use !resume.")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")