import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(page_title="MoonSight", page_icon="🌕", layout="wide")
st.title("🌕 MoonSight")
st.subheader("Lunar Landing Site Navigator")
st.write("Explore real lunar south-pole terrain measurements from NASA's Lunar Orbiter Laser Altimeter (LOLA).")
st.warning("Educational research prototype only. These data are not a landing-safety certification and must not be used for real mission planning.")

NASA_DATA_BASE = "https://core2.gsfc.nasa.gov/PGDA/LOLA_5mpp"
SITES = {
    "Connecting ridge (Site 01)": "Site01",
    "Shackleton rim (Site 04)": "Site04",
    "Peak near Shackleton (Site 07)": "Site07",
    "de Gerlache rim (Site 11)": "Site11",
    "Leibnitz beta plateau (Site 20)": "Site20",
    "Malapert massif (Site 23)": "Site23",
}

@st.cache_data(show_spinner=False, ttl=86400)
def load_lola_raster(site_code: str, product: str):
    import rasterio
    from rasterio.io import MemoryFile

    if product == "Elevation":
        filename = f"{site_code}_final_adj_5mpp_surf.tif"
    else:
        filename = f"{site_code}_final_adj_5mpp_slp.tif"
    url = f"{NASA_DATA_BASE}/{site_code}/{filename}"
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with MemoryFile(response.content) as memfile:
        with memfile.open() as dataset:
            out_height = min(dataset.height, 220)
            out_width = min(dataset.width, 220)
            values = dataset.read(1, out_shape=(out_height, out_width)).astype("float64")
            nodata = dataset.nodata
            crs = str(dataset.crs) if dataset.crs else "Not supplied"
            width, height = dataset.width, dataset.height

    if nodata is not None:
        values[values == nodata] = float("nan")
    values[~pd.notna(values)] = float("nan")
    valid = values[~pd.isna(values)]
    if valid.size == 0:
        raise ValueError("The selected raster contains no valid pixels.")

    series = pd.Series(valid)
    return {
        "array": values,
        "minimum": float(series.min()),
        "maximum": float(series.max()),
        "mean": float(series.mean()),
        "median": float(series.median()),
        "p90": float(series.quantile(0.90)),
        "valid_pixels": int(valid.size),
        "original_width": width,
        "original_height": height,
        "crs": crs,
        "url": url,
    }

with st.sidebar:
    st.header("NASA LOLA dataset")
    selected_site = st.selectbox("South-pole study area", list(SITES))
    product = st.radio("Terrain measurement", ["Elevation", "Slope"])
    st.caption("Source resolution: 5 metres per pixel.")
    load_button = st.button("Load NASA measurements", type="primary", use_container_width=True)
    st.divider()
    st.markdown("[Open NASA Moon Trek](https://trek.nasa.gov/moon/)")
    st.markdown("[Open NASA LOLA dataset archive](https://core2.gsfc.nasa.gov/PGDA/LOLA_5mpp/)")

site_code = SITES[selected_site]
st.info(f"Selected study area: **{selected_site}**. Press **Load NASA measurements** to retrieve the real GeoTIFF from NASA.")

if load_button:
    try:
        with st.spinner("Retrieving NASA LOLA GeoTIFF and processing terrain pixels..."):
            result = load_lola_raster(site_code, product)
        st.session_state["lola_result"] = result
        st.session_state["lola_site"] = selected_site
        st.session_state["lola_product"] = product
    except Exception as exc:
        st.error("NASA data could not be loaded. Check your internet connection and try again; the archive may also be temporarily unavailable.")
        st.caption(f"Technical detail: {type(exc).__name__}: {exc}")

overview, explorer, comparison, science = st.tabs(["Overview", "Terrain Explorer", "Compare Sites", "Science & Sources"])

