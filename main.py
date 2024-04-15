from commands.start import start
from commands.stop import stop
from commands.pomodoro import pomodoro
from commands.totaltime import totaltime
from commands.help import help
from commands import bot
from config import TOKEN, supabase

# @bot.event
# async def on_disconnect():
#     cur.close()
#     conn.close()

bot.run(TOKEN)