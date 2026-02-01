my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
     my_dataframe,
     max_selections = 5)

# The phrase:
#  if ingredients_list:
# actually means...
# if ingredients_list is not null: then do everything below this line that is indented. 


if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list: 
    # OR for each_fruit in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+ """')"""
    
    # st.write(my_insert_stmt)
    # st.stop()

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, **{name_on_order}** !", icon="✅")

# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


# import streamlit as st

# user_name = "Alice"
# task_status = "completed successfully"

# # Use an f-string to embed variables
# st.success(f"Task for user **{user_name}** {task_status}!")
