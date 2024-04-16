# import discord
# from datetime import datetime
# import asyncio
# from config import supabase
# from database.utils import add_time_tracking_row
# from time_tracking.utils import convert_seconds
# from commands import bot, tasks
# from typing import List
# from database.utils import update_time_tracking_row, get_data
# from time_tracking.utils import convert_seconds

# # Command to resume tracking time
# @bot.command(name='resume')
# async def resume(ctx):
#     """
#     Resume tracking time.

#     This function resumes the time tracking process and updates the chat with a message indicating that the timer has resumed.
    
#     Parameters:
#         ctx (Context): The context of the command invocation.

#     Returns:
#         None

#     Raises:
#         ValueError: If no active timer is found.
#         Exception: If there's an error while resuming the timer or updating the chat.
#     """
#     try:
#         # Check if a task is currently running
#         if not tasks:
#             raise ValueError("No active timer found! Please start a timer first")

#         # Get the current time
#         time_in = datetime.now()

#         # Create a new task to update the timer
#         async def update_timer(message):
#             while True:
#                 # Get the current time
#                 current_time = datetime.now()

#                 # Calculate the elapsed time
#                 elapsed_time = current_time - time_in

#                 # Convert the elapsed time to a string
#                 elapsed_time_str = convert_seconds(elapsed_time.total_seconds())

#                 # Update the timer in the chat
#                 await message.edit(content=f"Elapsed time: {elapsed_time_str}")

#                 # Wait for 1 second before updating the timer again
#                 await asyncio.sleep(1)

#         # Send a message to the chat indicating that the timer has resumed
#         message = await ctx.send(f"Time tracking resumed at {time_in}")

#         # Create a task to update the timer
#         task = bot.loop.create_task(update_timer(message))
#         tasks.append(task)

#     except Exception as e:
#         await ctx.send(f"Error: {str(e)}")

import discord
from datetime import datetime
import asyncio
from config import supabase
from database.utils import update_resumed_at
from time_tracking.utils import convert_seconds, format_datetime
from commands import bot, tasks, timers
from typing import List
from time_tracking.timer import Timer

@bot.command(name='resume')
async def resume(ctx):
    try:
        if ctx.author.id not in timers:
            raise ValueError("No active timer found! Please start a timer first")

        timer = timers[ctx.author.id]
        await timer.resume()

        await ctx.send(f"Time tracking resumed at {format_datetime(datetime.now())}.")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")