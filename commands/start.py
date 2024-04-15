import discord
from datetime import datetime
import asyncio
from config import supabase
from utils import add_time_tracking_row, convert_seconds
from commands import bot, tasks


@bot.command(name='start')
async def start(ctx):
    """
    Start tracking time.

    This command starts tracking time for the user who invoked it.
    It adds a new row to the database with the current start-time,
    and then creates a task that updates a timer in the chat every second
    with the elapsed time since starting.

    Parameters:
    ctx (Context): The context of the command invocation.

    Returns:
    None
    """
    time_in = datetime.now()
    add_time_tracking_row(ctx, time_in)
    message = await ctx.send(f"Time tracking started at {time_in}")

    # Create a task to update the timer
    async def update_timer(message):
        while True:
            # Get the current time
            current_time = datetime.now()

            # Calculate the elapsed time
            elapsed_time = current_time - time_in

            # Convert the elapsed time to a string
            elapsed_time_str = convert_seconds(elapsed_time.total_seconds())

            # Update the timer in the chat
            await message.edit(content=f"Elapsed time: {elapsed_time_str}")

            # Wait for 1 second before updating the timer again
            await asyncio.sleep(1)

    task = bot.loop.create_task(update_timer(message))
    tasks.append(task)