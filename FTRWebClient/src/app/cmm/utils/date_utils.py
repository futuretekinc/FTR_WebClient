from datetime import datetime

def yyyymmdd(dt):
    return "{y}{m:02d}{d:02d}".format(y=dt.year,m=dt.month,d=dt.day)

def hhmm(dt):
    return "{h:02d}{m:02d}".format(h=dt.hour,m=dt.minute)

def ss(dt):
    return "{s}".format(s=dt.second)

def ep_trans_time(time):
    try:
        dt = datetime.fromtimestamp(float(time))
        return (yyyymmdd(dt),hhmm(dt),ss(dt))
    except Exception:
        return (0,0,0)