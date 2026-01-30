# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)


# option = st.selectbox(
 #   "What is your favorite fruit?",
  #  ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fruit is:", option)
from snowflake.snowpark.functions import col
session = get_active_session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )
if ingredients_list:
  ingredients_string = ''
    
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
  #st.write(ingredients_string)   

  my_insert_stmt = f"""
INSERT INTO SMOOTHIES.PUBLIC.ORDERS
(INGREDIENTS, NAME_ON_ORDER)
VALUES ('{ingredients_string}', '{name_on_order}')
"""



  #st.write(my_insert_stmt)  
  #st.stop()
  time_to_start = st.button('Submit Order')
    
  if time_to_start:
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered! ',icon="✅")

