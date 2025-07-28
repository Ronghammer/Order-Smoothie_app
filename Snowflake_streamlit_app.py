# Import python packages
import streamlit as st
import requests
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

api_key= 'f1Xn1Y6ZtyPVNZuP8pE6pGrAyh0ypPfOM5M2wlD8'
if Ingredient_list: # if it IS NOT NULL to remove [] when select nothing
    # st.write(Ingredient_list) # TYPE 4 spaces they paste into python without syntax
    # st.text(Ingredient_list)
    
    Ingredient_string=''  
    for fruit_chosen in Ingredient_list:
        Ingredient_string+= fruit_chosen +' '
        # st.write(Ingredient_string)
        st.subheader(f"{fruit_chosen.title()} Nutrition Information")
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={fruit_chosen}&api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
        data = response.json()
        # Extract basic info from the first food item
        if "foods" in data and len(data["foods"]) > 0:
            food_item = data["foods"][0]
            nutrients = {
                "Description": food_item.get("description", ""),
                "Calories": food_item.get("foodNutrients", [{}])[0].get("value", "N/A"),
                "Serving Size": food_item.get("servingSize", "N/A"),
                "Brand": food_item.get("brandName", "N/A")
            }
            st.dataframe([nutrients])
        else:
            st.warning(f"No data found for {fruit_chosen}")
    else:
        st.error(f"Failed to fetch data for {fruit_chosen}")

  
       #  smoothiefroot_response = requests.get("https://fdc.nal.usda.gov/food-search?query=" + fruit_chosen)
       #  sf_df= st.dataframe( data= smoothiefroot_response.json(), use_container_width= True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + Ingredient_string +"""','""" +name_on_order +"""')"""
    st.write(my_insert_stmt )
    # st.stop()- used to test output
    
    # st.write(my_insert_stmt)
    time_to_insert= st.button('Submit Order')


    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order+' !', icon="✅")
      



# st.text(smoothiefroot_response).json()






