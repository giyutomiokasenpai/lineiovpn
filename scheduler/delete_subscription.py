from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import pytz

from database.delete_subscription import delete_subscription
from database.broadcasts_db import broadcast_continue

async def check_subscription():
    await delete_subscription()
    await broadcast_continue()

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_subscription,
        CronTrigger(hour=21, minute=00, timezone=pytz.utc)
    )
    scheduler.start()