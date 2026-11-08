# 🌕 MoonSight — Lunar Landing Site Navigator

**Explore the Moon using real lunar terrain measurements.**

MoonSight is an educational web application for exploring NASA Lunar Reconnaissance Orbiter (LRO) terrain data from selected lunar south-pole study areas.

## NASA data integrated

MoonSight retrieves NASA's **LOLA South Pole Landing Site DEM** GeoTIFF products directly from the NASA Goddard Planetary Geology, Geophysics and Geochemistry Laboratory archive.

The archive provides, for six named south-pole study areas:
- Surface-interpolated elevation maps (LDEM)
- Slope maps in degrees
- Additional products including data-count and uncertainty maps

The elevation and slope GeoTIFF products are documented at **5 metres per pixel** and use south-polar stereographic X/Y coordinates in the Moon_ME reference frame (DE421).

### Study areas

- Site 01 — Connecting ridge
- Site 04 — Shackleton rim
- Site 07 — Peak near Shackleton
- Site 11 — de Gerlache rim
- Site 20 — Leibnitz beta plateau
- Site 23 — Malapert massif

**Primary data source:** [NASA LOLA South Pole Landing Site DEMs](https://core2.gsfc.nasa.gov/PGDA/LOLA_5mpp/)

**Instrument background:** [NASA LRO data products](https://science.nasa.gov/mission/lro/data-products/)

**Additional exploration tool:** [NASA Moon Trek](https://trek.nasa.gov/moon/)

## How the integration works

1. Select a NASA study area and choose elevation or slope.
2. MoonSight downloads the corresponding GeoTIFF from NASA.
3. The app reads the raster, handles no-data pixels, and calculates descriptive statistics from a downsampled raster.
4. It displays a heatmap of the raster values.

The app requires an internet connection to retrieve the NASA data. Raster files are cached for 24 hours to reduce repeated downloads.

## Run locally

```bash
git clone https://github.com/dagimfkadie/MoonSight.git
cd MoonSight
pip install -r requirements.txt
streamlit run app.py
```

## Scientific limitations

- The current heatmap uses raster row and column indices, not geographic latitude/longitude.
- The prototype does not yet calculate a certified landing suitability score.
- Elevation and slope are only two factors. Illumination, rocks, craters, thermal conditions, communications, navigation uncertainty, and spacecraft constraints also matter.
- The visualized study areas are research locations in NASA's archive, not declarations of approved or safe landing sites.
- MoonSight is not a NASA product and is not endorsed by NASA.

## Team

Developed by a student team from Ethiopia for NASA Space Apps Challenge 2026.

## License

A license should be selected by the project team before public reuse.
