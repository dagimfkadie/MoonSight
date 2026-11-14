# MoonSight application architecture

## Purpose

MoonSight is an independent educational prototype for exploring lunar south-pole study regions relevant to the NASA Space Apps Challenge: Lunar Landing Site Navigator.

It brings together two complementary kinds of evidence:

1. Terrain measurements from NASA's Lunar Orbiter Laser Altimeter (LOLA) archive.
2. Date-specific apparent Sun and Earth directions from the NASA/JPL Horizons API.

The application is for exploration and learning. It does not certify a landing site or support real spacecraft operations.

## Technology

- Python: application logic and data processing
- Streamlit: interactive web interface
- Rasterio: reading and resampling NASA GeoTIFF rasters
- NumPy and Pandas: numerical operations and tabular summaries
- Plotly: interactive scientific plots
- Requests: NASA archive and JPL Horizons HTTP requests

## Data flow

### Terrain workflow

1. A user chooses a named NASA south-polar study region and a LOLA product.
2. MoonSight constructs the corresponding NASA archive URL.
3. The app downloads the GeoTIFF into a temporary file.
4. Rasterio reads the raster and downsamples it for browser display.
5. MoonSight displays the map and descriptive statistics for the valid preview pixels.
6. The user can export the displayed preview grid as CSV.

Terrain products currently supported:

| Product | Meaning | Unit |
|---|---|---|
| surf | Surface-interpolated elevation | metres |
| slp | Terrain slope | degrees |
| toterr | Total elevation uncertainty (RMS) | metres |
| slperr | Slope uncertainty (RMS) | degrees RMS |
| ldec | LOLA return count | returns per pixel |

### Sun and Earth geometry workflow

1. A user selects a published lunar study-region center or enters lunar coordinates.
2. The user selects a date.
3. MoonSight requests observer ephemerides from the JPL Horizons API for the Sun and Earth.
4. The app displays the returned apparent azimuth and elevation over the selected UT day.
5. The geometric horizon is shown as a reference.

The plotted body-center elevation is not a terrain-aware visibility calculation. Nearby ridges and crater rims may obstruct a body that is geometrically above the reference plane.

## Main application structure

- `app.py`: Streamlit interface, data retrieval, raster processing, plots, and comparison workflows
- `requirements.txt`: Python runtime dependencies
- `NASA_DATA_CITATION.md`: data provenance and attribution
- `DEMO_SCRIPT.md`: suggested project demonstration
- `docs/ARCHITECTURE.md`: this architecture overview

## Caching and temporary data

- NASA terrain downloads are cached by Streamlit for 24 hours.
- Horizons responses are cached for one hour.
- GeoTIFFs are processed from temporary files rather than being committed to the repository.
- Large source rasters should remain in NASA's archive; do not commit them to Git.

## Scientific interpretation and limitations

- Archive-tile statistics are not statistics for a defined landing ellipse.
- Displayed terrain arrays are downsampled previews, not full-resolution analyses.
- The NASA products include uncertainty and return-count layers; these should be considered alongside elevation and slope.
- The Horizons plot uses apparent body-center directions relative to a geometric reference plane.
- The current geometry workflow does not model local terrain obstruction, antenna performance, communication link budgets, or spacecraft-specific constraints.
- The solar-incidence proxy is not a measured or engineering-grade power-generation estimate.

MoonSight is an independent educational project, not a NASA product or endorsement. It must not be used for real mission planning or landing-safety decisions.

## Future engineering work

1. Add automated tests for URL construction, coordinate handling, and data-processing helpers.
2. Add clearer handling for unavailable or malformed NASA/JPL responses.
3. Add terrain-aware horizon analysis using appropriately validated elevation data.
4. Improve reproducibility by recording source URLs, retrieval dates, and analysis settings in exports.
5. Add screenshots and a deployment guide after the live application has been tested.
