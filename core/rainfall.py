import requests


def get_rainfall(lat, lon):
    """
    Get current and forecast rainfall from Open-Meteo.
    No API key required.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,rain,precipitation",
        "hourly": "precipitation,rain",
        "forecast_days": 1,
        "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current", {})

        rainfall = current.get(
            "rain",
            0
        )

        precipitation = current.get(
            "precipitation",
            0
        )

        temperature = current.get(
            "temperature_2m"
        )

        return {
            "rainfall_mm": float(rainfall or 0),
            "precipitation_mm": float(precipitation or 0),
            "temperature": temperature,
            "humidity": None,
            "description": "Live rainfall from Open-Meteo",
            "live": True
        }

    except Exception as e:

        print(
            "Rainfall API error:",
            e
        )

        return {
            "rainfall_mm": 0.0,
            "precipitation_mm": 0.0,
            "temperature": None,
            "humidity": None,
            "description": "Rainfall data unavailable",
            "live": False
        }
