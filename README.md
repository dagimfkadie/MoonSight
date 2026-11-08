# 🌕 MoonSight — Lunar South-Pole Terrain Explorer

MoonSight is an independent educational application for visualizing and comparing real lunar south-pole terrain products from NASA's Lunar Reconnaissance Orbiter (LRO) Lunar Orbiter Laser Altimeter (LOLA).

## NASA dataset integrated

**NASA Goddard Space Flight Center — High-Resolution LOLA Topography for Lunar South Pole Sites**

- Product page: https://pgda.gsfc.nasa.gov/products/78
- Data archive: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/

NASA provides GeoTIFF products at 5 m/pixel with south-polar stereographic X/Y coordinates in metres, Moon_ME reference frame, DE421 ephemeris.

### Study areas

| NASA ID | Region |
|---|---|
| Site01 | Connecting ridge |
| Site04 | Shackleton rim |
| Site06 | Nobile rim 1 |
| Site07 | Peak near Shackleton |
| Site11 | de Gerlache rim |
| Site20 | Leibnitz beta plateau |
| Site20v2 | Leibnitz beta plateau, extended |
| Site23 | Malapert massif |
| Site42 | de Gerlache-Kocher massif |

### Data products

| Suffix | Product | Unit |
|---|---|---|
| surf | Surface-interpolated elevation | metres |
| slp | Terrain slope | degrees |
| toterr | Total elevation uncertainty (RMS) | metres |
| slperr | Slope uncertainty (RMS) | degrees |
| ldec | Number of LOLA returns per pixel | count |

NASA's product description notes that roughly 90% of pixels in the improved 5 m/pixel LDEMs for the initial study regions are interpolated. This should not be assumed identical for every tile or derived layer. The return-count and uncertainty products are therefore important context.

## 2026 NASA Space Apps challenge alignment

MoonSight is being developed for the official [Lunar Landing Site Navigator](https://www.spaceappschallenge.org/2026/challenges/lunar-landing-site-navigator/) challenge.

The challenge asks teams to help compare lunar south-pole sites and dates by visualizing Sun and Earth positions relative to the horizon, solar power potential, and direct-to-Earth communication opportunities.

MoonSight now includes a JPL Horizons comparison panel that requests date-specific Sun and Earth azimuth/elevation for two user-entered lunar surface coordinates. MoonSight uses the published center coordinates for the named LOLA study regions from NASA's 2025 Lunar Surface Data Book. NASA states that these centers were derived from the DEM polygons and are accurate to approximately 5–10 metres. They are regional reference points, not a specific landing ellipse. The app also displays a normalized horizontal solar-incidence proxy, max(0, sin(Sun elevation)), which is not a real power-generation estimate.

### Published region-center coordinates

| Study area | Latitude (°) | East longitude (°) |
|---|---:|---:|
| Connecting ridge | -89.4632 | -137.49000 |
| Shackleton rim | -89.7668 | -171.87000 |
| Nobile rim 1 | -85.4381 | 37.36667 |
| Peak near Shackleton | -88.8110 | 123.69010 |
| de Gerlache rim | -88.6834 | -67.93210 |
| Leibnitz beta plateau | -85.4266 | 31.74276 |
| Leibnitz beta plateau (extended) | -85.4266 | 31.74276 |
| Malapert massif | -85.9948 | -0.23578 |
| de Gerlache-Kocher massif | -85.8296 | -116.32200 |

Source: [NASA Lunar Surface Data Book (2025)](https://ntrs.nasa.gov/citations/20250002845). Longitudes are normalized to 0–360° east when sent to Horizons.

## Features

- Load NASA elevation, slope, elevation uncertainty, slope uncertainty, and LOLA return-count GeoTIFFs.
- Display downsampled heatmaps using the source south-polar stereographic X/Y coordinates.
- Inspect preview statistics.
- Compare two study areas for the same terrain product.\n- Compare Sun and Earth azimuth/elevation for two lunar surface points and dates using the JPL Horizons API.
- Export preview values as CSV.

## How it works

1. MoonSight constructs the official NASA GeoTIFF path for the selected site and product.
2. It downloads the GeoTIFF from NASA.
3. Rasterio reads and downsamples the raster for browser-friendly display.
4. The source geotransform is used to label the heatmap in lunar map-projection coordinates.
5. Descriptive statistics are calculated from the displayed preview.

An internet connection is required. Loaded rasters are cached for 24 hours. JPL Horizons ephemerides are cached for one hour.

## Run locally

```bash
git clone https://github.com/dagimfkadie/MoonSight.git
cd MoonSight
pip install -r requirements.txt
streamlit run app.py
```

## Sun/Earth geometry limitations

JPL Horizons supplies apparent azimuth and elevation from a user-defined topocentric point on the Moon. The current display samples one UT day at hourly intervals. It compares the centers of the Sun and Earth against the local geometric reference plane.

This is not a terrain-aware horizon calculation. Crater rims and nearby ridges can block the Sun or Earth even when the body center is geometrically above the reference plane. The Earth is an extended disc, so center elevation is not identical to NASA's full-disc Earth-visibility definition. Communication also depends on antenna pointing, link budget, spacecraft geometry, and ground-network availability.

NASA separately publishes long-term average lunar-polar solar-illumination and Earth-visibility maps: https://pgda.gsfc.nasa.gov/products/69. These products average over long time periods and do not replace date-specific analysis.

## Scientific limitations

- Statistics describe the downsampled preview of an entire archive tile, not a defined landing ellipse.
- The axes show south-polar stereographic X/Y coordinates in metres, not latitude/longitude.
- NASA's product description reports roughly 90% interpolated pixels for the improved LDEMs in its initial study regions; interpolation characteristics should be checked per tile and product.
- Elevation and slope alone cannot establish landing safety. Local hazards, illumination, thermal conditions, communications, navigation uncertainty, and spacecraft-specific constraints require further analysis.
- MoonSight does not calculate a certified landing score and must not be used for actual spacecraft navigation or mission decisions.
- MoonSight is not a NASA product and is not endorsed by NASA.

See [NASA data attribution and citations](NASA_DATA_CITATION.md) for the full data citation and interpretation notes. A short [demo guide](DEMO_SCRIPT.md) is also included.\n\n## Additional ephemeris source

NASA/JPL Horizons API documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html

The Horizons API supports user-defined topocentric coordinates on bodies with a defined rotation model and provides apparent azimuth/elevation output. MoonSight requests the Sun (ID 10) and Earth (ID 399) as seen from a custom point on the Moon (body 301).

## Scientific reference

Barker, M. K. et al. (2021). *Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions*. Planetary and Space Science, 203, 105119. https://doi.org/10.1016/j.pss.2020.105119

## Team

Developed by a student team from Ethiopia for NASA Space Apps Challenge 2026.

## License

A license should be selected by the project team before public reuse.
