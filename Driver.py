import fastf1
import pyodbc

# Verbindung zur Datenbank herstellen
conn = pyodbc.connect("Driver={SQL Server};"
                      "Server=172.26.208.1,1433;"
                      "Database=F12022;"
                      "UID=sa;"
                      "PWD=F12022PyODBC!")
cursor = conn.cursor()

# Funktion zum Überprüfen und Einfügen eines Fahrers in die Tabelle "Driver"
def check_and_insert_driver(driver_number, driver_fullname, driver_abbreviation, driver_countrycode, driver_headshot, team_id):
    select_query = "SELECT DriverNumber FROM Driver WHERE DriverNumber = ?"
    cursor.execute(select_query, driver_number)
    result = cursor.fetchone()
    if result is None:
        insert_query = '''
            INSERT INTO Driver (DriverNumber, FullName, Abbreviation, CountryCode, HeadshotURL, TeamID)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        if team_id != "nan":
            cursor.execute(insert_query, driver_number, driver_fullname, driver_abbreviation, driver_countrycode, driver_headshot, team_id)
            conn.commit()
            print(f"Driver with DriverNumber {driver_number} inserted into the Driver table.")
        else:
            print(f"Driver with DriverNumber {driver_number} has 'nan' team_id and will not be inserted into the Driver table.")

# Code zum Abrufen der Session-Daten und Überprüfen/Einfügen der Fahrer in die Tabelle "Driver"
for roundnumber in range(1, 22):
    for session_type in ['FP1', 'FP2', 'FP3','Q','R', 'S','SQ']:
        try:
            session = fastf1.get_session(2022, roundnumber, session_type)
            session.load()
            session_results = session.results

            for index in range(len(session_results)):
                driver_number = session_results['DriverNumber'][index]
                driver_fullname = session_results['FullName'][index]
                driver_abbreviation = session_results['Abbreviation'][index]
                driver_countrycode = session_results['CountryCode'][index]
                driver_headshot = session_results['HeadshotUrl'][index]
                team_id = session_results['TeamId'][index]

                check_and_insert_driver(driver_number, driver_fullname, driver_abbreviation, driver_countrycode, driver_headshot, team_id)

        except ValueError as e:
            print(f"An error occurred: {str(e)}")

# Datenbankverbindung schließen
conn.close()
