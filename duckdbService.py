import logging
import os
import subprocess
import sys

import duckdb
import pandas as pd
from pandas import DataFrame
from streamlit.logger import get_logger

def create_database_if_not_exists():
    app_logger = get_logger(__name__)
    app_logger.setLevel(logging.INFO)
    # duckdb database set up
    if "data" not in os.listdir():
        app_logger.info("duckdb database set up")
        app_logger.info("List working directory content: %s", os.listdir())
        app_logger.info("Create 'data' folder, if it doesn't exist")
        os.makedirs("data", exist_ok=True)

    if "exercises_sql_tables.duckdb" not in os.listdir("data"):
        app_logger.info("Create Database and tables")
        subprocess.run([f"{sys.executable}", "init_db.py"], check=False)


class duckdbService:
    def __init__(self):
        create_database_if_not_exists()
        self.con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

    def get_themes(self) -> list[str]:
        query = """
            SELECT DISTINCT theme FROM memory_state
        """
        return self.con.execute(query).df()["theme"].tolist()

    def get_exercises_per_theme(self, theme: str) -> DataFrame:
        return self.con.query(
            f"SELECT * FROM memory_state WHERE theme = '{theme}' ORDER BY last_reviewed"
        ).df()

    def get_exercises_list_per_theme(self, theme: str) -> list[str]:
        return self.get_exercises_per_theme(theme)["exercice_name"].tolist()

    def get_exercise_answer_query(self,  theme: str, exercise_index: int) -> str:
        ANSWER_FILE_PATH = self.get_exercises_per_theme(theme).loc[exercise_index, "answers"]
        with open(ANSWER_FILE_PATH, "r") as file:
            return file.read()

    def get_exercise_answer_df(self, theme: str, exercise_index: int) -> DataFrame:
        try:
            ANSWER_QUERY = self.get_exercise_answer_query(theme, exercise_index)
            EXPECTED_DF = self.con.query(ANSWER_QUERY).df()
        except Exception as e:
            EXPECTED_DF = pd.DataFrame()
        return EXPECTED_DF

    def get_exercise_question(self, theme: str, exercise_index: int) -> str:
        return (self.get_exercises_per_theme(theme)
                    .loc[exercise_index, "questions"])

    def get_exercise_tables(self, theme:str, exercise_index: int) -> list[DataFrame]:
        return (self.get_exercises_per_theme(theme)
                    .loc[exercise_index, "tables"].tolist())

    def execute_query(self, query: str) -> DataFrame:
        return self.con.execute(query).df()