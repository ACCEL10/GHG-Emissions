import streamlit as st
import pandas as pd

# Title and Description
st.title("Scope 1 GHG Emissions Calculator")
st.write("""
Scope 1 GHG emissions are direct emissions from owned or controlled sources.  
This calculator allows you to input fuel consumption and emission data for the following subcategories:
- Fugitive Emissions  
- Stationary Combustion (given in litres)
        - The values for 'Natural gas' and 'Natural gas' are in units of cubic metres
- Mobile Combustion  
- Process Emissions  
You can use default emission factors or provide your own.
""")

# Emission Factors (kg CO₂e per unit of fuel)
default_emission_factors = {
    "Anthracite Coal": 37,
    "Bituminous Coal": 38,
    "Lignite Coal": 38,
    "Mixed (Commercial Sector)": 37,
    "Mixed (Electric Power Sector)": 73,
    "Diesel (liters)": 2.68,
    "Gasoline (liters)": 2.31,
    "Natural Gas (m³)": 1.94,
    "LPG (kg)": 2.98,
    "Coal (kg)": 2.86,
    "Refrigerants (kg)": 1430.0  # Example factor for R134a (Fugitive Emissions)
}

# Dictionary of fuel types for each subcategory
subcategory_fuel_dict = {
    "Fugitive Emissions": ["Refrigerants (kg)"],
    "Stationary Combustion": {
    "Aviation spirit": 2.33116,
    "Aviation turbine fuel": 2.54269,
    "Burning oil": 2.54015,
    "Butane": 1.74532,
    "CNG": 0.44942,
    "Coal (domestic)": 0.36549,
    "Coal (electricity generation)": 0.33368,
    "Coal (electricity generation - home produced coal only)": 0.33368,
    "Coal (industrial)": 0.34002,
    "Coking coal": 0.37675,
    "Diesel (100% mineral diesel)":2.66155,
    "Diesel (average biofuel blend)": 2.51279,
    "Gas oil": 2.75541,
    "LNG": 1.17216,
    "LPG": 1.55713,
    "Lubricants": 2.74934,
    "Marine fuel oil":3.10202,
    "Marine gas oil": 2.77139,
    "Naphtha":2.11894,
    "Natural gas": 2.04542,
    "Natural gas (100% mineral blend)": 2.06318,
    "Other petroleum gas": 0.94441,
    "Petroleum coke":0.35886 ,
    "Petrol (100% mineral petrol)": 2.35372,
    "Petrol (average biofuel blend)": 2.08440,
    "Processed fuel oils - distillate oil": 2.75541,
    "Processed fuel oils - residual oil": 3.17493,
    "Propane":1.54357,
    "Waste oils": 2.74923
    },
    "Mobile Combustion": ["Diesel (liters)", "Gasoline (liters)"],
    "Process Emissions": []  # Add specific fuels if applicable
}

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
    subcategory = st.selectbox("Subcategory", list(subcategory_fuel_dict.keys()))

    # Dynamically update the fuel type dropdown based on selected subcategory
    if subcategory == "Stationary Combustion":
        available_fuels = list(subcategory_fuel_dict[subcategory].keys())
    else:
        available_fuels = subcategory_fuel_dict[subcategory]

    if available_fuels:
        fuel_type = st.selectbox("Fuel Type", options=available_fuels)
        if subcategory == "Stationary Combustion":
            emission_factor = subcategory_fuel_dict[subcategory][fuel_type]
        else:
            emission_factor = default_emission_factors.get(fuel_type, 0.0)
    else:
        st.warning("No fuel types available for the selected subcategory.")
        fuel_type = None
        emission_factor = 0.0

    fuel_consumed = st.number_input("Fuel Consumed (in units)", min_value=0.0, step=0.01)
    use_default_factor = st.checkbox("Use Default Emission Factor", value=True)

    if not use_default_factor:
        emission_factor = st.number_input("Custom Emission Factor (kg CO₂e per unit)", min_value=0.0, step=0.01)

    if st.button("Add Entry"):
        if fuel_type:
            st.session_state.entries.append({
                "Subcategory": subcategory,
                "Fuel Type": fuel_type,
                "Fuel Consumed": fuel_consumed,
                "Emission Factor": emission_factor
            })
            st.success("Entry added successfully!")
        else:
            st.error("Please select a valid fuel type.")

# Display current entries
if st.session_state.entries:
    st.write("### Current Fuel Data")
    fuel_data = pd.DataFrame(st.session_state.entries)
    fuel_data = calculate_emissions(fuel_data)

    # Set the index to start from 1
    fuel_data.index = fuel_data.index + 1

    # Display the updated DataFrame
    st.dataframe(fuel_data)

    # Button to clear the table
    if st.button("Clear All Entries"):
        st.session_state.entries = []  # Reset the entries list
        st.success("All entries have been cleared!")

    # Total emissions by subcategory
    st.write("### Total Emissions by Subcategory")
    total_emissions = fuel_data.groupby("Subcategory")["Emissions (kg CO₂e)"].sum()

    # Total emissions
    total_emissions_all = fuel_data["Emissions (kg CO₂e)"].sum()
    st.success(f"### Total Scope 1 Emissions: {total_emissions_all:.2f} kg CO₂e")
