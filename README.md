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

NASA's product description notes that roughly 90% of pixels in these interpolated polar elevation maps are interpolated. The return-count and uncertainty products are therefore important context.

## Features

- Load NASA elevation, slope, elevation uncertainty, slope uncertainty, and LOLA return-count GeoTIFFs.
- Display downsampled heatmaps using the source south-polar stereographic X/Y coordinates.
- Inspect preview statistics.
- Compare two study areas for the same product.
- Export preview values as CSV.

## How it works

1. MoonSight constructs the official NASA GeoTIFF path for the selected site and product.
2. It downloads the GeoTIFF from NASA.
3. Rasterio reads and downsamples the raster for browser-friendly display.
4. The source geotransform is used to label the heatmap in lunar map-projection coordinates.
5. Descriptive statistics are calculated from the displayed preview.

An internet connection is required. Loaded rasters are cached for 24 hours.

## Run locally

```bash
git clone https://github.com/dagimfkadie/MoonSight.git
cd MoonSight
pip install -r requirements.txt
streamlit run app.py
```

## Scientific limitations

- Statistics describe the downsampled preview of an entire archive tile, not a defined landing ellipse.
- The axes show south-polar stereographic X/Y coordinates in metres, not latitude/longitude.
- NASA's elevation products are interpolated surfaces; the product description notes that roughly 90% of pixels are interpolated.
- Elevation and slope alone cannot establish landing safety. Local hazards, illumination, thermal conditions, communications, navigation uncertainty, and spacecraft-specific constraints require further analysis.
- MoonSight does not calculate a certified landing score and must not be used for actual spacecraft navigation or mission decisions.
- MoonSight is not a NASA product and is not endorsed by NASA.

## Scientific reference

Barker, M. K. et al. (2021). *Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions*. Planetary and Space Science, 203, 105119. https://doi.org/10.1016/j.pss.2020.105119

## Team

Developed by a student team from Ethiopia for NASA Space Apps Challenge 2026.

## License

A license should be selected by the project team before public reuse.
