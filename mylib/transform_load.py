import os
import pandas as pd
from dotenv import load_dotenv
from databricks import sql

# load the csv file and insert into a new databricks database
def load(dataset="data/Nutrition.csv"):
    """Transforms and Loads data into the databricks database"""
    payload = pd.read_csv(dataset)
    load_dotenv()
    with sql.connect (server_hostname = os.getenv ("SERVER_HOSTNAME"),
        http_path=os.getenv("HTTP_PATH" ),
        access_token=os.getenv("DATABRICKS_KEY")
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Nutrition (
                ID INTEGER PRIMARY KEY,
                cancer STRING,
                diabetes STRING,
                heart_disease STRING,
                EGGSFREQ INTEGER,
                GREENSALADFREQ INTEGER,
                FRIESFREQ INTEGER,
                MILKFREQ INTEGER,
                SODAFREQ INTEGER,
                COFFEEFREQ INTEGER,
                CAKESFREQ INTEGER
            )
            ''')

            cursor.execute("SELECT * FROM Nutrition VALUES")
            check_data = cursor.fetchall()
            if not check_data:
                print('Inserting data into Nutrition table...')
                cursor.executemany('''
                INSERT INTO Nutrition (
                    ID, cancer, diabetes, heart_disease, 
                    EGGSFREQ, GREENSALADFREQ, FRIESFREQ, 
                    MILKFREQ, SODAFREQ, COFFEEFREQ, CAKESFREQ
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', [tuple(row) for row in payload.itertuples(index=False, name=None)])


            cursor.close()
            connection.close()


if __name__ == "__main__":
    load()