with overview:
    st.header("What the NASA data tells us")
    st.markdown("""
MoonSight retrieves real LOLA terrain GeoTIFFs from NASA's South Pole landing-site archive.
Select **Elevation** to inspect surface height, or **Slope** to inspect terrain steepness.

A lower slope can be one useful terrain-screening factor, but it does not prove that a site is safe.
Rocks, craters, illumination, communications, thermal conditions and spacecraft constraints also matter.
""")
    if "lola_result" in st.session_state:
        r = st.session_state["lola_result"]
        if st.session_state.get("lola_site") == selected_site and st.session_state.get("lola_product") == product:
            unit = "m" if product == "Elevation" else "degrees"
            a, b, c, d = st.columns(4)
            a.metric(f"Mean {product.lower()}", f"{r['mean']:.2f} {unit}")
            b.metric(f"Median {product.lower()}", f"{r['median']:.2f} {unit}")
            c.metric("90th percentile", f"{r['p90']:.2f} {unit}")
            d.metric("Valid sampled pixels", f"{r['valid_pixels']:,}")
            st.caption(f"Original raster: {r['original_width']:,} × {r['original_height']:,} pixels. The visualization and summary statistics use a downsampled raster for this prototype.")
        else:
            st.info("Load the currently selected site and measurement to display its results.")
    else:
        st.info("No NASA raster loaded yet. Choose a study area and press the load button.")

with explorer:
    st.header("NASA LOLA terrain explorer")
    if "lola_result" in st.session_state:
        r = st.session_state["lola_result"]
        if st.session_state.get("lola_site") == selected_site and st.session_state.get("lola_product") == product:
            unit = "metres" if product == "Elevation" else "degrees"
            fig = go.Figure(data=go.Heatmap(z=r["array"], colorbar={"title": unit}, hoverongaps=False))
            fig.update_layout(
                title=f"{selected_site} — NASA LOLA {product}",
                xaxis_title="Raster sample column (not longitude)",
                yaxis_title="Raster sample row (not latitude)",
                height=600,
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("This is a raster-value view, not a georeferenced latitude/longitude map. The source GeoTIFF uses a lunar south-polar stereographic coordinate system.")
            st.write(f"Source file: [{site_code} {product} GeoTIFF]({r['url']})")
            st.write(f"Source coordinate reference: {r['crs']}")
        else:
            st.info("Load the selected site and measurement to view its raster.")
    else:
        st.info("Load NASA measurements to display the terrain raster.")

with comparison:
    st.header("Compare NASA study areas")
    st.write("Select a study area in the sidebar and load its elevation or slope raster. Record the displayed statistics for each site to compare them. Automated multi-site comparison can be added after verifying each raster's coverage and metadata.")
    st.dataframe(pd.DataFrame([
        {"NASA study area": name, "Archive ID": code, "Available products": "Elevation + slope"}
        for name, code in SITES.items()
    ]), use_container_width=True, hide_index=True)

with science:
    st.header("Scientific method and data provenance")
    st.markdown("""
**Primary dataset — NASA LOLA South Pole Landing Site DEMs**

- Instrument: Lunar Orbiter Laser Altimeter (LOLA), aboard NASA's Lunar Reconnaissance Orbiter.
- Products: surface-interpolated elevation maps and slope maps.
- Published raster resolution: 5 metres per pixel.
- Coordinate reference: south-polar stereographic, Moon_ME frame, DE421.
- Study areas: Connecting ridge, Shackleton rim, Peak near Shackleton, de Gerlache rim, Leibnitz beta plateau and Malapert massif.

**How MoonSight uses it**

1. Downloads the selected elevation or slope GeoTIFF directly from NASA's archive.
2. Reads the raster and handles its no-data value.
3. Calculates descriptive statistics from a downsampled raster.
4. Displays the raster as a heatmap for visual exploration.

**Limitations**

- Heatmaps are shown in raster pixel coordinates, not latitude/longitude.
- The prototype does not calculate a certified landing score.
- Elevation and slope alone cannot establish landing safety.
- NASA data availability depends on an internet connection.
""")
    st.markdown("[NASA LOLA South Pole Landing Site DEM archive](https://core2.gsfc.nasa.gov/PGDA/LOLA_5mpp/)")
    st.markdown("[NASA LRO instrument and data overview](https://science.nasa.gov/mission/lro/data-products/)")
    st.markdown("[NASA Moon Trek](https://trek.nasa.gov/moon/)")
    st.markdown("[NASA Planetary Data System — LRO archive](https://pds-geosciences.wustl.edu/missions/lro/)")
    st.error("MoonSight is an educational prototype, not a certified lunar navigation, landing-site selection, or mission decision-support system.")

st.divider()
st.caption("MoonSight | NASA LOLA data integration | Explore. Analyze. Discover.")
