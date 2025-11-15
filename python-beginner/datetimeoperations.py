from datetime import datetime, date, time, timedelta
import pytz   # pip install pytz

# --------------------------------------------------------
# 1. CURRENT DATE AND TIME
# --------------------------------------------------------
now = datetime.now()
today = date.today()

print("Now:", now)
print("Today:", today)


# --------------------------------------------------------
# 2. FORMAT DATE/TIME TO STRING
# --------------------------------------------------------
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted:", formatted)

# Common formats:
# %Y = year, %m = month, %d = day
# %H = hour, %M = minute, %S = second


# --------------------------------------------------------
# 3. PARSE STRING TO DATE/TIME
# --------------------------------------------------------
date_str = "2025-11-15 18:30:00"
parsed_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print("Parsed datetime:", parsed_dt)


# --------------------------------------------------------
# 4. ADD / SUBTRACT DAYS, MONTHS, HOURS
# --------------------------------------------------------
one_week_later = now + timedelta(days=7)
two_hours_before = now - timedelta(hours=2)

print("One week later:", one_week_later)
print("Two hours before:", two_hours_before)


# --------------------------------------------------------
# 5. DIFFERENCE BETWEEN DATES
# --------------------------------------------------------
d1 = datetime(2025, 11, 1)
d2 = datetime(2025, 11, 15)

diff = d2 - d1
print("Difference in days:", diff.days)
print("Difference full:", diff)


# --------------------------------------------------------
# 6. COMPARING DATES
# --------------------------------------------------------
if d2 > d1:
    print("d2 is after d1")


# --------------------------------------------------------
# 7. TIMEZONE CONVERSION (IMPORTANT)
# --------------------------------------------------------
uae = pytz.timezone("Asia/Dubai")
india = pytz.timezone("Asia/Kolkata")

uae_now = datetime.now(uae)
india_now = uae_now.astimezone(india)

print("UAE Time:", uae_now)
print("India Time:", india_now)


# --------------------------------------------------------
# 8. EPOCH TIMESTAMP (UNIX TIME)
# --------------------------------------------------------
timestamp = now.timestamp()
print("Timestamp:", timestamp)

# Convert timestamp to datetime
from_ts = datetime.fromtimestamp(timestamp)
print("From timestamp:", from_ts)


# --------------------------------------------------------
# 9. START AND END OF DAY
# --------------------------------------------------------
start_day = datetime.combine(today, time.min)
end_day = datetime.combine(today, time.max)

print("Start of day:", start_day)
print("End of day:", end_day)


# --------------------------------------------------------
# 10. UTILITY FUNCTIONS
# --------------------------------------------------------

def to_yyyymmdd(dt):
    return dt.strftime("%Y%m%d")

def next_monday(dt):
    return dt + timedelta(days=(7 - dt.weekday()))

print("YYYYMMDD:", to_yyyymmdd(now))
print("Next Monday:", next_monday(now))