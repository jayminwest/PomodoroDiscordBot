from datetime import datetime
from commands import bot, tasks
from database.utils import update_time_tracking_row, get_data
from time_tracking.utils import convert_seconds

# Command to stop tracking time
@bot.command(name='stop')
async def stop(ctx):
    """
    Stop tracking time.

    This function stops the time tracking process and updates the database with the total duration.
    
    Parameters:
        ctx (Context): The context of the command invocation.

    Returns:
        None

    Raises:
        ValueError: If no active timer is found.
        Exception: If there's an error while stopping the timer or updating the database.
    """
    try:
        time_out = datetime.now()

        data = get_data(ctx, "time_in")

        if not data.data[0]:
            raise ValueError("No active timer found! Please start a timer first")
        
        time_in = data.data[0].get("time_in")
        time_in = datetime.strptime(time_in, "%Y-%m-%dT%H:%M:%S")

        duration = time_out - time_in
        total_seconds = duration.seconds
        update_time_tracking_row(ctx, time_in, time_out, total_seconds)
        
        await ctx.send(f"Time tracking stopped at {time_out}. Total duration: {convert_seconds(total_seconds)}")

        # Cancel all the tasks that are currently running
        for task in tasks:
            task.cancel()
        tasks.clear()

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")