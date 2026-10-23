"""Streamlit dashboard for educational CubeSat electrical power studies."""

import io
import pandas as pd
import streamlit as st

from src.power_budget import calculate_total_power, calculate_total_energy
from src.solar_power import calculate_solar_power, calculate_solar_energy
from src.battery_model import calculate_final_soc

st.set_page_config(page_title="CubeSat Power Systems", page_icon="🛰️", layout="wide")
st.title("🛰️ CubeSat Power Systems")
st.caption("Interactive educational dashboard · All inputs are illustrative assumptions")

with st.sidebar:
    st.header("Analysis settings")
    period_hours = st.number_input("Analysis period (h)", min_value=0.1, value=24.0, step=1.0)
    st.info("Use consistent units. This simplified tool is not flight software or a mission-validated design tool.")

tab_load, tab_solar, tab_battery, tab_balance = st.tabs(
    ["⚡ Power budget", "☀️ Solar array", "🔋 Battery", "📊 Energy balance"]
)

with tab_load:
    st.subheader("Subsystem loads")
    st.write("Edit the illustrative loads below. Power is treated as the average power while each subsystem is active.")
    defaults = pd.DataFrame([
        {"Subsystem": "On-board computer", "Power (W)": 1.5, "Operating hours": 24.0},
        {"Subsystem": "Communications", "Power (W)": 2.5, "Operating hours": 1.0},
        {"Subsystem": "Payload", "Power (W)": 3.0, "Operating hours": 2.0},
        {"Subsystem": "ADCS", "Power (W)": 1.0, "Operating hours": 6.0},
    ])
    loads = st.data_editor(defaults, num_rows="dynamic", use_container_width=True, key="loads")
    valid_loads = (
        not loads.empty
        and loads["Subsystem"].astype(str).str.strip().ne("").all()
        and (loads["Power (W)"] >= 0).all()
        and (loads["Operating hours"] >= 0).all()
        and (loads["Operating hours"] <= period_hours).all()
    )
    if not valid_loads:
        st.error("Give every subsystem a name and use non-negative values. Operating hours cannot exceed the analysis period.")
        load_energy = 0.0
        total_power = 0.0
    else:
        load_energy = float((loads["Power (W)"] * loads["Operating hours"]).sum())
        total_power = float(calculate_total_power([
            {"power_w": float(row["Power (W)"]), "operating_hours": float(row["Operating hours"])}
            for _, row in loads.iterrows()
        ]))
        c1, c2, c3 = st.columns(3)
        c1.metric("Sum of listed power", f"{total_power:.2f} W")
        c2.metric("Energy consumed", f"{load_energy:.2f} Wh")
        c3.metric("Average load over period", f"{load_energy / period_hours:.2f} W")
        chart = loads[["Subsystem", "Power (W)"]].set_index("Subsystem")
        st.bar_chart(chart)
    st.caption("The sum of rated power assumes simultaneous operation; the energy calculation uses each subsystem's entered operating time.")

with tab_solar:
    st.subheader("Solar-array estimate")
    c1, c2 = st.columns(2)
    with c1:
        area = st.number_input("Active cell area (m²)", min_value=0.0, value=0.02, step=0.005, format="%.4f")
        irradiance = st.number_input("Incident irradiance (W/m²)", min_value=0.0, value=1361.0, step=10.0)
        sunlight_hours = st.number_input("Sunlight duration in period (h)", min_value=0.0, max_value=float(period_hours), value=min(14.0, float(period_hours)), step=0.5)
    with c2:
        efficiency = st.slider("Cell conversion efficiency", 0.0, 1.0, 0.30, 0.01, format="%.2f")
        degradation = st.slider("Power degradation factor", 0.0, 1.0, 0.05, 0.01, format="%.2f")
        other_losses = st.slider("Additional electrical losses", 0.0, 0.8, 0.10, 0.01, format="%.2f")
    solar_power = calculate_solar_power(area, irradiance, efficiency, degradation) * (1 - other_losses)
    solar_energy = calculate_solar_energy(solar_power, sunlight_hours)
    c1, c2 = st.columns(2)
    c1.metric("Estimated array output", f"{solar_power:.3f} W")
    c2.metric("Estimated energy generated", f"{solar_energy:.3f} Wh")
    st.caption("First-order estimate. It does not model incidence angle, orbital geometry, shadowing, temperature, or time-varying illumination.")

with tab_battery:
    st.subheader("Battery state of charge")
    c1, c2 = st.columns(2)
    with c1:
        initial_soc = st.slider("Initial state of charge (%)", 0, 100, 80)
        capacity = st.number_input("Nominal battery capacity (Wh)", min_value=0.1, value=20.0, step=1.0)
    with c2:
        charged = st.number_input("Energy delivered to battery (Wh)", min_value=0.0, value=5.0, step=0.5)
        used = st.number_input("Energy drawn from battery (Wh)", min_value=0.0, value=3.0, step=0.5)
        charge_efficiency = st.slider("Charging efficiency", 0.0, 1.0, 0.90, 0.01)
    final_soc = calculate_final_soc(initial_soc, capacity, charged, used, charge_efficiency)
    c1, c2, c3 = st.columns(3)
    c1.metric("Initial SOC", f"{initial_soc}%")
    c2.metric("Estimated final SOC", f"{final_soc:.1f}%")
    c3.metric("Change in SOC", f"{final_soc - initial_soc:+.1f} percentage points")
    st.caption("Simplified energy bookkeeping; ignores voltage, temperature, battery aging, discharge limits, and battery-management behavior.")

with tab_balance:
    st.subheader("Daily / period energy balance")
    st.write("Combines the current load table with the solar-array estimate. Treat this as a first-order screening calculation.")
    balance_wh = solar_energy - load_energy
    c1, c2, c3 = st.columns(3)
    c1.metric("Solar energy", f"{solar_energy:.2f} Wh")
    c2.metric("Load energy", f"{load_energy:.2f} Wh")
    c3.metric("Net energy", f"{balance_wh:+.2f} Wh", delta="Surplus" if balance_wh >= 0 else "Deficit")
    if balance_wh >= 0:
        st.success(f"Illustrative energy surplus: {balance_wh:.2f} Wh over the selected period.")
    else:
        st.warning(f"Illustrative energy deficit: {abs(balance_wh):.2f} Wh over the selected period. The assumed generation does not cover the entered loads.")
    balance = pd.DataFrame({
        "Category": ["Solar generation", "Subsystem consumption", "Net balance"],
        "Energy (Wh)": [solar_energy, load_energy, balance_wh],
    })
    st.bar_chart(balance.set_index("Category"))
    report = io.StringIO()
    pd.DataFrame({
        "Metric": ["Analysis period (h)", "Sum of listed power (W)", "Load energy (Wh)", "Solar-array power after losses (W)", "Solar energy (Wh)", "Net energy balance (Wh)"],
        "Value": [period_hours, total_power, load_energy, solar_power, solar_energy, balance_wh],
    }).to_csv(report, index=False)
    st.download_button("Download summary CSV", report.getvalue(), "cubesat_power_summary.csv", "text/csv")
    st.caption("This balance does not simulate eclipse timing or the sequence of charging and discharging. A positive net balance alone does not prove that a real spacecraft has adequate power or battery capacity.")

st.divider()
st.caption("Educational prototype · Illustrative values only · Validate assumptions before using results for engineering decisions.")
