from datetime import datetime, timedelta

delta = timedelta(
    days=0,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=10,
    hours=0,
    weeks=0
)

dt_start = datetime.now()
dt_end = datetime(2024,1,30,10,50,1)
dt = dt_start

while dt<dt_end:

    if dt.date() == datetime(2024, 9, 7).date():
        print(dt) #твоё условие
    dt += delta
    print(dt) #твоё условие
    
