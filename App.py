import duckdb
import pandas as pd
import streamlit as st

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
answer_query = """
    SELECT * FROM df_customers
    LEFT JOIN df_stores
    USING (customer_id)
"""


def print_df(name, df):
    st.write(name)
    st.write(df)


with st.sidebar:
    currentTheme = st.selectbox(
        "Que souhaitez-vous réviser ?",
        ["SQL", "Spark", "Scala"],
        placeholder="Sélectionner un thème",
    )
    st.write(f"Thème actuel : {currentTheme}")

st.header("Entrer votre requête")
client_query = st.text_area(
    label="Récupérer tous les clients avec leurs magasin s'il en ont un"
)
result_df = duckdb.sql(client_query)

if client_query != "":
    st.write("Result")
    st.write(result_df.df())

questionTab, answerTab = st.tabs(["Tables", "Réponse"])

with questionTab:
    print_df("df_customers", df_customers)
    print_df("df_stores", df_stores)
    print_df("df_store_products", df_store_products)
    print_df("df_products", df_products)
    print_df("Expected", duckdb.query(answer_query).df())

with answerTab:
    st.write(answer_query)
