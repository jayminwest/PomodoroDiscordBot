import discord
from datetime import datetime
import asyncio
from config import supabase
from utils import add_time_tracking_row, convert_seconds
from commands import bot, tasks
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
    start_time = datetime.now()
    try:
        add_time_tracking_row(ctx, start_time)
    except Exception as e:
        await ctx.send(f"Failed to add time tracking row: {str(e)}")
        return

    message = await ctx.send(f"Time tracking started at {start_time}")

    # Create new timer:
    timer = Timer()

    # Start the timer:
    await timer.start()

    async def update_timer(message: discord.Message) -> None:
        while True:
            # Get the elapsed time from the timer
            elapsed_time_str = timer.get_elapsed_time()

            # Update the message with the elapsed time
            await message.edit(content=f"Elapsed time: {elapsed_time_str}")

            # Wait for 1 second before updating the timer again
            await asyncio.sleep(1)

    task = bot.loop.create_task(update_timer(message))
    tasks.append(task)

    # async def update_timer(message: discord.Message, start_time: datetime) -> None:
    #     while True:
    #         current_time = datetime.now()
    #         elapsed_time = current_time - start_time
    #         elapsed_time_str = convert_seconds(elapsed_time.total_seconds())
    #         await message.edit(content=f"Elapsed time: {elapsed_time_str}")
    #         await asyncio.sleep(1)

    # task = bot.loop.create_task(update_timer(message, start_time))
    # tasks.append(task)
