
import datetime

def get_live_time_berlin():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

print(get_live_time_berlin())



