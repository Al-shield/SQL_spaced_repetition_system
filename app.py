import os
import subprocess
import sys

import duckdb
import pandas as pd
import streamlit as st
import logging

from solution_resolver import check_answer
from streamlit.logger import get_logger


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

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

def print_df(name, df):
    st.write(name)
    st.write(df)

with st.sidebar:
    currentTheme = st.selectbox(
        "Que souhaitez-vous réviser ?",
        ["JOIN", "GROUP BY"],
        placeholder="Sélectionner un thème",
    )
    st.write(f"Thème actuel : {currentTheme}")
    exercises = con.query(f"SELECT * FROM memory_state WHERE theme = '{currentTheme}' ORDER BY last_reviewed").df()
    st.write("Exercices disponibles:")
    for exercise_name in exercises['exercice_name'].tolist():
        st.write(exercise_name)

    ANSWER_FILE_PATH = exercises.loc[0, "answers"]
    try:
        with open(ANSWER_FILE_PATH, "r") as file:
            ANSWER_QUERY = file.read()
        EXECTED_DF = con.query(ANSWER_QUERY).df()
    except Exception as e:
        EXECTED_DF = pd.DataFrame()
    exercise_question = exercises.loc[0, "questions"]

st.header("Entrer votre requête")
client_query = st.text_area(
    label=exercise_question
)

if client_query != "":
    result_df = con.execute(client_query).df()
    st.write("Result")
    st.write(result_df)
    check_answer(result_df, EXECTED_DF)

questionTab, answerTab = st.tabs(["Tables", "Réponse"])

with questionTab:
    exercise_table = exercises.loc[0, 'tables'].tolist()
    for table in exercise_table:
        table_df = con.query(f"SELECT * FROM {table}").df()
        print_df(table, table_df)
    print_df("Expected", EXECTED_DF)

with answerTab:
    st.write(ANSWER_QUERY)
