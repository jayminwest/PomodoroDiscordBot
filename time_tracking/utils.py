import asyncio
from datetime import datetime, timedelta
from config import supabase

def convert_seconds(seconds):
    # Convert seconds to a string in the format HH:MM:SS
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

async def update_timer(message, time_in):
    # Update the timer in the chat
    while True:
        current_time = datetime.now()
        elapsed_time = current_time - time_in
        elapsed_time_str = convert_seconds(elapsed_time.total_seconds())
        await message.edit(content=f"Elapsed time: {elapsed_time_str}")
        await asyncio.sleep(1)

# Create a task to update the timer
async def update_countdown(message, interval, time_in):
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
    # Run a pomodoro session
    while True:
        await asyncio.sleep(pomodoro_interval)
        await ctx.send("Time to take a break!")
        await asyncio.sleep(break_interval)
        await ctx.send("Time to start working!")