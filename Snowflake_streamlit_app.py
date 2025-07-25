# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col, when_matched


# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruit you want in your custom smoothie!
  """
)

# add order name
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your smoothie order is", name_on_order)



# Get all fruits that could be selected

cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)



# create list to conatin selected fruits
Ingredient_list = st.multiselect(
    "Choose Up to five Ingredients:",
    my_dataframe,
    max_selections=5
)

if Ingredient_list: # if it IS NOT NULL to remove [] when select nothing
    # st.write(Ingredient_list) # TYPE 4 spaces they paste into python without syntax
    # st.text(Ingredient_list)
    
    Ingredient_string=''  
    for fruit_chosen in Ingredient_list:
        Ingredient_string+= fruit_chosen +' '
        # st.write(Ingredient_string)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + Ingredient_string +"""','""" +name_on_order +"""')"""
    st.write(my_insert_stmt )
    # st.stop()- used to test output
    
    # st.write(my_insert_stmt)
    time_to_insert= st.button('Submit Order')


    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order+' !', icon="✅")





