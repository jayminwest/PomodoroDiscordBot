from datetime import datetime
import asyncio
from database.utils import add_time_tracking_row
from time_tracking.utils import convert_seconds
from commands import bot, tasks
from time_tracking.utils import update_countdown

@bot.command(name='pomodoro')
async def pomodoro(ctx, pomodoro_interval: int = 25, break_interval: int = 5) -> None:
    """
    Start a pomodoro session.

    Parameters:
    ctx (Context): The context of the command invocation.
    pomodoro_interval (int): The length of the pomodoro interval in minutes. Defaults to 25.
    break_interval (int): The length of the break interval in minutes. Defaults to 5.
    """
    try:
        # Convert intervals from minutes to seconds
        pomodoro_interval *= 60
        break_interval *= 60

        time_in = datetime.now()
        add_time_tracking_row(ctx, time_in)
        message = await ctx.send(f"Pomodoro session started at {time_in}")
        message = await ctx.send(f"Remaining time: ")

        # Create a task to run the pomodoro session
        pomodoro_task = asyncio.create_task(pomodoro_session(ctx, pomodoro_interval, break_interval))
        tasks.append(pomodoro_task)

        # Create a task to update the timer
        async def update_timer():
            while True:
                current_time = datetime.now()
                remaining_time = pomodoro_interval - (current_time - time_in).total_seconds()
                remaining_time_str = convert_seconds(remaining_time)
                await message.edit(content=f"Remaining time: {remaining_time_str}")
                await asyncio.sleep(1)

        update_timer_task = bot.loop.create_task(update_timer())
        tasks.append(update_timer_task)

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

async def pomodoro_session(ctx, pomodoro_interval: int, break_interval: int) -> None:
    """
    Run a pomodoro session.

    Parameters:
    ctx (Context): The context of the command invocation.
    pomodoro_interval (int): The length of the pomodoro interval in seconds.
    break_interval (int): The length of the break interval in seconds.
    """
    while True:
        await asyncio.sleep(pomodoro_interval)
        await ctx.send("Time to take a break!")
        await asyncio.sleep(break_interval)
        await ctx.send("Time to start working!")