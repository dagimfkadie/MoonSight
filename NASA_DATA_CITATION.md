# NASA data attribution and citations

MoonSight retrieves public NASA LOLA raster products at runtime. The application does not own or redistribute the original NASA GeoTIFFs.

## Primary dataset

NASA Goddard Space Flight Center, Planetary Geology, Geophysics and Geochemistry Laboratory.

**High-Resolution LOLA Topography for Lunar South Pole Sites**

- Product documentation: https://pgda.gsfc.nasa.gov/products/78
- Data directory: https://pgda.gsfc.nasa.gov/data/LOLA_5mpp/
- Instrument: Lunar Orbiter Laser Altimeter (LOLA), on the Lunar Reconnaissance Orbiter (LRO).
- Grid: 5 metres per pixel.
- Map coordinates: south-polar stereographic X/Y coordinates in metres.
- Reference frame: Moon_ME, ephemeris DE421.

## Products used

| File suffix | Description | Units |
|---|---|---|
| surf | Surface-interpolated elevation model | metres |
| slp | Slope map | degrees |
| toterr | Total elevation uncertainty (RMS) | metres |
| slperr | Slope uncertainty (RMS) | degrees |
| ldec | Number of LOLA returns per pixel | count |

The files are served directly by NASA. MoonSight downsamples them for interactive visualization and computes descriptive statistics from the displayed preview. These statistics are not full-resolution statistics.

## Scientific paper

Barker, M. K., et al. (2021). *Improved LOLA Elevation Maps for South Pole Landing Sites: Error Estimates and Their Impact on Illumination Conditions*. Planetary and Space Science, 203, 105119.

https://doi.org/10.1016/j.pss.2020.105119

The NASA product page also refers to:

Mazarico, E., et al. (2011). *Illumination conditions of the lunar polar regions using LOLA topography*. Icarus, 211(2), 1066–1081. https://doi.org/10.1016/j.icarus.2010.10.030

## Interpretation notes

NASA's product description explains that the improved 5 m/pixel LDEMs for the initial study regions contain a large fraction of interpolated pixels (approximately 90%). This is a property of the described products and should not be assumed identical for every tile or every derived layer. The LOLA return-count and uncertainty layers should be considered alongside elevation and slope.

These datasets are research products, not landing approvals. A site-wide average does not describe the hazards in a particular landing ellipse. MoonSight is an independent educational project and is not endorsed by NASA.

## Date-specific Sun and Earth ephemerides

MoonSight also queries the NASA/JPL Horizons API for the apparent azimuth and elevation of the Sun (target ID 10) and Earth (target ID 399) as viewed from a user-defined lunar surface point (Moon body ID 301).

- API documentation: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- API endpoint: https://ssd.jpl.nasa.gov/api/horizons.api

The application uses observer ephemerides, geodetic lunar site coordinates, UT time, and azimuth/elevation quantity 4. Results are sampled hourly over the selected UT date.

JPL Horizons reference manual: https://ssd.jpl.nasa.gov/horizons/manual.html

## Long-term lunar illumination and Earth visibility context

NASA PGDA also provides long-term average polar solar illumination and Earth-visibility maps:
https://pgda.gsfc.nasa.gov/products/69

Those products average over long periods (including an 18.6-year lunar nutation cycle in the described products) and should not be confused with the date-specific Horizons output.

## Published lunar study-region coordinates

The named region-center coordinates used for MoonSight's JPL Horizons scenarios are taken from NASA's 2025 *Lunar Surface Data Book*, Table A2.1-1. The document states that the coordinates were generated from the south-pole LOLA DEM files and that the centers of the original polygons are accurate to approximately 5–10 metres.

NASA Technical Reports Server record: https://ntrs.nasa.gov/citations/20250002845

These coordinates identify regional reference points. They are not the center of a selected landing ellipse and do not establish a safe landing location.
