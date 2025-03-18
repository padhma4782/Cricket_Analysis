import os
import json
from CricketDatabase import CricketDatabaseManager
from dotenv import load_dotenv

load_dotenv()

# Database Connection
DB_HOST = os.getenv('MySQL_host')
DB_USER = os.getenv('MySQL_username')
DB_PASSWORD = os.getenv('MySQL_password')
DB_NAME = os.getenv('MySQL_database')


JSON_FOLDER = "cricsheet_json"

# Connect to Cricket_DB
try:
    cricDBconn = CricketDatabaseManager(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
    
    cursor = cricDBconn.cursor
    print("hello")

    if cricDBconn:
        # Create Tables
        tables = {
            "matches": """
                CREATE TABLE IF NOT EXISTS matches (
                    match_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_type VARCHAR(20),
                    match_number INT,
                    city VARCHAR(100),
                    venue VARCHAR(255),
                    season VARCHAR(20),
                    result VARCHAR(20),
                    toss_winner VARCHAR(50),
                    toss_decision VARCHAR(10)
                );
            """,
            "teams": """
                CREATE TABLE IF NOT EXISTS teams (
                    team_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    team_name VARCHAR(50),
                    FOREIGN KEY (match_id) REFERENCES matches(match_id)
                );
            """,
            "players": """
                CREATE TABLE IF NOT EXISTS players (
                    player_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    team_name VARCHAR(50),
                    player_name VARCHAR(100),
                    FOREIGN KEY (match_id) REFERENCES matches(match_id)
                );
            """,
            "officials": """
                CREATE TABLE IF NOT EXISTS officials (
                    official_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    role VARCHAR(50),
                    name VARCHAR(100),
                    FOREIGN KEY (match_id) REFERENCES matches(match_id)
                );
            """,
            "innings": """
                CREATE TABLE IF NOT EXISTS innings (
                    innings_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    team VARCHAR(50),
                    FOREIGN KEY (match_id) REFERENCES matches(match_id)
                );
            """,
            "deliveries": """
                CREATE TABLE IF NOT EXISTS deliveries (
                    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    innings_id INT,
                    over_number INT,
                    batter VARCHAR(100),
                    bowler VARCHAR(100),
                    non_striker VARCHAR(100),
                    runs_batter INT,
                    runs_extras INT,
                    runs_total INT,
                    FOREIGN KEY (match_id) REFERENCES matches(match_id),
                    FOREIGN KEY (innings_id) REFERENCES innings(innings_id)
                );
            """,
            "wickets": """
                CREATE TABLE IF NOT EXISTS wickets (
                    wicket_id INT AUTO_INCREMENT PRIMARY KEY,
                    match_id INT,
                    delivery_id INT,
                    player_out VARCHAR(100),
                    kind VARCHAR(50),
                    FOREIGN KEY (match_id) REFERENCES matches(match_id),
                    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id)
                );
            """,
        }

        # Execute table creation queries
        for table_name, create_query in tables.items():
            cursor.execute(create_query)

        cricDBconn.connection.commit()


        # Function to process JSON and insert data
        def process_json_file(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    match_data = json.load(file)
                    match_info = match_data["info"]
                    innings_data = match_data["innings"]

                    # Insert into Matches
                    cursor.execute(
                        """
                        INSERT INTO matches (match_type, match_number, city, venue, season, result, toss_winner, toss_decision)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            match_info.get("match_type"),
                            match_info.get("event", {}).get("match_number"),
                            match_info.get("city"),
                            match_info.get("venue"),
                            match_info.get("season"),
                            match_info.get("outcome", {}).get("result", match_info.get("outcome", {}).get("winner", "")),
                            match_info.get("toss", {}).get("winner"),
                            match_info.get("toss", {}).get("decision"),
                        ),
                    )
                    match_id = cursor.lastrowid

                    # Insert into Teams
                    for team in match_info.get("teams", []):
                        cursor.execute("INSERT INTO teams (match_id, team_name) VALUES (%s, %s)", (match_id, team))

                    # Insert into Players
                    for team, players in match_info.get("players", {}).items():
                        for player in players:
                            cursor.execute(
                                "INSERT INTO players (match_id, team_name, player_name) VALUES (%s, %s, %s)",
                                (match_id, team, player),
                            )

                    # Insert into Officials
                    for role, names in match_info.get("officials", {}).items():
                        for name in names:
                            cursor.execute(
                                "INSERT INTO officials (match_id, role, name) VALUES (%s, %s, %s)", (match_id, role, name)
                            )

                    # Insert into Innings & Deliveries
                    for inning in innings_data:
                        team = inning.get("team")
                        cursor.execute("INSERT INTO innings (match_id, team) VALUES (%s, %s)", (match_id, team))
                        innings_id = cursor.lastrowid

                        for over_number, deliveries in enumerate(inning.get("overs", [])):
                            for delivery in deliveries.get("deliveries", []):
                                cursor.execute(
                                    """
                                    INSERT INTO deliveries (match_id, innings_id, over_number, batter, bowler, non_striker, runs_batter, runs_extras, runs_total)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """,
                                    (
                                        match_id,
                                        innings_id,
                                        over_number,
                                        delivery.get("batter"),
                                        delivery.get("bowler"),
                                        delivery.get("non_striker"),
                                        delivery.get("runs", {}).get("batter"),
                                        delivery.get("runs", {}).get("extras"),
                                        delivery.get("runs", {}).get("total"),
                                    ),
                                )
                                delivery_id = cursor.lastrowid

                                # Insert into Wickets
                                if "wickets" in delivery:
                                    for wicket in delivery["wickets"]:
                                        cursor.execute(
                                            """
                                            INSERT INTO wickets (match_id, delivery_id, player_out, kind)
                                            VALUES (%s, %s, %s, %s)
                                            """,
                                            (match_id, delivery_id, wicket.get("player_out"), wicket.get("kind")),
                                        )
                except json.JSONDecodeError as e:
                    print(f"Error parsing {file_path}: {e}")

        # Process each JSON file in the `cricsheet_json` folder
        for json_file in os.listdir(JSON_FOLDER):
            if json_file.endswith(".json"):
                try:
                    process_json_file(os.path.join(JSON_FOLDER, json_file))
                except Exception as e:
                    error_message = f"Error parsing {json_file}: {e}\n"
                    with open("error_log.txt", "a") as error_file:
                        error_file.write(error_message)

        # Commit changes
        cricDBconn.connection.commit()

        # Close connection
        cricDBconn.cursor.close()
        cricDBconn.connection.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")
