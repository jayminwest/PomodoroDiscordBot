import asyncio
from datetime import datetime
from time_tracking.utils import convert_seconds
from database.utils import update_paused_at, add_time_tracking_row, update_resumed_at
from commands import tasks, bot

class Timer:
    def __init__(self, user_id=None, start_time=None, message=None, paused_at=None):
        """
        Initialize a new Timer object.

        Parameters:
            user_id (int): The ID of the user who started the timer.
            start_time (datetime): The time when the timer was started.
            message (Message): The message object to be edited with the updated timer.
            paused_at (datetime): The time the timer was last paused

        Returns:
            None
        """
        self.user_id = user_id
        self.start_time = start_time
        self.message = message
        self.paused_at = paused_at
        self.paused = False
        self.resumed_at = None
        self.task = None

    async def start(self):
        """
        Start the timer.

        Returns:
            None
        """
        try:
            if self.user_id not in tasks:
                tasks[self.user_id] = []
            task = bot.loop.create_task(self.update_timer())
            tasks[self.user_id].append(task)

            # Updating the database:
            add_time_tracking_row(self.user_id, self.start_time)
        
        except Exception as e:
            await self.message.edit(content=f"Error: {str(e)}")
    
    async def update_timer(self):
        """
        Update the timer in the chat every second.

        Returns:
            None
        """
        while True:
            if self.start_time is None:
                await self.message.edit(content="Timer not started")
                break

            if self.paused is False:
                elapsed_time = datetime.now() - self.start_time
                if self.paused_at:
                    elapsed_time += self.paused_at - self.start_time
                await self.message.edit(content=f"Elapsed time: {convert_seconds(elapsed_time.total_seconds())}")
            else:
                elapsed_time = self.paused_at - self.start_time
                await self.message.edit(content=f"Elapsed time: {convert_seconds(elapsed_time.total_seconds())} - PAUSED")
            
            await asyncio.sleep(1)

    async def pause(self):
        """
        Pause the timer.

        Returns:
            None
        """
        self.paused = True
        if self.task:
            self.task.cancel()
        self.paused_at = datetime.now()
        update_paused_at(self.user_id, self.start_time, self.paused_at)
        await self.message.edit(content=f"Elapsed time: {self.get_elapsed_time()} - PAUSED")

    async def resume(self):
        """
        Resume the timer.

        Returns:
            None
        """
        self.paused = False
        self.resumed_at = datetime.now()
        update_resumed_at(self.user_id, self.start_time, self.resumed_at)
        self.task = bot.loop.create_task(self.update_timer())
        tasks[self.user_id].append(self.task)
        await self.message.edit(content=f"Elapsed time: {self.get_elapsed_time()}")

    async def stop(self):
        """
        Stop the timer.

        Returns:
            None
        """
        # self.paused_at += (datetime.now() - self.start_time).total_seconds()
        # self.start_time = None

    def get_elapsed_time(self) -> str:
        """
        Get the elapsed time of the timer.

        Returns:
            str: A string representing the elapsed time in the format HH:MM:SS.
        """
        if self.start_time is None:
            return "Timer not started"
        elif self.paused:
            elapsed_time = self.paused_at - self.start_time
        else:
            elapsed_time = datetime.now() - self.start_time
        return convert_seconds(elapsed_time.total_seconds())