
# 🌕 MoonSight — Lunar Landing Site Navigator

**Explore the Moon. Compare landing locations. Understand the lunar environment.**

MoonSight is an interactive educational web application designed to help users explore potential lunar landing locations and understand the environmental conditions that could affect future Moon missions.

By combining lunar geographic information, sunlight visualization, Earth visibility, and communication-window estimates, MoonSight brings important aspects of lunar exploration into one interactive platform.

## 🚀 Project Overview

Choosing a suitable lunar landing location involves understanding several environmental factors. MoonSight aims to make these factors easier to explore through an accessible, interactive dashboard.

Users can select locations, explore lunar surface information, compare dates, and examine estimated environmental conditions.

## ✨ Key Features

### 1. Interactive Lunar Map
- Explore selected regions of the Moon.
- Select and examine potential landing locations.
- View geographic information about selected areas.

### 2. Lunar Lighting Explorer
- Select different dates for comparison.
- Explore estimated sunlight conditions.
- Understand how illumination changes over time.

### 3. Sun Position Visualization
- Visualize the estimated direction of sunlight.
- Explore how the Sun's position affects lunar surface illumination.
- Understand the importance of lighting for lunar exploration.

### 4. Earth Visibility and Communication
- Explore estimated Earth visibility from selected locations.
- Understand how location and lunar geometry affect communication opportunities.
- Visualize potential communication windows.

### 5. Landing Site Comparison Dashboard
Compare selected locations using available information, including:
- Geographic characteristics
- Surface illumination
- Earth visibility
- Estimated communication opportunities

## 🛰️ Why MoonSight?

Future lunar missions require careful consideration of landing locations and environmental conditions.

MoonSight aims to make lunar exploration data more understandable and accessible by combining multiple information sources into one interactive experience.

The project is designed as an educational prototype, not a certified lunar mission-planning system.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web application |
| Pandas | Data processing |
| Plotly | Interactive visualizations |
| NASA datasets | Lunar exploration information |

## 📡 Data Sources

MoonSight is designed to use publicly available scientific data, including relevant NASA lunar datasets.

Potential sources include:

- [NASA Open Data Portal](https://data.nasa.gov/)
- [NASA Scientific Visualization Studio](https://svs.gsfc.nasa.gov/)
- [NASA Planetary Data System](https://pds.nasa.gov/)
- [NASA/JPL Solar System Dynamics](https://ssd.jpl.nasa.gov/)

Specific datasets and their use will be documented as they are integrated.

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/dagimfkadie/MoonSight.git
cd MoonSight
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 📁 Project Structure

```text
MoonSight/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── README.md
│
├── modules/
│   ├── lunar_map.py
│   ├── lighting.py
│   ├── sun_position.py
│   ├── earth_visibility.py
│   └── comparison.py
│
└── assets/
    └── README.md
```

## 🌍 Our Mission

Our goal is to make scientific information about the Moon more accessible and help people better understand the challenges of future lunar exploration.

**Explore. Analyze. Discover.**

## 👥 Team

Developed by a student team from Ethiopia for NASA Space Apps Challenge 2026.

## ⚠️ Scientific Limitations

MoonSight is an educational prototype. Estimates and visualizations will be identified clearly, and scientific calculations will be documented with their assumptions and data sources.

It must not be used for actual spacecraft navigation or mission decisions.

## 📜 License

This project is intended for educational and research purposes. A license will be added to clarify reuse and distribution.
