import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from CricketDatabase import CricketDatabaseManager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

# Database Connection
DB_HOST = os.getenv('MySQL_host')
DB_USER = os.getenv('MySQL_username')
DB_PASSWORD = os.getenv('MySQL_password')
DB_NAME = os.getenv('MySQL_database')

encoded_password = quote_plus(DB_PASSWORD)
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"
try:
    #cricDBconn = CricketDatabaseManager(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
    engine = create_engine(DATABASE_URL)
    #cursor = cricDBconn.cursor
    print("*****connected****")

    if engine:
        print("***inside engine****")
    # 1. Top 10 Batsmen by Total Runs in ODIs   
        query = """
            SELECT batter, SUM(runs_batter) AS total_runs
            FROM deliveries
            JOIN matches ON deliveries.match_id = matches.match_id
            WHERE matches.match_type = 'ODI'
            GROUP BY batter
            ORDER BY total_runs DESC
            LIMIT 10;
        """
        data = pd.read_sql(query, engine)
        plt.figure(figsize=(10, 6))
        sns.barplot(y="batter", x="total_runs", data=data, palette="Blues_r")
        plt.title("Top 10 Batsmen by Runs in ODIs")
        plt.xlabel("Total Runs")
        plt.ylabel("Batter")
        plt.show()
    # 2. Leading Wicket-Takers in T20 Matches
        query = """
            SELECT bowler, COUNT(*) AS total_wickets
            FROM deliveries
            JOIN matches ON deliveries.match_id = matches.match_id
            WHERE matches.match_type = 'T20' AND runs_total = 0
            GROUP BY bowler
            ORDER BY total_wickets DESC
            LIMIT 10;
        """
        data = pd.read_sql(query, engine)
        plt.figure(figsize=(10, 6))
        sns.barplot(y="bowler", x="total_wickets", data=data, palette="Reds_r")
        plt.title("Top 10 Wicket-Takers in T20s")
        plt.xlabel("Total Wickets")
        plt.ylabel("Bowler")
        plt.show()

        # 3. Team Win in Matches in descending order
        query = """
        SELECT result, COUNT(result) AS total_wins
        FROM matches
        WHERE result NOT IN ('Draw', 'Tie', 'No Result')
        GROUP BY result
        ORDER BY total_wins DESC
        LIMIT 3;
        """
        data = pd.read_sql(query, engine)
        plt.figure(figsize=(10, 6))
        sns.barplot(y="total_wins", x="result", data=data, palette="Greens_r")
        plt.title("Team Win  in Matches")
        plt.xlabel("Team")
        plt.ylabel("Win")
        plt.show()

        # 4. Total count for each Match Type played 
        query = """
        SELECT match_type, COUNT(*) AS total_count
        FROM matches
        Group by match_type
        """
        data = pd.read_sql(query, engine)
        plt.figure(figsize=(8, 5))
        sns.barplot(x="match_type", y="total_count", data=data, palette="coolwarm")
        plt.title("Total Centuries by Match Type")
        plt.xlabel("Match Type")
        plt.ylabel("Total played")
        plt.show()

        # 5. Matches Played Per Year
        query = """
                SELECT season AS year_played, COUNT(*) AS total_matches
                FROM matches
                GROUP BY year_played
                ORDER BY year_played DESC
                LIMIT 10;
                """
        data = pd.read_sql(query, engine)
        plt.figure(figsize=(12, 5))
        sns.lineplot(x="year_played", y="total_matches", data=data, marker="o", color="purple")
        plt.title("Matches Played Per Year")
        plt.xlabel("Year")
        plt.ylabel("Total Matches")
        plt.xticks(rotation=45)
        plt.show()
except SQLAlchemyError as e:
    print(f"Error connecting to the database: {e}")
    engine = None