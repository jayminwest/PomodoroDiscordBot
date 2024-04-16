from config import supabase
from database.utils import add_time_tracking_row
from time_tracking.utils import convert_seconds
from commands import bot
from datetime import timedelta, datetime
from database.utils import get_data

# Command to get total time spent
@bot.command(name='totaltime')
async def totaltime(ctx, start_date=None, end_date=None):
    """
    Get the total time spent between the start and end dates.

    Parameters:
    ctx (Context): The context of the command invocation.
    start_date (str): The start date in the format 'YYYY-MM-DD'. Defaults to None.
    end_date (str): The end date in the format 'YYYY-MM-DD'. Defaults to None.

    Returns:
    None

    Raises:
    ValueError: If the start_date or end_date is not in the format 'YYYY-MM-DD'.

    """

    # Validate input dates
    if (start_date and end_date):
        try:
            # Attempt conversion from string to datetime object 
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")

        except ValueError:
            await ctx.send("Invalid date format. Please ensure they follow YYYY-MM-DD pattern.")

    else:  # No value error occurred - continue processing data
        try:
            data = get_data(ctx, "duration", start_date, end_date)
        
            result = data.data
            
            if result:
                total_seconds = sum(parse_duration(row.get("duration")).total_seconds() for row in result)

                if total_seconds:
                    await ctx.send(f"Total time: {convert_seconds(total_seconds)}")
                    
                else:
                    await ctx.send("No time tracking data found.")
                
            else:
                await ctx.send("No time tracking data found.")
            
        except TypeError as te:
            await ctx.send(f"A Type Error has occurred: {te}")
        
        except KeyError as ke:
            await ctx.send(f"A Key Error has occurred: {ke}")

        except Exception as e:
            await ctx.send(f"Error: {str(e)}")  

def parse_duration(duration_str):
    """
    Parses a duration string in the format 'hours:minutes:seconds' and returns a timedelta object.
    
    Parameters:
        duration_str (str): A string representing the duration in the format 'hours:minutes:seconds'.
        
    Returns:
        timedelta: A timedelta object representing the parsed duration.
    """
    hours, minutes, seconds = map(int, duration_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)