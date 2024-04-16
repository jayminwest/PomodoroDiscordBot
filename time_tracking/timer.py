import asyncio
from datetime import datetime
from time_tracking.utils import convert_seconds
from database.utils import update_paused_at, add_time_tracking_row, update_resumed_at
from commands import tasks, bot

class Timer:
    def __init__(self, user_id=None, start_time=None, message=None, paused_at=0):
        self.user_id = user_id
        self.start_time = start_time
        self.message = message
        self.paused_at = paused_at
        self.paused = False
        self.resumed_at = None

    async def start(self):
        # Updating the database:
        add_time_tracking_row(self.user_id, self.start_time)
        while not self.paused:
            # Get the elapsed time from the timer
            elapsed_time_str = self.get_elapsed_time()
            
            # Update the message with the elapsed time
            await self.message.edit(content=f"Elapsed time: {elapsed_time_str}")

            # Wait for 1 second before updating the timer again
            await asyncio.sleep(1)

    async def pause(self):
        self.paused = True

        update_paused_at(self.user_id, self.start_time, datetime.now())

        await self.message.edit(content=f"Elapsed time: {self.get_elapsed_time()} - PAUSED")
        
    async def resume(self):
        self.paused = False
        self.resumed_at = datetime.now()

        # Update the database:
        update_resumed_at(self.user_id, self.start_time, self.resumed_at)

        # Start a new task to continue updating the timer
        task = bot.loop.create_task(self.start())
        tasks.append(task)

        await self.message.edit(content=f"Elapsed time: {self.get_elapsed_time()}")

    async def stop(self):
        self.paused_at += (datetime.now() - self.start_time).total_seconds()
        self.start_time = None

    def get_elapsed_time(self) -> str:
        if self.start_time is None:
            return "Timer not started"
        elif self.paused_at == 0:
            elapsed_time = datetime.now() - self.start_time
            return convert_seconds(elapsed_time.total_seconds())
        else:
            elapsed_time = self.paused_at + (datetime.now() - self.start_time).total_seconds()
            return convert_seconds(elapsed_time)
