from flask import Flask, render_template, request, jsonify

from core.rainfall import get_rainfall
from core.risk_engine import analyze_route
from dashboard.map import create_risk_map


app = Flask(__name__)


# ============================================================
# DEFAULT LOCATION
# ============================================================

DEFAULT_START_LAT = 31.1048
DEFAULT_START_LON = 77.1734

DEFAULT_END_LAT = 31.1210
DEFAULT_END_LON = 77.1900


# ============================================================
# MAIN DASHBOARD
# ============================================================

@app.route("/", methods=["GET", "POST"])
def home():

    # Default values
    start_lat = DEFAULT_START_LAT
    start_lon = DEFAULT_START_LON

    end_lat = DEFAULT_END_LAT
    end_lon = DEFAULT_END_LON

    segments = 12

    unstable_cutoff = 1.00
    marginal_cutoff = 1.30

    error = None


    # --------------------------------------------------------
    # READ FORM DATA
    # --------------------------------------------------------

    if request.method == "POST":

        try:

            start_lat = float(
                request.form.get(
                    "start_lat",
                    DEFAULT_START_LAT
                )
            )

            start_lon = float(
                request.form.get(
                    "start_lon",
                    DEFAULT_START_LON
                )
            )

            end_lat = float(
                request.form.get(
                    "end_lat",
                    DEFAULT_END_LAT
                )
            )

            end_lon = float(
                request.form.get(
                    "end_lon",
                    DEFAULT_END_LON
                )
            )

            segments = int(
                request.form.get(
                    "segments",
                    12
                )
            )

            unstable_cutoff = float(
                request.form.get(
                    "unstable_cutoff",
                    1.00
                )
            )

            marginal_cutoff = float(
                request.form.get(
                    "marginal_cutoff",
                    1.30
                )
            )


            # ------------------------------------------------
            # LIMIT VALUES
            # ------------------------------------------------

            segments = max(
                5,
                min(30, segments)
            )


            if marginal_cutoff <= unstable_cutoff:

                marginal_cutoff = (
                    unstable_cutoff + 0.30
                )


            # ------------------------------------------------
            # CHECK COORDINATES
            # ------------------------------------------------

            if not (-90 <= start_lat <= 90):
                raise ValueError(
                    "Start latitude must be between -90 and 90."
                )

            if not (-180 <= start_lon <= 180):
                raise ValueError(
                    "Start longitude must be between -180 and 180."
                )

            if not (-90 <= end_lat <= 90):
                raise ValueError(
                    "End latitude must be between -90 and 90."
                )

            if not (-180 <= end_lon <= 180):
                raise ValueError(
                    "End longitude must be between -180 and 180."
                )


        except (ValueError, TypeError) as e:

            error = str(e)

            start_lat = DEFAULT_START_LAT
            start_lon = DEFAULT_START_LON

            end_lat = DEFAULT_END_LAT
            end_lon = DEFAULT_END_LON

            segments = 12

            unstable_cutoff = 1.00
            marginal_cutoff = 1.30


    # ========================================================
    # GET LIVE RAINFALL
    # ========================================================

    weather = get_rainfall(
        start_lat,
        start_lon
    )

    rainfall_mm = weather.get(
        "rainfall_mm",
        0.0
    )


    # ========================================================
    # RUN SLOPE RISK ANALYSIS
    # ========================================================

    results = analyze_route(

        start_lat=start_lat,

        start_lon=start_lon,

        end_lat=end_lat,

        end_lon=end_lon,

        segments=segments,

        rainfall_mm=rainfall_mm,

        unstable_cutoff=unstable_cutoff,

        marginal_cutoff=marginal_cutoff
    )


    # ========================================================
    # COUNT RISK LEVELS
    # ========================================================

    unstable_count = sum(
        1
        for r in results
        if r["classification"] == "UNSTABLE"
    )

    marginal_count = sum(
        1
        for r in results
        if r["classification"] == "MARGINAL"
    )

    stable_count = sum(
        1
        for r in results
        if r["classification"] == "STABLE"
    )


    # ========================================================
    # OVERALL RISK
    # ========================================================

    if unstable_count > 0:

        overall_risk = "UNSTABLE"

    elif marginal_count > 0:

        overall_risk = "MARGINAL"

    else:

        overall_risk = "STABLE"


    # ========================================================
    # HIGHEST RISK SEGMENT
    # ========================================================

    if results:

        highest_risk = max(
            results,
            key=lambda x: x.get(
                "risk_score",
                0
            )
        )

    else:

        highest_risk = {

            "segment": "N/A",

            "risk_score": 0,

            "fos": 0,

            "slope_deg": 0,

            "rainfall_mm": 0,

            "pore_pressure_kpa": 0

        }


    # ========================================================
    # FORM VALUES
    # ========================================================

    values = {

        "start_lat": start_lat,

        "start_lon": start_lon,

        "end_lat": end_lat,

        "end_lon": end_lon,

        "segments": segments,

        "unstable_cutoff": unstable_cutoff,

        "marginal_cutoff": marginal_cutoff

    }


    # ========================================================
    # RENDER DASHBOARD
    # ========================================================

    return render_template(

        "index.html",

        # We no longer directly embed the Folium map here.
        # The map is loaded through /risk-map.
        map_html="",

        results=results,

        weather=weather,

        unstable_count=unstable_count,

        marginal_count=marginal_count,

        stable_count=stable_count,

        overall=overall_risk,

        highest_risk=highest_risk,

        error=error,

        values=values

    )


