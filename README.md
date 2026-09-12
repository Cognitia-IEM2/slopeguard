# SlopeGuard
## Physics-Based Slope Stability & Live Rainfall Highway Landslide Early Warning System
SlopeGuard is an early warning system designed to identify and monitor potential landslide risks along highway slopes.
The system combines *physics-based slope stability analysis, live rainfall data, pore-pressure modeling, terrain parameters, and interactive risk mapping* to estimate the stability of monitored highway segments and provide early warnings when potentially unsafe conditions develop.
---
## Problem Statement
Highway corridors in hilly and mountainous regions are vulnerable to landslides, especially during periods of intense or prolonged rainfall.
Traditional monitoring methods can be expensive, manually intensive, and may not provide timely warnings for every vulnerable slope.
SlopeGuard aims to provide an affordable and scalable digital solution that continuously evaluates slope conditions using rainfall and geotechnical parameters, helping identify potentially unstable highway segments before a landslide occurs.
---
## Key Features
- *Live Rainfall Monitoring*
  - Retrieves current weather and rainfall information using the Open-Meteo API.
- *Physics-Based Slope Stability*
  - Estimates slope stability using the Factor of Safety (FoS).
- *Rainfall–Pore Pressure Coupling*
  - Models how rainfall infiltration can increase pore-water pressure within the soil.
- *Geotechnical Soil Parameters*
  - Uses soil cohesion, friction angle, unit weight, and soil depth in stability calculations.
- *Interactive Risk Map*
  - Displays monitored highway segments on an interactive Folium map.
  - Segments are classified according to their estimated stability and risk.
- *Risk Classification*
  - Segments are categorized into:
    - Stable
    - Marginal
    - Unstable
- *Segment-Level Analysis*
  - Evaluates multiple highway segments and identifies the highest-risk locations.
- *Tunable Risk Thresholds*
  - Risk thresholds can be adjusted for different monitoring requirements.
- *Transparent Calculations*
  - Provides physically interpretable stability indicators instead of relying only on a black-box prediction.
---
## How It Works
SlopeGuard follows the pipeline:
*Rainfall → Infiltration → Pore Pressure → Slope Stability → Factor of Safety → Risk Level → Early Warning*
### 1. Rainfall Input
Live rainfall information is retrieved for the monitored location.
### 2. Rainfall–Infiltration Model
Rainfall is converted into an estimated infiltrated water amount using an infiltration factor.
### 3. Pore Pressure Estimation
The estimated water infiltration is used to calculate an increase in pore-water pressure.
### 4. Factor of Safety
The system applies an infinite-slope stability model using:
- Slope angle
- Soil cohesion
- Soil friction angle
- Soil unit weight
- Soil depth
- Pore-water pressure
The Factor of Safety is calculated as:
*FoS = Resisting Shear Strength / Driving Shear Stress*
### 5. Risk Classification
The calculated stability condition is converted into a risk category.
### 6. Highway Segment Ranking
Multiple monitored segments are analyzed and ranked to identify locations requiring greater attention.
---
## Technology Stack
### Backend
- Python
- Flask
### Data and APIs
- Open-Meteo API
- Python Requests
### Geospatial Visualization
- Folium
- OpenStreetMap
- OpenTopoMap
- Interactive map layers and markers
### Scientific Modeling
- Infinite-slope stability analysis
- Factor of Safety calculation
- Rainfall infiltration modeling
- Pore-pressure estimation
### Frontend
- HTML
- CSS
- JavaScript
---
## Project Structure
```text
SlopeGuard/
│
├── app.py
│
├── core/
│   ├── rainfall.py
│   ├── risk_engine.py
│   ├── pore_pressure.py
│   └── slope_stability.py
│
├── dashboard/
│   └── map.py
│
├── templates/
│   └── index.html
│
├── requirements.txt
├── README.md
└── .gitignore

⸻

Installation

1. Clone the repository

git clone https://github.com/anushka-b31/slopegurd.git
cd slopegurd

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows

venv\Scripts\activate

macOS / Linux

source venv/bin/activate

4. Install dependencies

python -m pip install -r requirements.txt

⸻

Running the Application

Start the Flask application:

python app.py

The application will run locally at:

http://127.0.0.1:5000

Open the address in your browser to access the SlopeGuard dashboard.

⸻

Dashboard

The SlopeGuard dashboard provides:

* Overall highway risk status
* Highest-risk segment
* Live rainfall information
* Slope stability information
* Segment-wise risk analysis
* Interactive risk map
* Risk alerts

⸻

Risk Interpretation

Condition	Interpretation
Stable	Slope has a relatively safe stability condition
Marginal	Slope requires increased monitoring
Unstable	Potentially unsafe condition requiring attention

The thresholds can be tuned according to the monitoring environment and engineering requirements.

⸻

Why SlopeGuard?

Most landslide warning approaches focus on rainfall thresholds alone.

SlopeGuard goes one step further by connecting rainfall to a simplified physical mechanism:

Rainfall → Water Infiltration → Pore Pressure → Reduced Effective Stress → Slope Stability

This makes the system more interpretable and provides an engineering-oriented basis for early warning.

⸻

Limitations

SlopeGuard is a prototype screening and early-warning system and should not replace detailed geotechnical investigations.

The current implementation uses simplified slope-stability and rainfall–infiltration assumptions. Real-world deployment would require:

* High-resolution DEM/elevation data
* Detailed soil and geological surveys
* Real highway geometry
* Field instrumentation
* Soil moisture and pore-pressure sensors
* Historical landslide inventories
* Calibration using local rainfall and failure data
* Validation against observed landslide events

⸻

Future Scope

Future versions of SlopeGuard can integrate:

* Real-time DEM and satellite data
* GIS-based highway and terrain datasets
* Soil and geological maps
* IoT pore-pressure and soil-moisture sensors
* Historical landslide databases
* Satellite-based change detection
* Advanced rainfall forecasting
* Machine-learning-assisted calibration
* Automated SMS/email emergency alerts
* Multi-highway monitoring
* Cloud deployment and scalable APIs

⸻

Impact

SlopeGuard can support highway authorities, disaster-management teams, and local administrations by helping them:

* Identify vulnerable highway segments
* Monitor rainfall-driven slope conditions
* Prioritize high-risk locations
* Improve early-warning capability
* Reduce dependence on manual monitoring
* Support faster preventive action

The goal is to move from reactive landslide response toward proactive risk monitoring and early warning.

⸻

Hackathon Prototype

SlopeGuard was developed as a prototype for a Physics-Based Slope Stability & Live Rainfall Highway Landslide Early Warning System.

The project demonstrates how physical slope-stability principles and live environmental data can be combined into an accessible digital monitoring platform.

⸻

License

This project is intended for educational, research, and hackathon purposes.
