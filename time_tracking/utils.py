import asyncio
from datetime import datetime, timedelta
from config import supabase

def convert_seconds(total_seconds):
    """
    Convert seconds to a string in the format HH:MM:SS.

    Args:
        total_seconds (int): The total number of seconds to be converted.

    Returns:
        str: A string representing the time in the format HH:MM:SS.
    """
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

async def update_timer(message, time_in):
    """
    Update the timer in the chat.

    Args:
        message (Message): The message object to be edited with the updated timer.
        time_in (datetime): The start time of the timer.

    Returns:
        None
    """
    while True:
        current_time = datetime.now()
        elapsed_time = current_time - time_in
        elapsed_time_str = convert_seconds(elapsed_time.total_seconds())
        await message.edit(content=f"Elapsed time: {elapsed_time_str}")
        await asyncio.sleep(1)

async def update_countdown(message, interval, time_in):
    """
    Create a task to update the countdown timer.

    Args:
        message (Message): The message object to be edited with the updated countdown.
        interval (int): The total time for the countdown in seconds.
        time_in (str): The start time of the countdown in the format "%Y-%m-%d %H:%M:%S".

    Returns:
        None
    """
    while True:
        # Get the current time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate the remaining time
        remaining_time = interval - (datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(time_in, "%Y-%m-%d %H:%M:%S")).total_seconds()

        # Convert the remaining time to a string
        remaining_time_str = convert_seconds(remaining_time)

        # Update the timer in the chat
        await message.edit(content=f"Remaining time: {remaining_time_str}")

        # Wait for 1 second before updating the timer again
        await asyncio.sleep(1)


async def pomodoro_session(ctx, pomodoro_interval, break_interval):
    """
    Run a pomodoro session.

    Args:
        ctx (Context): The context of the command invocation.
        pomodoro_interval (int): The length of each pomodoro session in seconds.
        break_interval (int): The length of each break in seconds.

    Returns:
        None
    """
    # Run a pomodoro session
    while True:
        await asyncio.sleep(pomodoro_interval)
        await ctx.send("Time to take a break!")
        await asyncio.sleep(break_interval)
        await ctx.send("Time to start working!")

def format_datetime(dt):
    """
    Format a datetime object into a string.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        str: A string representing the datetime in the format "%B %d, %Y at %I:%M %p".
    """
    return dt.strftime("%B %d, %Y at %I:%M %p")