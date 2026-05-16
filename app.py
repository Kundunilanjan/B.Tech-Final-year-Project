# ====================================================
# Soil Safety Live Dashboard
# ====================================================

# Import Libraries

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# ====================================================
# Load Trained Random Forest Model
# ====================================================

model = joblib.load('soil_safety_rf_model.pkl')

# ====================================================
# Streamlit Page Configuration
# ====================================================

st.set_page_config(
    page_title='Soil Safety Dashboard',
    page_icon='🏗',
    layout='wide'
)

# ====================================================
# Title
# ====================================================

st.title('🏗 Smart Soil Safety Monitoring Dashboard')

st.markdown(
    '### Random Forest Based Construction Safety Prediction System'
)

st.write(
    'This dashboard predicts whether soil is safe for construction using Machine Learning.'
)

# ====================================================
# Sidebar Inputs
# ====================================================

st.sidebar.header('Enter Soil Parameters')

# ====================================================
# Soil Type
# ====================================================

soil_type = st.sidebar.selectbox(
    'Soil Type',
    ['Clay', 'Sand', 'Silt', 'Rock']
)

soil_mapping = {
    'Clay': 0,
    'Sand': 1,
    'Silt': 2,
    'Rock': 3
}

soil_encoded = soil_mapping[soil_type]

# ====================================================
# Soil Moisture
# ====================================================

soil_moisture = st.sidebar.slider(
    'Soil Moisture (%)',
    0.0,
    100.0,
    25.0
)

# ====================================================
# Shear Strength
# ====================================================

shear_strength = st.sidebar.slider(
    'Shear Strength (kPa)',
    0.0,
    300.0,
    150.0
)

# ====================================================
# Bearing Capacity
# ====================================================

bearing_capacity = st.sidebar.slider(
    'Bearing Capacity (kPa)',
    0.0,
    1000.0,
    400.0
)

# ====================================================
# Excavation Depth
# ====================================================

excavation_depth = st.sidebar.slider(
    'Excavation Depth (m)',
    0.0,
    50.0,
    10.0
)

# ====================================================
# Retaining Wall Type
# ====================================================

retaining_wall = st.sidebar.selectbox(
    'Retaining Wall Type',
    ['Concrete', 'Steel', 'Timber']
)

retaining_wall_mapping = {
    'Concrete': 0,
    'Steel': 1,
    'Timber': 2
}

retaining_wall_encoded = retaining_wall_mapping[retaining_wall]

# ====================================================
# Support System
# ====================================================

support_system = st.sidebar.selectbox(
    'Support System',
    ['Anchored', 'Braced', 'Cantilever']
)

support_mapping = {
    'Anchored': 0,
    'Braced': 1,
    'Cantilever': 2
}

support_encoded = support_mapping[support_system]

# ====================================================
# Deformation
# ====================================================

deformation = st.sidebar.slider(
    'Deformation (mm)',
    0.0,
    100.0,
    10.0
)

# ====================================================
# Rainfall
# ====================================================

rainfall = st.sidebar.slider(
    'Rainfall (mm/day)',
    0.0,
    500.0,
    50.0
)

# ====================================================
# Temperature
# ====================================================

temperature = st.sidebar.slider(
    'Temperature (°C)',
    0.0,
    60.0,
    30.0
)

# ====================================================
# Groundwater Level
# ====================================================

groundwater = st.sidebar.slider(
    'Groundwater Level (m)',
    0.0,
    20.0,
    5.0
)

# ====================================================
# Seismic Activity
# ====================================================

seismic = st.sidebar.selectbox(
    'Seismic Activity',
    [0, 1]
)

# ====================================================
# Ground Settlement
# ====================================================

settlement = st.sidebar.slider(
    'Ground Settlement (mm)',
    0.0,
    100.0,
    15.0
)

# ====================================================
# Wall Displacement
# ====================================================

wall_displacement = st.sidebar.slider(
    'Wall Displacement (mm)',
    0.0,
    100.0,
    10.0
)

# ====================================================
# Pore Water Pressure
# ====================================================

pore_pressure = st.sidebar.slider(
    'Pore Water Pressure (kPa)',
    0.0,
    300.0,
    100.0
)

# ====================================================
# Strain Gauge
# ====================================================

strain_gauge = st.sidebar.slider(
    'Strain Gauge',
    0.0,
    100.0,
    40.0
)

# ====================================================
# Create Input DataFrame
# ====================================================

input_data = pd.DataFrame({

    'Soil_Type': [soil_encoded],
    'Soil_Moisture_%': [soil_moisture],
    'Shear_Strength_kPa': [shear_strength],
    'Bearing_Capacity_kPa': [bearing_capacity],
    'Excavation_Depth_m': [excavation_depth],
    'Retaining_Wall_Type': [retaining_wall_encoded],
    'Support_System': [support_encoded],
    'Deformation_mm': [deformation],
    'Rainfall_mm_day': [rainfall],
    'Temperature_C': [temperature],
    'Groundwater_Level_m': [groundwater],
    'Seismic_Activity': [seismic],
    'Ground_Settlement_mm': [settlement],
    'Wall_Displacement_mm': [wall_displacement],
    'Pore_Water_Pressure_kPa': [pore_pressure],
    'Strain_Gauge': [strain_gauge]

})

# ====================================================
# Prediction
# ====================================================

prediction = model.predict(input_data)[0]

# ====================================================
# Risk Labels
# ====================================================

risk_labels = {
    0: '🟢 SAFE CONSTRUCTION ZONE',
    1: '🟡 MEDIUM RISK ZONE',
    2: '🔴 UNSAFE CONSTRUCTION ZONE'
}

# ====================================================
# Prediction Result
# ====================================================

st.subheader('Prediction Result')

if prediction == 0:
    st.success(risk_labels[prediction])

elif prediction == 1:
    st.warning(risk_labels[prediction])

else:
    st.error(risk_labels[prediction])

# ====================================================
# Show Input Data
# ====================================================

st.subheader('Current Soil Parameters')

st.dataframe(input_data)

# ====================================================
# Metrics
# ====================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    'Soil Moisture',
    f'{soil_moisture}%'
)

col2.metric(
    'Bearing Capacity',
    f'{bearing_capacity} kPa'
)

col3.metric(
    'Ground Settlement',
    f'{settlement} mm'
)

# ====================================================
# Visualization
# ====================================================

chart_df = pd.DataFrame({

    'Parameter': [
        'Moisture',
        'Shear Strength',
        'Bearing Capacity',
        'Settlement',
        'Wall Displacement',
        'Pore Pressure'
    ],

    'Value': [
        soil_moisture,
        shear_strength,
        bearing_capacity,
        settlement,
        wall_displacement,
        pore_pressure
    ]

})

fig = px.bar(
    chart_df,
    x='Parameter',
    y='Value',
    title='Live Soil Monitoring Parameters'
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ====================================================
# Safety Recommendation
# ====================================================

st.subheader('Safety Recommendation')

if prediction == 0:

    st.info(
        'Soil conditions appear stable for construction activities.'
    )

elif prediction == 1:

    st.warning(
        'Moderate risk detected. Additional monitoring is recommended.'
    )

else:

    st.error(
        'Unsafe soil conditions detected. Immediate engineering review required.'
    )

# ====================================================
# Footer
# ====================================================

st.markdown('---')

st.write(
    'Developed Using Random Forest + Streamlit + IoT Concepts'
)
