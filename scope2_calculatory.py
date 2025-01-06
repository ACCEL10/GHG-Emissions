#scope2
import streamlit as st

# Define a function to calculate Scope 1 GHG emissions
def calculate_scope1_emissions(activity_data, emission_factors):
    total_emissions = 0
    breakdown = {}

    for source, activity in activity_data.items():
        if source in emission_factors:
            emissions = activity * emission_factors[source]
            breakdown[source] = emissions
            total_emissions += emissions
        else:
            breakdown[source] = "Emission factor not found"
    
    return total_emissions, breakdown

# Streamlit app
st.title("Scope 2 GHG Calculator")

# Sidebar for inputs
st.sidebar.header("Activity Data")
st.sidebar.write("Enter your activity data (e.g., fuel usage).")

# Example emission factors (can be expanded or updated)
emission_factors = {
    "Diesel": 2.68,         # kg CO2e per liter
    "Natural Gas": 2.01,    # kg CO2e per cubic meter
    "Refrigerant R134a": 1430  # kg CO2e per kilogram
}

# Get input for activity data
activity_data = {}
for source in emission_factors.keys():
    activity_data[source] = st.sidebar.number_input(
        f"{source} Usage ({'liters' if source == 'Diesel' else 'cubic meters' if source == 'Natural Gas' else 'kg'})",
        min_value=0.0, step=1.0, format="%.2f"
    )

# Calculate emissions when user clicks the button
if st.sidebar.button("Calculate"):
    total_emissions, breakdown = calculate_scope1_emissions(activity_data, emission_factors)
    
    # Display results
    st.header("Results")
    st.write(f"### Total Scope 1 Emissions: **{total_emissions:.2f} kg CO2e**")
    st.write("#### Breakdown by Source:")
    for source, emissions in breakdown.items():
        st.write(f"- {source}: **{emissions}** kg CO2e")

    # Bar chart visualization
    st.write("#### Emissions Breakdown Chart:")
    chart_data = {source: emissions for source, emissions in breakdown.items() if isinstance(emissions, (int, float))}
    if chart_data:
        st.bar_chart(chart_data)
    else:
        st.write("No valid data to display in chart.")

