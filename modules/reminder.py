
import re
from datetime import datetime
from dateutil import parser
from dateutil import tz
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
sched = AsyncIOScheduler()
sched.start()

def parse_datetime(dt):
    compiled = re.compile("""(?:(?P<years>[0-9])(?:years?|y))?
                             (?:(?P<months>[0-9]{1,2})(?:months?|mo))?
                             (?:(?P<weeks>[0-9]{1,4})(?:weeks?|w))?
                             (?:(?P<days>[0-9]{1,5})(?:days?|d))?
                             (?:(?P<hours>[0-9]{1,5})(?:hours?|h))?
                             (?:(?P<minutes>[0-9]{1,5})(?:minutes?|m))?
                             (?:(?P<seconds>[0-9]{1,5})(?:seconds?|s))?
                             """, re.VERBOSE)

    match = compiled.fullmatch(dt)
    if match is None or not match.group(0):
        try:
            tzinfos = {"CEST": tz.gettz("Europe/Berlin")}
            dt = parser.parse(f"{dt} CEST", tzinfos=tzinfos)
            return dt
        except:
            return None

    data = { k: int(v) for k, v in match.groupdict(default=0).items() }
    now = datetime.now()
    dt = now + relativedelta(**data)
    return dt


class Reminder:
    def __init__(self, _datetime, msg, user, message, time, here, di):
        self._datetime = _datetime
        self.msg = msg
        self.user = user
        self.message = message
        self.time = time
        self.here=here
        self.di = di
        sched.add_job(self.send_reminder, self.di, run_date=self._datetime)

    async def send_reminder(self):
        if self.here:
            await self.message.channel.send(self.msg)
        else:
            await self.user.send(self.msg)


async def remindme(message,time,msg,here=False):
    user = message.author

    dt = parse_datetime(time)
    if dt == None:
        print('error resolving datetime')
        await message.channel.send('error resolving datetime')
        return

    Reminder(dt, msg, user, message, time, here, 'date')
    await message.channel.send("I'll remind you then!")