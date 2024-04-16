"""
TODO: 
- Finish implementing the pause and resume commands
    - Add functionality for pause and resume to the database
- Alter the code so that the timer is updated in the chat upon pause and resume

"""

from commands import bot, start, stop, pomodoro, totaltime, help, pause, resume
from config import TOKEN

bot.run(TOKEN)