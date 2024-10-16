import os
from tabulate import tabulate
from dotenv import load_dotenv
from databricks import sql

complex_query = """
WITH Nutrition_avg AS(
  SELECT cancer, diabetes, heart_disease,
    ROUND(AVG(EGGSFREQ),2) as avg_eggs,
    ROUND(AVG(GREENSALADFREQ),2) as avg_salad,
    ROUND(AVG(FRIESFREQ),2) as avg_fries, 
    ROUND(AVG(MILKFREQ),2) as avg_milk,
    ROUND(AVG(SODAFREQ),2) as avg_soda,
    ROUND(AVG(COFFEEFREQ),2) as avg_coffee,
    ROUND(AVG(CAKESFREQ),2) as avg_cakes
  FROM Nutrition
  GROUP BY cancer, diabetes, heart_disease
)

SELECT ID, n.cancer, n.diabetes, n.heart_disease, 
  ROUND(n.EGGSFREQ-na.avg_eggs,2) as diff_eggs,
  ROUND(n.GREENSALADFREQ-na.avg_salad,2) as diff_salad,
  ROUND(n.FRIESFREQ-na.avg_fries,2) as diff_fries,
  ROUND(n.MILKFREQ-na.avg_milk,2) as diff_milk,
  ROUND(n.SODAFREQ-na.avg_soda,2) as diff_soda,
  ROUND(n.COFFEEFREQ-na.avg_coffee,2) as diff_coffee,
  ROUND(n.CAKESFREQ-na.avg_cakes,2) as diff_cakes
FROM Nutrition as n JOIN Nutrition_avg as na 
  ON n.cancer = na.cancer AND 
     n.diabetes = na.diabetes AND 
     n.heart_disease = na.heart_disease
ORDER BY n.cancer, n.diabetes, n.heart_disease, ID
"""

def query_nutrition():
    load_dotenv()
    with sql.connect (server_hostname = os.getenv ("SERVER_HOSTNAME"),
        http_path=os.getenv("HTTP_PATH" ),
        access_token=os.getenv("DATABRICKS_KEY")
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(complex_query)
            rows = cursor.fetchall()

            headers = ["ID", "cancer", "diabetes", "heart_disease", "diff_eggs", 
                       "diff_salad", "diff_fries", "diff_milk", "diff_soda", 
                       "diff_coffee", "diff_cakes"]
            print(tabulate(rows, headers, tablefmt="grid"))
            
            cursor.close()
            connection.close()

if __name__ == "__main__":
    query_nutrition()