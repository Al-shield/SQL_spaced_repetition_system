import streamlit as st
from pandas import DataFrame


def check_answer(answer: DataFrame, solution: DataFrame):
    sameLen = True
    sameCol = True

    # check cols
    if len(answer.columns) != len(solution.columns):
        st.write("Les colonnes sélectionnées ne sont pas les bonnes.")
        sameCol = False

    # check len
    if len(answer) != len(solution):
        st.write("Le nombre de ligne est incorrect.")
        sameLen = False

    # check content
    if sameCol and sameLen:
        diff_df = answer.compare(solution)
        if len(diff_df) != 0:
            st.write(answer.compare(solution))
        else:
            st.write("Félicitation c'est correct !")
