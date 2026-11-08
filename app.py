import math
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="MoonSight", page_icon="🌕", layout="wide")
st.title("🌕 MoonSight")
st.subheader("Lunar Landing Site Navigator")
st.write("Explore lunar locations, compare lighting scenarios, and investigate environmental conditions.")
st.warning("Educational prototype only. Demo values are illustrative and are not suitable for real mission planning.")

# Illustrative coordinates, not verified landing candidates.
SITES = {
    "South Pole Alpha": (-80.0, 20.0),
    "South Pole Beta": (-75.0, 35.0),
    "Near Side Gamma": (10.0, 15.0),
    "Equatorial Delta": (0.0, -25.0),
}

def light_factor(elevation):
    return max(0.0, math.sin(math.radians(elevation))) * 100

with st.sidebar:
    st.header("Mission Scenario")
    location = st.selectbox("Choose a location", list(SITES))
    scenario_date = st.date_input("Scenario date", value=date.today())
    sun_angle = st.slider("Assumed Sun elevation", 0, 90, 15)
    earth_visible = st.checkbox("Assume Earth is visible", value=True)

latitude, longitude = SITES[location]
light = light_factor(sun_angle)

a, b, c, d = st.columns(4)
a.metric("Latitude", f"{latitude:.1f}°")
b.metric("Longitude", f"{longitude:.1f}°")
c.metric("Idealized light factor", f"{light:.1f}%")
d.metric("Earth visibility", "Assumed yes" if earth_visible else "Assumed no")

overview, explorer, comparison, science = st.tabs(
    ["Overview", "Lunar Explorer", "Compare Scenarios", "Science & Data"]
)

with overview:
    st.header("Selected Lunar Location")
    st.write(f"**Location:** {location}")
    st.write(f"**Scenario date:** {scenario_date}")
    st.write("Earth visibility:", "Assumed visible" if earth_visible else "Assumed not visible")

    chart = pd.DataFrame({
        "Factor": ["Idealized direct-light factor"],
        "Value": [light]
    })
    fig = px.bar(
        chart, x="Factor", y="Value",
        range_y=[0, 100],
        title="Idealized flat-surface light factor"
    )
    st.plotly_chart(fig, use_container_width=True)

with explorer:
    st.header("Lunar Coordinate Explorer")
    st.caption("Illustrative coordinates only; these are not verified landing sites.")

    df = pd.DataFrame([
        {"Location": name, "Latitude": coords[0], "Longitude": coords[1]}
        for name, coords in SITES.items()
    ])

    fig = px.scatter(
        df,
        x="Longitude",
        y="Latitude",
        text="Location",
        hover_name="Location",
        range_x=[-180, 180],
        range_y=[-90, 90],
        title="Illustrative Lunar Coordinates"
    )
    fig.update_traces(marker_size=14)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)

with comparison:
    st.header("Compare Two Scenarios")
    left, right = st.columns(2)

    with left:
        st.subheader("Scenario A")
        angle_a = st.slider("Sun elevation A", 0, 90, 10)
        earth_a = st.checkbox("Earth visible in A (assumption)", value=True)

    with right:
        st.subheader("Scenario B")
        angle_b = st.slider("Sun elevation B", 0, 90, 35)
        earth_b = st.checkbox("Earth visible in B (assumption)", value=False)

    results = pd.DataFrame({
        "Scenario": ["A", "B"],
        "Sun elevation": [angle_a, angle_b],
        "Light factor (%)": [light_factor(angle_a), light_factor(angle_b)],
        "Earth visibility (assumed)": [earth_a, earth_b]
    })

    st.dataframe(results, use_container_width=True, hide_index=True)
    st.metric(
        "Light-factor difference (B − A)",
        f"{light_factor(angle_b) - light_factor(angle_a):+.1f} percentage points"
    )

with science:
    st.header("Scientific Methodology")
    st.markdown("""
### Current prototype
- Coordinates are illustrative demo values.
- Illumination uses a simplified flat-surface model.
- Earth visibility is manually selected.
- The selected date is not yet used for astronomical calculations.

### Planned NASA data integration
- Lunar elevation and terrain datasets
- Lunar imagery and surface geology
- Solar illumination information
- Documented lunar coordinate datasets
""")
    st.markdown("[NASA Planetary Data System](https://pds.nasa.gov/)")
    st.markdown("[NASA Open Data Portal](https://data.nasa.gov/)")
    st.markdown("[NASA Scientific Visualization Studio](https://svs.gsfc.nasa.gov/)")
    st.error("This prototype is not a certified lunar navigation or landing decision-support system.")

st.divider()
st.caption("MoonSight | Explore. Analyze. Discover.")
