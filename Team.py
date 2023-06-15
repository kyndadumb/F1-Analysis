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

cursor.execute('''
    CREATE TABLE Team (
        TeamID NVARCHAR(255) PRIMARY KEY,
        TeamName NVARCHAR(255),
        TeamColor NVARCHAR(255)
    )
''')

conn.commit()

print ("Table Team created!")

team_data = [
    {'TeamID': 'red_bull', 'TeamName': 'Red Bull Racing', 'TeamColor': '#0600EF'},
    {'TeamID': 'alphatauri', 'TeamName': 'AlphaTauri', 'TeamColor': '#2B4562'},
    {'TeamID': 'ferrari', 'TeamName': 'Ferrari', 'TeamColor': '#DC0000'},
    {'TeamID': 'mercedes', 'TeamName': 'Mercedes', 'TeamColor': '#00D2BE'},
    {'TeamID': 'aston_martin', 'TeamName': 'Aston Martin', 'TeamColor': '#006F62'},
    {'TeamID': 'alpine', 'TeamName': 'Alpine', 'TeamColor': '#0090FF'},
    {'TeamID': 'williams', 'TeamName': 'Williams', 'TeamColor': '#005AFF'},
    {'TeamID': 'haas', 'TeamName': 'Haas F1 Team', 'TeamColor': '#787878'},
    {'TeamID': 'alfa', 'TeamName': 'Alfa Romeo', 'TeamColor': '#900000'},
    {'TeamID': 'mclaren', 'TeamName': 'McLaren', 'TeamColor': '#FF8700'}
]

for team in team_data:
    team_id = team['TeamID']
    team_name = team['TeamName']
    team_color = team['TeamColor']
    
    # SQL-Abfrage zum Einfügen der Daten
    insert_query = "INSERT INTO Team (TeamID, TeamName, TeamColor) VALUES (?, ?, ?)"
    
    # Parameterwerte für die SQL-Abfrage
    params = (team_id, team_name, team_color)
    
    # Daten in die Datenbank einfügen
    cursor.execute(insert_query, params)

    print("Wrote: " + team_name)

conn.commit()
conn.close()