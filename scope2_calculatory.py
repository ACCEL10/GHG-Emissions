import streamlit as st
import pandas as pd

# Title and description
st.title("Scope 2 GHG Emissions Calculator")
st.markdown("""
            This calculator helps you estimate your organization’s Scope 2 greenhouse gas (GHG) emissions, which result from the electricity, heating, cooling, or steam you consume. These emissions are indirect and occur at the source of energy production, such as power plants.

            To calculate your carbon output, you can either input a custom emission factor or use the default value from the Grid Emission Factor for 2022 as 0.774 from Suruhanjaya Tenagara
""")
st.subheader("How It Works:")
st.markdown(""" 
                1.Enter Your Energy Consumption: Provide the total energy used (in kilowatt-hours, kWh).

                2.Choose an Emission Factor: Use the default value (0.772 kg CO₂e/kWh for 2022) or input a custom emission factor specific to your energy source or region.

                3.View Your Total Emissions: The calculator will estimate the total GHG emissions (in kilograms of CO₂ equivalent, kg CO₂e) associated with your energy use.
""")

# Sidebar for user input
st.sidebar.header("Input Parameters")

# User input for energy sources
energy_sources = st.sidebar.multiselect(
    "Select energy sources used:",
    options=["Electricity", "Steam", "Heat", "Cooling"]
)

# Data dictionary to store inputs for each source
data = {}

for source in energy_sources:
    # Energy consumption input
    consumption = st.sidebar.number_input(
        f"Energy Consumption for {source} (kWh):",
        min_value=0.0, value=0.0, step=0.1
    )

    # Option to select or input emission factor
    emission_factor_option = st.sidebar.radio(
        f"Choose Emission Factor for {source}:",
        options=["0.774", "Input custom"],
        key=source
    )
    if emission_factor_option == "0.774":
        emission_factor = 0.774  # Default value for 2022
    else:
        emission_factor = st.sidebar.number_input(
            f"Enter custom Emission Factor for {source} (kg CO₂-eq/kWh):",
            min_value=0.0, value=0.0, step=0.01
        )

    # Store inputs
    data[source] = {
        "Consumption (kWh)": consumption,
        "Emission Factor (kg CO₂-eq/kWh)": emission_factor
    }

# Function to calculate total emissions
def calculate_total_emissions(data):
    total_emissions = 0.0
    for source, values in data.items():
        consumption = values.get("Consumption (kWh)", 0.0)
        emission_factor = values.get("Emission Factor (kg CO₂-eq/kWh)", 0.0)
        emissions = consumption * emission_factor
        total_emissions += emissions
    return total_emissions

# Calculate and display results
if data:
    # Convert to DataFrame for display
    df = pd.DataFrame(data).T
    df["Emissions (kg CO₂-eq)"] = df["Consumption (kWh)"] * df["Emission Factor (kg CO₂-eq/kWh)"]

    # Display results
    
    st.table(df)
    total_emissions = calculate_total_emissions(data)
    st.write(f"**Total Emissions (kg CO₂-eq): {total_emissions:.2f}**")
else:
    st.write("Please enter data to calculate emissions.")

