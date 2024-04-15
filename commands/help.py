import discord
from commands import bot

# Custom help command
bot.remove_command('help')

@bot.command(name='help')
async def help(ctx):
    """
    Display the help message.

    Parameters:
    ctx (Context): The context of the command invocation.
    """
    embed = discord.Embed(title="Help", description="List of available commands:")
    embed.add_field(name="!start", value="Start tracking time", inline=False)
    embed.add_field(name="!stop", value="Stop tracking time", inline=False)
    embed.add_field(name="!pomodoro work_time break_time ", value="Start a pomodoro session (default intervals are 25 and 5 minutes)", inline=False)
    embed.add_field(name="!totaltime start_date end_date ", value="Get total time spent between two dates (default is all time)", inline=False)
    await ctx.send(embed=embed)