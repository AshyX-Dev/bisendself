from pytz import timezone
from datetime import datetime

def getTehranTimezone() -> datetime:
    return datetime.now(timezone("Asia/Tehran"))
