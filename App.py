import duckdb
import pandas as pd
import streamlit as st

data = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
df = pd.DataFrame(data)

with st.sidebar:
    currentTheme = st.selectbox(
        "Que souhaitez-vous réviser ?",
        ["SQL", "Spark", "Scala"],
        placeholder="Sélectionner un thème"
    )
    st.write(f"Thème actuel : {currentTheme}")

st.write("df :", df)

client_query = st.text_area(label="Request to apply on this dataframe")
result_df = duckdb.sql(client_query)

if client_query != "":
    st.write("Result")
    st.write(result_df.df())