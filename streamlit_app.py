import streamlit as st
from snowflake.snowpark.functions import col

st.title("My Parents' New Healthy Diner")
st.write("Choose fruit for your smoothie!")

# Get Snowflake connection
cnx = st.connection("Snowflake")
session = cnx.session()

# Get name for the order
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)

# Load fruit options
fruit_df = session.table("smoothies.public.fruit_options").select(col("Fruit_Name"))
fruit_list = [row["Fruit_Name"] for row in fruit_df.collect()]

# Fruit selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    fruit_list,
    max_selections=5
)

# Process order
if ingredients_list:
    ingredients_string = " ".join(ingredients_list)

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.Orders(ingredients, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    submitted = st.button("Submit")

    if submitted:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")
