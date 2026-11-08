import tempfile
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(page_title="MoonSight", page_icon="🌕", layout="wide")
st.title("🌕 MoonSight")
st.subheader("NASA lunar south-pole terrain explorer")
st.write("Explore elevation, slope, and measurement uncertainty from NASA's Lunar Orbiter Laser Altimeter (LOLA).")
st.warning("Educational prototype only. Not a landing-safety certification or a tool for real mission planning.")

BASE = "https://pgda.gsfc.nasa.gov/data/LOLA_5mpp"
SITES = {
    "Connecting ridge": "Site01",
    "Shackleton rim": "Site04",
    "Nobile rim 1": "Site06",
    "Peak near Shackleton": "Site07",
    "de Gerlache rim": "Site11",
    "Leibnitz beta plateau": "Site20",
    "Leibnitz beta plateau (extended)": "Site20v2",
    "Malapert massif": "Site23",
    "de Gerlache-Kocher massif": "Site42",
}
PRODUCTS = {
    "Elevation": ("surf", "metres"),
    "Slope": ("slp", "degrees"),
    "Elevation uncertainty": ("toterr", "metres RMS"),
    "Slope uncertainty": ("slperr", "degrees RMS"),
    "LOLA return count": ("ldec", "returns per pixel"),
}

@st.cache_data(ttl=86400, show_spinner=False)
def load_raster(site, product, max_dimension):
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.transform import xy

    suffix, unit = PRODUCTS[product]
    filename = f"{site}_final_adj_5mpp_{suffix}.tif"
    url = f"{BASE}/{site}/{filename}"
    with requests.get(url, stream=True, timeout=(20, 180)) as response:
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(suffix=".tif") as tmp:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    tmp.write(chunk)
            tmp.flush()
            with rasterio.open(tmp.name) as ds:
                scale = min(1.0, max_dimension / max(ds.width, ds.height))
                out_w = max(1, int(ds.width * scale))
                out_h = max(1, int(ds.height * scale))
                arr = ds.read(1, out_shape=(out_h, out_w), resampling=Resampling.average, masked=True)
                arr = np.ma.filled(arr.astype("float64"), np.nan)
                transform = ds.transform * ds.transform.scale(ds.width / out_w, ds.height / out_h)
                xs = [xy(transform, 0, c, offset="center")[0] for c in range(out_w)]
                ys = [xy(transform, r, 0, offset="center")[1] for r in range(out_h)]
                valid = arr[np.isfinite(arr)]
                if valid.size == 0:
                    raise ValueError("No valid data pixels were found.")
                stats = {
                    "mean": float(np.mean(valid)),
                    "median": float(np.median(valid)),
                    "p90": float(np.percentile(valid, 90)),
                    "min": float(np.min(valid)),
                    "max": float(np.max(valid)),
                    "valid": int(valid.size),
                    "source_shape": (int(ds.height), int(ds.width)),
                    "preview_shape": (out_h, out_w),
                    "crs": str(ds.crs),
                    "pixel_size": tuple(float(v) for v in ds.res),
                }
    return {"array": arr, "x": xs, "y": ys, "stats": stats, "url": url, "unit": unit}

def show_map(result, title):
    fig = go.Figure(go.Heatmap(
        z=result["array"], x=result["x"], y=result["y"],
        colorbar={"title": result["unit"]},
        hovertemplate="X: %{x:,.1f} m<br>Y: %{y:,.1f} m<br>Value: %{z:.3f}<extra></extra>",
        connectgaps=False,
    ))
    fig.update_layout(
        title=title, height=560,
        xaxis_title="South-polar stereographic X (m)",
        yaxis_title="South-polar stereographic Y (m)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Coordinates are lunar map-projection X/Y in metres, not latitude/longitude. The displayed grid is downsampled.")

with st.sidebar:
    st.header("NASA LOLA data")
    site_name = st.selectbox("Study area", list(SITES))
    site = SITES[site_name]
    product = st.selectbox("Data product", list(PRODUCTS))
    detail = st.select_slider("Preview resolution", options=[250, 400, 600, 800], value=400)
    load = st.button("Load NASA data", type="primary", use_container_width=True)
    st.caption("Internet required. Loaded rasters are cached for 24 hours.")
    st.markdown("[NASA data product page](https://pgda.gsfc.nasa.gov/products/78)")
    st.markdown("[NASA Moon Trek](https://trek.nasa.gov/moon/)")

