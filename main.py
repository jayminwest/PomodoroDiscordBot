"""
TODO: 
- Finish implementing the pause and resume commands
    - Add functionality for pause and resume to the database
- Alter the code so that the timer is updated in the chat upon pause and resume
    - This could be done with a single task that is created when the timer is started and updated when the timer is paused or resumed
        - How to implement this?

        
For DA WORK:

I would like you to help me refactor some code from a discord bot that I am working on. The bot acts as a timer for a user to track the amount of time they spend studying. Right now it as structured as following: 
main.py: intilizes and runs the bot
commands/
-start.py
-stop.py
-pause.py
-resume.py
-pomodoro.py: begins a pomodoro timer
-totaltime.py: prints the user's total time tracked
-help.py
-__init__.py
database/
-utils.py
time_tracking/
-timer.py: acts as a single class for the user's timer
-utils.py
"""

from commands import bot, start, stop, pomodoro, totaltime, help, pause, resume
from config import TOKEN

bot.run(TOKEN)