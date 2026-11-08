# MoonSight — demonstration guide

## Suggested 90-second walkthrough

**0:00–0:15 — The problem**

"Choosing a lunar landing region requires more than looking at a Moon image. Terrain slope, elevation, and uncertainty affect how scientists interpret a candidate region."

**0:15–0:30 — The source**

"MoonSight uses public Lunar Orbiter Laser Altimeter data from NASA's Lunar Reconnaissance Orbiter. The NASA archive provides elevation and slope GeoTIFFs, plus uncertainty and laser-return-count layers."

**0:30–0:55 — Live exploration**

1. Open the app.
2. Select a named south-pole study area.
3. Select Elevation and load the NASA data.
4. Show the heatmap and explain that its axes are south-polar map coordinates in metres.
5. Switch to Slope, then to Elevation uncertainty or LOLA return count.

**0:55–1:15 — Comparison**

"MoonSight lets us compare two archive study areas using the same terrain measurement. The current comparison uses downsampled previews, so these values are exploratory summaries, not landing-ellipse scores."

**1:15–1:30 — Limitations and next step**

"NASA's documentation warns that many 5-metre elevation pixels are interpolated. That's why MoonSight includes uncertainty and data-count layers. The next research step is to combine terrain with illumination and local hazard data. This prototype does not certify landing safety."

## Before recording

- Confirm the app successfully downloads at least one NASA raster on the deployment platform.
- Record the exact study area and product used in the demo.
- Show the NASA source link in the Science & Sources tab.
- Do not invent or claim a best or safest landing site.
- Make clear which values are downsampled preview statistics.
- Mention the selected official NASA Space Apps challenge in the introduction and explain how the project addresses it.