# ============================================================
# DEDICATED FOLIUM RISK MAP
# ============================================================

@app.route("/risk-map")
def risk_map_page():

    try:

        start_lat = float(
            request.args.get(
                "start_lat",
                DEFAULT_START_LAT
            )
        )

        start_lon = float(
            request.args.get(
                "start_lon",
                DEFAULT_START_LON
            )
        )

        end_lat = float(
            request.args.get(
                "end_lat",
                DEFAULT_END_LAT
            )
        )

        end_lon = float(
            request.args.get(
                "end_lon",
                DEFAULT_END_LON
            )
        )

        segments = int(
            request.args.get(
                "segments",
                12
            )
        )

        unstable_cutoff = float(
            request.args.get(
                "unstable_cutoff",
                1.00
            )
        )

        marginal_cutoff = float(
            request.args.get(
                "marginal_cutoff",
                1.30
            )
        )

    except (ValueError, TypeError):

        start_lat = DEFAULT_START_LAT
        start_lon = DEFAULT_START_LON

        end_lat = DEFAULT_END_LAT
        end_lon = DEFAULT_END_LON

        segments = 12

        unstable_cutoff = 1.00
        marginal_cutoff = 1.30


    # --------------------------------------------------------
    # LIMIT SEGMENTS
    # --------------------------------------------------------

    segments = max(
        5,
        min(30, segments)
    )


    # --------------------------------------------------------
    # GET RAINFALL
    # --------------------------------------------------------

    weather = get_rainfall(
        start_lat,
        start_lon
    )

    rainfall_mm = weather.get(
        "rainfall_mm",
        0.0
    )


    # --------------------------------------------------------
    # ANALYZE ROUTE
    # --------------------------------------------------------

    results = analyze_route(

        start_lat=start_lat,

        start_lon=start_lon,

        end_lat=end_lat,

        end_lon=end_lon,

        segments=segments,

        rainfall_mm=rainfall_mm,

        unstable_cutoff=unstable_cutoff,

        marginal_cutoff=marginal_cutoff

    )


    # --------------------------------------------------------
    # CREATE FOLIUM MAP
    # --------------------------------------------------------

    risk_map = create_risk_map(

        results,

        start=(
            start_lat,
            start_lon
        )

    )


    # --------------------------------------------------------
    # RETURN MAP DIRECTLY
    # --------------------------------------------------------

    return risk_map.get_root().render()


# ============================================================
# WEATHER API
# ============================================================

@app.route("/api/weather", methods=["GET"])
def weather_api():

    try:

        lat = float(
            request.args.get(
                "lat",
                DEFAULT_START_LAT
            )
        )

        lon = float(
            request.args.get(
                "lon",
                DEFAULT_START_LON
            )
        )

    except (ValueError, TypeError):

        return jsonify({

            "error":
            "Invalid latitude or longitude"

        }), 400


    if not (-90 <= lat <= 90):

        return jsonify({

            "error":
            "Latitude must be between -90 and 90"

        }), 400


    if not (-180 <= lon <= 180):

        return jsonify({

            "error":
            "Longitude must be between -180 and 180"

        }), 400


    weather = get_rainfall(
        lat,
        lon
    )


    return jsonify(weather)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "ok",

        "application": "SlopeGuard",

        "rainfall_source": "Open-Meteo",

        "map": "Folium + Leaflet",

        "risk_model":
        "Physics-based infinite-slope screening",

        "message":
        "SlopeGuard is running successfully."

    })


# ============================================================
# INCIDENT FEEDBACK
# ============================================================

@app.route(
    "/api/incident",
    methods=["POST"]
)
def incident_feedback():

    data = request.get_json(
        silent=True
    )

    if data is None:

        data = {}


    segment = data.get(
        "segment",
        "Unknown"
    )

    confirmed = data.get(
        "confirmed",
        False
    )


    return jsonify({

        "status": "recorded",

        "segment": segment,

        "confirmed": bool(
            confirmed
        ),

        "message":
        "Incident feedback received."

    })


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )