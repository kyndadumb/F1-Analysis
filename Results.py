import fastf1
import pyodbc

fastf1.Cache.enable_cache('cache')

conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=172.26.208.1,1433;"
                      "Database=F12022;"
                      "UID=sa;"
                      "PWD=F12022PyODBC!")
cursor = conn.cursor()

print("connected to database")

create_table_query = """
CREATE TABLE RaceResults (
    RoundNumber INT,
	DriverNumber INT,
    TeamID NVARCHAR(255),
    Position FLOAT,
    ClassifiedPosition NVARCHAR(255),
    GridPosition FLOAT,
    Status NVARCHAR(255),
    Points FLOAT,
    FOREIGN KEY (DriverNumber) REFERENCES Driver(DriverNumber),
    FOREIGN KEY (TeamID) REFERENCES Team(TeamID),
    FOREIGN KEY (RoundNumber) REFERENCES Event(RoundNumber)
)
"""
cursor.execute(create_table_query)
conn.commit()

print("Table RaceResults created!")


for roundnumber in range(1, 23):
    try:
        session = fastf1.get_session(2022, roundnumber, 'R')
        session.load()
        session_result = session.results
        session_roundnumber = int(session.event.RoundNumber)
        for _, row in session_result.iterrows():
            result_drivernumber = int(row['DriverNumber'])
            result_teamid = row['TeamId']
            result_position = float(row['Position'])
            result_classifiedposition = row['ClassifiedPosition']
            result_gridposition = float(row['GridPosition'])   
            result_status = row['Status']
            result_points = float(row['Points'])  

            select_team_query = "SELECT TeamID FROM Team WHERE TeamID = ?"
            cursor.execute(select_team_query, result_teamid)
            team_result = cursor.fetchone()
            if team_result is not None:
                insert_sql = '''
                    INSERT INTO RaceResults (RoundNumber, DriverNumber, TeamId, Position, ClassifiedPosition, GridPosition, Status, Points)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?) '''
                        
                cursor.execute(insert_sql, (session_roundnumber, result_drivernumber, result_teamid, result_position, result_classifiedposition, result_gridposition, result_status, result_points))

                conn.commit()
            else:
                print(f"Team with TeamID {result_teamid} does not exist in the Team table. Skipping insertion.")

    except ValueError as e:
        print(f"An error occurred for round {roundnumber} and session type {session_type}: {str(e)}")

conn.close()