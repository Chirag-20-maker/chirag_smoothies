import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title(f"My Parents new healthy Diner!")
st.write(
  """Choose Fruit in your Smoothie!.
  """)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on Smoothie will be", name_on_order)


ingredients_list = st.multiselect(
    "Choose upto 5 ingredients",
     my_dataframe, 
    max_selections = 5
)

if ingredients_list:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    my_insert_stmt = """ Insert into SMOOTHIES.PUBLIC.Orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)

    submitted = st.button('submit')

    if submitted:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered'  +  name_on_order ,icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())    
sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    
