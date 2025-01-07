# #scope 1
# import mysql.connector
# import streamlit as st

# # Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="your_username",
#     password="your_password",
#     database="your_database"
# )
# cursor = conn.cursor()

# # Streamlit inputs
# st.title("Scope 1 GHG Emissions Calculator")
# fuel_type = st.selectbox("Select Fuel Type", ["Diesel", "Gasoline", "Natural Gas", "LPG", "Coal"])
# fuel_consumed = st.number_input("Fuel Consumed", min_value=0.0, step=0.1)
# emission_factor = st.number_input("Emission Factor (kg CO₂e per unit)", min_value=0.0, step=0.01)

# if st.button("Add Entry"):
#     cursor.execute(
#         "INSERT INTO scope1_emissions (fuel_type, fuel_consumed, emission_factor) VALUES (%s, %s, %s)",
#         (fuel_type, fuel_consumed, emission_factor)
#     )
#     conn.commit()
#     st.success("Entry added to the database!")

# # Fetch and display the data
# if st.button("Show Data"):
#     cursor.execute("SELECT * FROM scope1_emissions")
#     rows = cursor.fetchall()
#     st.write("### Emissions Data")
#     for row in rows:
#         st.write(row)

# # Close the connection
# conn.close()



import streamlit as st
import pandas as pd

# Title and Description
st.title("Scope 1 GHG Emissions Calculator")
st.write("""
Scope 1 GHG emissions are direct emissions from owned or controlled sources.  
This calculator allows you to input fuel consumption and emission data for the following subcategories:
- Fugitive Emissions  
- Stationary Combustion  
- Mobile Combustion  
- Process Emissions  
You can use default emission factors or provide your own.
""")

# Emission Factors (kg CO₂e per unit of fuel)
default_emission_factors = {
    "Anthracite Coal": 37,
    "Bituminous Coal":38,
    "Lignite Coal":38,
    "Mixed (Commercial Sector)":37,
    "Mixed (Electric Power Sector)":73,
    "Diesel (liters)": 2.68,
    "Gasoline (liters)": 2.31,
    "Natural Gas (m³)": 1.94,
    "LPG (kg)": 2.98,
    "Coal (kg)": 2.86,
    "Refrigerants (kg)": 1430.0  # Example factor for R134a (Fugitive Emissions)
}

# Subcategories
subcategories = ["Fugitive Emissions", "Stationary Combustion", "Mobile Combustion", "Process Emissions"]

# Initialize session state for inputs
if "entries" not in st.session_state:
    st.session_state.entries = []

# Function to calculate emissions
def calculate_emissions(df):
    df["Emissions (kg CO₂e)"] = df["Fuel Consumed"] * df["Emission Factor"]
    return df

# Add a new entry
st.write("### Add Fuel Consumption Data")

with st.expander("Add a New Entry"):
    subcategory = st.selectbox("Subcategory", subcategories)
    fuel_type = st.selectbox("Fuel Type", options=list(default_emission_factors.keys()))
    fuel_consumed = st.number_input("Fuel Consumed (in units)", min_value=0.0, step=0.01)
    use_default_factor = st.checkbox("Use Default Emission Factor", value=True)

    if use_default_factor:
        emission_factor = default_emission_factors.get(fuel_type, 0.0)
    else:
        emission_factor = st.number_input("Custom Emission Factor (kg CO₂e per unit)", min_value=0.0, step=0.01)

    if st.button("Add Entry"):
        st.session_state.entries.append({
            "Subcategory": subcategory,
            "Fuel Type": fuel_type,
            "Fuel Consumed": fuel_consumed,
            "Emission Factor": emission_factor
        })
        st.success("Entry added successfully!")

# Display current entries
if st.session_state.entries:
    st.write("### Current Fuel Data")
    fuel_data = pd.DataFrame(st.session_state.entries)
    fuel_data = calculate_emissions(fuel_data)
    
    # Set the index to start from 1
    fuel_data.index = fuel_data.index + 1

    # Display the updated DataFrame
    st.dataframe(fuel_data)

    # Total emissions by subcategory
    st.write("### Total Emissions by Subcategory")
    total_emissions = fuel_data.groupby("Subcategory")["Emissions (kg CO₂e)"].sum()

    # Total emissions
    total_emissions_all = fuel_data["Emissions (kg CO₂e)"].sum()
    st.success(f"### Total Scope 1 Emissions: {total_emissions_all:.2f} kg CO₂e")

