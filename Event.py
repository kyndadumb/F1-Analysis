import fastf1
import pyodbc

fastf1.Cache.enable_cache(cache_dir="cache")

year = 2022

conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=172.26.208.1,1433;"
                      "Database=F12022;"
                      "UID=sa;"
                      "PWD=F12022PyODBC!")
cursor = conn.cursor()

for x in range(1, 23):
    event = fastf1.get_event(year, x)
    
    event_data = {
        'RoundNumber': int(event.RoundNumber),
        'Country': event.Country,
        'Location': event.Location,
        'OfficialEventName': event.OfficialEventName,
        'EventName': event.EventName,
        'EventFormat': event.EventFormat,
        'Session1': event.Session1,
        'Session1Date': event.Session1Date,
        'Session2': event.Session2,
        'Session2Date': event.Session2Date,
        'Session3': event.Session3,
        'Session3Date': event.Session3Date,
        'Session4': event.Session4,
        'Session4Date': event.Session4Date,
        'Session5': event.Session5,
        'Session5Date': event.Session5Date,
    }

    sql = '''
        INSERT INTO Event (
            RoundNumber, Country, Location, OfficialEventName,
            EventName, EventFormat, Session1, Session1Date, Session2,
            Session2Date, Session3, Session3Date, Session4, Session4Date,
            Session5, Session5Date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(sql, tuple(event_data.values()))
    conn.commit()

    print(event.EventName + " added!")