if load:
    try:
        with st.spinner("Downloading and processing NASA GeoTIFF..."):
            st.session_state["raster"] = load_raster(site, product, detail)
            st.session_state["raster_key"] = (site, product, detail)
    except requests.RequestException as exc:
        st.error("NASA's server could not complete the download. Check your connection and try again.")
        st.caption(f"{type(exc).__name__}: {exc}")
    except Exception as exc:
        st.error("The raster could not be processed.")
        st.caption(f"{type(exc).__name__}: {exc}")

overview, map_tab, compare, sources = st.tabs(["Overview", "Terrain map", "Compare sites", "Science & sources"])

with overview:
    st.header("What MoonSight measures")
    st.write("The app retrieves real NASA LOLA GeoTIFF files and displays terrain height, slope, uncertainty, and the number of laser returns per pixel.")
    st.dataframe(pd.DataFrame([{"Region": n, "NASA ID": code} for n, code in SITES.items()]), use_container_width=True, hide_index=True)
    if st.session_state.get("raster_key") == (site, product, detail):
        r = st.session_state["raster"]
        s = r["stats"]
        st.subheader("Loaded raster summary")
        a, b, c, d = st.columns(4)
        a.metric("Mean", f"{s['mean']:.3f} {r['unit']}")
        b.metric("Median", f"{s['median']:.3f} {r['unit']}")
        c.metric("90th percentile", f"{s['p90']:.3f} {r['unit']}")
        d.metric("Valid preview pixels", f"{s['valid']:,}")
        st.caption(f"Original raster: {s['source_shape'][1]:,} × {s['source_shape'][0]:,}; preview: {s['preview_shape'][1]:,} × {s['preview_shape'][0]:,}; source pixel size: {s['pixel_size']}.")
    else:
        st.info("Choose a study area and product, then press Load NASA data.")

with map_tab:
    if st.session_state.get("raster_key") == (site, product, detail):
        r = st.session_state["raster"]
        show_map(r, f"{site_name} — {product}")
        st.write(f"NASA source: [{site}_{PRODUCTS[product][0]}.tif]({r['url']})")
        st.write(f"Coordinate reference: {r['stats']['crs']}")
        grid = pd.DataFrame(r["array"], index=r["y"], columns=r["x"])
        grid.index.name = "Y map coordinate (m)"
        grid.columns.name = "X map coordinate (m)"
        st.download_button("Download preview as CSV", grid.to_csv().encode(), f"{site}_{PRODUCTS[product][0]}_preview.csv", "text/csv")
    else:
        st.info("Load the selected NASA raster to see its map.")

with compare:
    st.header("Compare two study areas")
    left, right = st.columns(2)
    with left:
        name_a = st.selectbox("Study area A", list(SITES), index=0)
    with right:
        name_b = st.selectbox("Study area B", list(SITES), index=1)
    compare_product = st.selectbox("Product to compare", list(PRODUCTS), key="compare_product")
    if st.button("Load comparison"):
        try:
            with st.spinner("Retrieving both NASA products..."):
                a = load_raster(SITES[name_a], compare_product, 300)
                b = load_raster(SITES[name_b], compare_product, 300)
            rows = []
            for name, item in [(name_a, a), (name_b, b)]:
                s = item["stats"]
                rows.append({"Study area": name, "Mean": s["mean"], "Median": s["median"], "90th percentile": s["p90"], "Unit": item["unit"]})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
            st.caption("Statistics describe downsampled previews of the full archive tiles, not selected landing ellipses.")
            ca, cb = st.columns(2)
            with ca:
                show_map(a, name_a)
            with cb:
                show_map(b, name_b)
        except Exception as exc:
            st.error("Comparison failed. Check your connection and try again.")
            st.caption(f"{type(exc).__name__}: {exc}")

