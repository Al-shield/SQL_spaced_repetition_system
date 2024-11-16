# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import random

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# --------------
# Exercice List
# --------------
DEFAULT_LAST_REVIEWED = "1970-01-01"
ANSWERS_FOLDER = "answers"
exercice_list = {
    "theme": ["JOIN", "JOIN", "GROUP BY"],
    "exercice_name": ["customers_and_stores", "self_meetings", "average_meetings"],
    "tables": [
        ["df_customers", "df_stores", "df_store_products", "df_products"],
        ["df_meetings_persons"],
        ["df_meetings_persons"],
    ],
    "last_reviewed": [
        DEFAULT_LAST_REVIEWED,
        DEFAULT_LAST_REVIEWED,
        DEFAULT_LAST_REVIEWED,
    ],
    "questions": [
        "Récupérer tous les clients avec leurs magasin s'il en ont un",
        """
        Pour calculer le temps que Benjamin passe en réunion en fonction de qui d'autre est présent, il faut:
        - créer une table avec toutes les combinaisons de personnes ayant assisté au même meeting
        - ne garder que les records qui concernent Benjamin
        - enlever les records où il est en réunion "avec lui-même"
        """,
        "Faire un group by pour savoir la durée moyenne de mes meetings avec chaque personne. Ne garder que les résultats pour lesquels la moyenne est > à 1h",
    ],
    "answers": [
        f"{ANSWERS_FOLDER}/customers_and_stores.sql",
        f"{ANSWERS_FOLDER}/self_meetings.sql",
        f"{ANSWERS_FOLDER}/average_meetings.sql",
    ],
}
exercice_list_df = pd.DataFrame(exercice_list)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM exercice_list_df")

# --------------------------
# Customer Store Exercice
# --------------------------
customers_data = {
    "customer_id": [11, 12, 13, 14, 15],
    "customer_name": ["Zeinaba", "Tancrède", "Israel", "Kaouter", "Alan"],
}
stores_data = {"store_id": [1, 2, 3, 4], "customer_id": [11, 12, 13, 15]}
store_products_data = {
    "store_id": [1, 1, 1, 2, 2, 3, 4],
    "product_id": [101, 103, 105, 101, 103, 104, 105],
}
p_names = [
    "Cherry coke",
    "Laptop",
    "Ipad",
    "Livre",
]
products_data = {
    "product_id": [100, 101, 103, 104],
    "product_name": p_names,
    "product_price": [3, 800, 400, 30],
}
df_customers = pd.DataFrame(customers_data)
df_stores = pd.DataFrame(stores_data)
df_store_products = pd.DataFrame(store_products_data)
df_products = pd.DataFrame(products_data)

con.execute("CREATE TABLE IF NOT EXISTS df_customers AS SELECT * FROM df_customers")
con.execute("CREATE TABLE IF NOT EXISTS df_stores AS SELECT * FROM df_stores")
con.execute(
    "CREATE TABLE IF NOT EXISTS df_store_products AS SELECT * FROM df_store_products"
)
con.execute("CREATE TABLE IF NOT EXISTS df_products AS SELECT * FROM df_products")

# --------------------------
# Meeting Exercice
# --------------------------

person_names = ["Benjamin", "Florian", "Tarik", "Bob", "Sirine", "Alice"]

meetings_data = []
for meeting_id in range(150):
    persons_in_meet = random.sample(person_names, random.randint(1, 5))
    for person_name in persons_in_meet:
        meetings_data.append((meeting_id, person_name))
meetings_df = pd.DataFrame(meetings_data, columns=["meeting_id", "person_name"])

meeting_durations = []
for meeting_id in meetings_df["meeting_id"].unique():
    duration = random.randint(10, 60)  # You can adjust the range as needed
    meeting_durations.append((meeting_id, duration))
durations_df = pd.DataFrame(
    meeting_durations, columns=["meeting_id", "duration_minutes"]
)

average_duration = durations_df["duration_minutes"].mean()
meetings_with_flo = meetings_df[meetings_df["person_name"] == "Florian"][
    "meeting_id"
].unique()
for _, row in durations_df.iterrows():
    if row["meeting_id"] in meetings_with_flo:
        row["duration_minutes"] += random.randint(50, 55)

meetings_persons_df = meetings_df.merge(durations_df, on="meeting_id")
con.execute(
    "CREATE TABLE IF NOT EXISTS df_meetings_persons AS SELECT * FROM meetings_persons_df"
)

con.close()
