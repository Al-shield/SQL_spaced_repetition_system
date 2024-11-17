import streamlit as st
from duckdbService import duckdbService
from solution_resolver import check_answer

duckdbService = duckdbService()

def print_df(name, df):
    st.write(name)
    st.write(df)


with st.sidebar:
    currentTheme = st.selectbox(
        "Que souhaitez-vous réviser ?",
        duckdbService.get_themes(),
        placeholder="Sélectionner un thème",
    )
    st.write(f"Thème actuel : {currentTheme}")
    exercises = duckdbService.get_exercises_list_per_theme(currentTheme)
    st.write("Exercices disponibles:")
    for exercise_name in exercises:
        st.write(exercise_name)

    EXPECTED_DF = duckdbService.get_exercise_answer_df(currentTheme, 0)
    exercise_question = duckdbService.get_exercise_question(currentTheme, 0)

st.header("Entrer votre requête")
client_query = st.text_area(label=exercise_question)

if client_query != "":
    result_df = duckdbService.execute_query(client_query)
    st.write("Result")
    st.write(result_df)
    check_answer(result_df, EXPECTED_DF)

questionTab, answerTab = st.tabs(["Tables", "Réponse"])

with questionTab:
    exercise_table = duckdbService.get_exercise_tables(currentTheme, 0)
    for table in exercise_table:
        table_df = duckdbService.execute_query(f"SELECT * FROM {table}")
        print_df(table, table_df)
    print_df("Expected", EXPECTED_DF)

with answerTab:
    st.write(duckdbService.get_exercise_answer_query(currentTheme, 0))