with sources:
    st.header("NASA data provenance")
    st.markdown("""
**Instrument:** Lunar Orbiter Laser Altimeter (LOLA), aboard NASA's Lunar Reconnaissance Orbiter.

**NASA products used:**
- surf — surface-interpolated elevation (metres)
- slp — terrain slope (degrees)
- toterr — total elevation uncertainty (RMS metres)
- slperr — slope uncertainty (RMS degrees)
- ldec — number of LOLA returns in each pixel

NASA describes these GeoTIFFs as 5 m/pixel, with south-polar stereographic X/Y coordinates in metres, Moon_ME reference frame, DE421 ephemeris.

NASA notes that roughly 90% of pixels in these interpolated polar elevation maps are interpolated. The LOLA return-count and uncertainty layers therefore provide important context for interpreting the maps.

**Scientific reference:** Barker et al. (2021), *Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions*, Planetary and Space Science, 203, 105119. [DOI](https://doi.org/10.1016/j.pss.2020.105119)
""")
    st.markdown("[NASA product page and file links](https://pgda.gsfc.nasa.gov/products/78)")
    st.markdown("[NASA LOLA data archive](https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/)")
    st.markdown("[NASA lunar polar illumination and Earth-visibility maps](https://pgda.gsfc.nasa.gov/products/69)")
    st.markdown("[JPL Horizons API documentation](https://ssd-api.jpl.nasa.gov/doc/horizons.html)")
    st.markdown("[NASA Moon Trek](https://trek.nasa.gov/moon/)")
    st.error("These measurements alone cannot establish landing safety. MoonSight does not calculate a certified landing score and is not a NASA product.")

st.divider()
st.caption("MoonSight | NASA LRO-LOLA terrain data | Explore. Analyze. Discover.")


