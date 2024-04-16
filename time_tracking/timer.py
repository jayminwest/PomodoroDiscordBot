import asyncio
from datetime import datetime
from time_tracking.utils import convert_seconds

class Timer:
    def __init__(self):
        self.start_time = None
        self.paused_time = 0

    async def start(self):
        self.start_time = datetime.now()
        while True:
            current_time = datetime.now()
            elapsed_time = current_time - self.start_time
            print(f"Elapsed time: {elapsed_time.total_seconds()} seconds")
            await asyncio.sleep(1)

    async def pause(self):
        self.paused_time += (datetime.now() - self.start_time).total_seconds()
        self.start_time = None

    async def resume(self):
        self.start_time = datetime.now()

    async def stop(self):
        self.paused_time += (datetime.now() - self.start_time).total_seconds()
        self.start_time = None

    def get_elapsed_time(self) -> str:
        if self.start_time is None:
            return "Timer not started"
        elif self.paused_time == 0:
            elapsed_time = datetime.now() - self.start_time
            return convert_seconds(elapsed_time.total_seconds())
        else:
            elapsed_time = self.paused_time + (datetime.now() - self.start_time).total_seconds()
            return convert_seconds(elapsed_time)