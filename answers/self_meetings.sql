SELECT * FROM df_customers
LEFT JOIN df_stores
USING (customer_id)