# Date-specific Sun and Earth geometry from NASA/JPL Horizons.
@st.cache_data(ttl=3600, show_spinner=False)
def get_horizons_altaz(target_id, longitude_east, latitude, selected_date):
    import csv
    from datetime import timedelta
    from io import StringIO

    start = selected_date.isoformat()
    stop = (selected_date + timedelta(days=1)).isoformat()
    params = {
        "format": "json",
        "COMMAND": f"'{target_id}'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'OBSERVER'",
        "OBJ_DATA": "'NO'",
        "CENTER": "'coord@301'",
        "COORD_TYPE": "'GEODETIC'",
        "SITE_COORD": f"'{longitude_east},{latitude},0'",
        "START_TIME": f"'{start}'",
        "STOP_TIME": f"'{stop}'",
        "STEP_SIZE": "'1h'",
        "QUANTITIES": "'4'",
        "CSV_FORMAT": "'YES'",
        "TIME_TYPE": "'UT'",
    }
    response = requests.get(
        "https://ssd.jpl.nasa.gov/api/horizons.api",
        params=params,
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("error"):
        raise ValueError(payload["error"])
    raw = payload.get("result", "")
    if "$$SOE" not in raw or "$$EOE" not in raw:
        raise ValueError("JPL Horizons did not return an ephemeris table: " + raw[:500])

    table = raw.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    records = []
    for row in csv.reader(StringIO(table), skipinitialspace=True):
        if len(row) < 3:
            continue
        try:
            timestamp = pd.to_datetime(row[0].strip().strip('"'), errors="raise")
            azimuth = float(row[-2].strip())
            elevation = float(row[-1].strip())
        except (ValueError, TypeError):
            continue
        records.append({
            "UTC": timestamp,
            "Azimuth (degrees)": azimuth,
            "Elevation (degrees)": elevation,
        })
    if not records:
        raise ValueError("JPL Horizons returned no parseable azimuth/elevation samples.")
    return pd.DataFrame(records)

st.divider()
st.header("☀️ Sun & Earth geometry — JPL Horizons")
st.write(
    "Compare the Sun and Earth above the local geometric horizon at two custom lunar "
    "surface points and dates. Positions are calculated by NASA/JPL Horizons."
)
st.caption(
    "Enter the east longitude and latitude of each candidate point. The default coordinates "
    "are generic demonstration points, not the centers of the named LOLA study areas."
)

with st.expander("Candidate coordinates and dates", expanded=True):
    ca, cb = st.columns(2)
    with ca:
        st.subheader("Scenario A")
        lon_a = st.number_input("A east longitude (°)", min_value=-180.0, max_value=180.0, value=0.0, step=0.1, key="h_lon_a")
        lat_a = st.number_input("A latitude (°)", min_value=-90.0, max_value=90.0, value=-89.5, step=0.1, key="h_lat_a")
        date_a = st.date_input("A date (UT)", key="h_date_a")
    with cb:
        st.subheader("Scenario B")
        lon_b = st.number_input("B east longitude (°)", min_value=-180.0, max_value=180.0, value=90.0, step=0.1, key="h_lon_b")
        lat_b = st.number_input("B latitude (°)", min_value=-90.0, max_value=90.0, value=-89.5, step=0.1, key="h_lat_b")
        date_b = st.date_input("B date (UT)", key="h_date_b")

if st.button("Compare Sun and Earth positions", type="primary", key="run_horizons"):
    try:
        with st.spinner("Requesting Sun and Earth ephemerides from JPL Horizons..."):
            scenarios = []
            for label, lon, lat, chosen_date in [
                ("A", lon_a, lat_a, date_a),
                ("B", lon_b, lat_b, date_b),
            ]:
                sun = get_horizons_altaz(10, lon, lat, chosen_date)
                earth = get_horizons_altaz(399, lon, lat, chosen_date)
                merged = sun.rename(columns={
                    "Azimuth (degrees)": "Sun azimuth (°)",
                    "Elevation (degrees)": "Sun elevation (°)",
                }).merge(
                    earth.rename(columns={
                        "Azimuth (degrees)": "Earth azimuth (°)",
                        "Elevation (degrees)": "Earth elevation (°)",
                    }),
                    on="UTC",
                    how="inner",
                )
                merged["Scenario"] = label
                merged["Sun center above geometric horizon"] = merged["Sun elevation (°)"] > 0
                merged["Earth center above geometric horizon"] = merged["Earth elevation (°)"] > 0
                scenarios.append(merged)
            result = pd.concat(scenarios, ignore_index=True)
            st.session_state["horizons_result"] = result
            st.session_state["horizons_details"] = {
                "A": {"longitude": lon_a, "latitude": lat_a, "date": str(date_a)},
                "B": {"longitude": lon_b, "latitude": lat_b, "date": str(date_b)},
            }
    except Exception as exc:
        st.error("The JPL Horizons comparison could not be completed. Check the connection and try again.")
        st.caption(f"{type(exc).__name__}: {exc}")

if "horizons_result" in st.session_state:
    result = st.session_state["horizons_result"]
    details = st.session_state["horizons_details"]
    st.subheader("Comparison results")
    metric_cols = st.columns(4)
    for idx, label in enumerate(["A", "B"]):
        subset = result[result["Scenario"] == label]
        sun_pct = 100 * subset["Sun above geometric horizon"].mean()
        earth_pct = 100 * subset["Earth above geometric horizon"].mean()
        metric_cols[idx * 2].metric(f"Scenario {label} — Sun above horizon", f"{sun_pct:.1f}%")
        metric_cols[idx * 2 + 1].metric(f"Scenario {label} — Earth above horizon", f"{earth_pct:.1f}%")

    sun_fig = go.Figure()
    earth_fig = go.Figure()
    for label in ["A", "B"]:
        subset = result[result["Scenario"] == label]
        sun_fig.add_trace(go.Scatter(x=subset["UTC"], y=subset["Sun elevation (°)"], mode="lines+markers", name=f"Scenario {label}"))
        earth_fig.add_trace(go.Scatter(x=subset["UTC"], y=subset["Earth elevation (°)"], mode="lines+markers", name=f"Scenario {label}"))
    for fig, title, ytitle in [
        (sun_fig, "Sun elevation over the selected UT day", "Sun elevation (degrees)"),
        (earth_fig, "Earth elevation over the selected UT day", "Earth elevation (degrees)"),
    ]:
        fig.add_hline(y=0, line_dash="dash", annotation_text="Geometric horizon")
        fig.update_layout(title=title, xaxis_title="UT", yaxis_title=ytitle, height=390)
        st.plotly_chart(fig, use_container_width=True)

    st.dataframe(result, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Sun/Earth ephemeris comparison (CSV)",
        result.to_csv(index=False).encode("utf-8"),
        "moonsight_horizons_comparison.csv",
        "text/csv",
    )
    st.caption(
        "Interpretation: positive Sun-center elevation indicates the Sun center is above the local geometric "
        "reference horizon in Horizons; positive Earth-center elevation indicates the Earth center is above "
        "that geometric horizon. This uses the center of each body, not its full apparent disc, and is not a terrain-shadow or radio-link simulation. Local "
        "ridges, crater walls, antenna orientation, link budget, and operational constraints "
        "can still block power or communication."
    )
