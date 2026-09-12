import folium
from folium.plugins import HeatMap


RISK_COLORS = {
    "UNSTABLE": "#ef4444",
    "MARGINAL": "#f59e0b",
    "STABLE": "#22c55e"
}


def create_risk_map(results, start=(20.5937, 78.9629)):

    # -----------------------------
    # CREATE INDIA MAP
    # -----------------------------
    risk_map = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        control_scale=True,
        tiles="OpenStreetMap"
    )

    # -----------------------------
    # MAP LAYERS
    # -----------------------------
    folium.TileLayer(
        tiles="OpenTopoMap",
        name="Terrain",
        control=True
    ).add_to(risk_map)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
              "World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite",
        control=True
    ).add_to(risk_map)

    # -----------------------------
    # SORT RESULTS
    # -----------------------------
    route_results = sorted(
        results,
        key=lambda r: r.get("segment", "")
    )

    # -----------------------------
    # HEATMAP
    # -----------------------------
    heat_data = []

    for r in route_results:

        lat = r.get("lat")
        lon = r.get("lon")
        score = r.get("risk_score", 0)

        if lat is not None and lon is not None:

            heat_data.append([
                float(lat),
                float(lon),
                float(score) / 100.0
            ])

    if heat_data:

        HeatMap(
            heat_data,
            name="Landslide Risk Heatmap",
            min_opacity=0.35,
            radius=30,
            blur=25,
            max_zoom=10
        ).add_to(risk_map)

    # -----------------------------
    # HIGHWAY ROUTE
    # -----------------------------
    route_points = []

    for r in route_results:

        lat = r.get("lat")
        lon = r.get("lon")

        if lat is not None and lon is not None:
            route_points.append([lat, lon])

    if len(route_points) >= 2:

        folium.PolyLine(
            route_points,
            color="#38bdf8",
            weight=5,
            opacity=0.9,
            tooltip="Monitored Highway Route"
        ).add_to(risk_map)

    # -----------------------------
    # SEGMENT MARKERS
    # -----------------------------
    for r in route_results:

        lat = r.get("lat")
        lon = r.get("lon")

        if lat is None or lon is None:
            continue

        classification = r.get(
            "classification",
            "STABLE"
        )

        color = RISK_COLORS.get(
            classification,
            "#22c55e"
        )

        segment = r.get(
            "segment",
            "Unknown"
        )

        risk_score = r.get(
            "risk_score",
            0
        )

        fos = r.get(
            "fos",
            0
        )

        slope = r.get(
            "slope_deg",
            0
        )

        rainfall = r.get(
            "rainfall_mm",
            0
        )

        pore_pressure = r.get(
            "pore_pressure_kpa",
            0
        )

        confidence = r.get(
            "confidence",
            "MEDIUM"
        )

        popup_html = f"""
        <div style="
            width:250px;
            font-family:Arial;
            font-size:13px;
        ">

            <h3 style="
                color:{color};
                margin-bottom:12px;
            ">
                {segment}
            </h3>

            <b>Risk Level:</b>
            {classification}

            <br><br>

            <b>Risk Score:</b>
            {risk_score}/100

            <br><br>

            <b>Factor of Safety:</b>
            {fos}

            <br><br>

            <b>Slope:</b>
            {slope}°

            <br><br>

            <b>Rainfall:</b>
            {rainfall} mm

            <br><br>

            <b>Pore Pressure:</b>
            {pore_pressure} kPa

            <br><br>

            <b>Confidence:</b>
            {confidence}

            <hr>

            <b>Latitude:</b>
            {lat}

            <br>

            <b>Longitude:</b>
            {lon}

        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=9,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            weight=2,
            popup=folium.Popup(
                popup_html,
                max_width=320
            ),
            tooltip=f"{segment} | {classification}"
        ).add_to(risk_map)

    # -----------------------------
    # START LOCATION
    # -----------------------------
    folium.Marker(
        location=[
            start[0],
            start[1]
        ],
        tooltip="Monitoring Start",
        popup="Highway monitoring starts here.",
        icon=folium.Icon(
            color="blue",
            icon="play"
        )
    ).add_to(risk_map)

    # -----------------------------
    # CLICK ANYWHERE ON MAP
    # -----------------------------
    map_name = risk_map.get_name()

    click_script = f"""
    <script>

    {map_name}.on('click', function(e) {{

        var lat = e.latlng.lat.toFixed(6);
        var lon = e.latlng.lng.toFixed(6);

        L.popup()
            .setLatLng(e.latlng)
            .setContent(
                '<div style="font-family:Arial;width:230px;">' +
                '<h3 style="margin-top:0;">Location Selected</h3>' +
                '<b>Latitude:</b> ' + lat +
                '<br><b>Longitude:</b> ' + lon +
                '<br><br>' +
                '<span style="color:#64748b;">' +
                'Nearest monitored highway segment can be inspected using the markers.' +
                '</span>' +
                '</div>'
            )
            .openOn({map_name});

        L.circleMarker(
            e.latlng,
            {{
                radius: 7,
                color: '#2563eb',
                fillColor: '#60a5fa',
                fillOpacity: 0.8
            }}
        ).addTo({map_name});

    }});

    </script>
    """

    risk_map.get_root().html.add_child(
        folium.Element(click_script)
    )

    # -----------------------------
    # LEGEND
    # -----------------------------
    legend_html = """

    <div style="
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;

        background: rgba(7,20,38,0.95);

        padding: 15px 18px;

        border-radius: 10px;

        border: 1px solid #385477;

        color: white;

        font-family: Arial;

        font-size: 12px;

        box-shadow:
            0 5px 20px rgba(0,0,0,0.4);
    ">

        <div style="
            font-size:14px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            Landslide Risk
        </div>

        <div style="margin:7px 0;">

            <span style="
                display:inline-block;
                width:12px;
                height:12px;
                background:#ef4444;
                border-radius:50%;
                margin-right:7px;
            "></span>

            Very High / Unstable

        </div>

        <div style="margin:7px 0;">

            <span style="
                display:inline-block;
                width:12px;
                height:12px;
                background:#f59e0b;
                border-radius:50%;
                margin-right:7px;
            "></span>

            High / Marginal

        </div>

        <div style="margin:7px 0;">

            <span style="
                display:inline-block;
                width:12px;
                height:12px;
                background:#22c55e;
                border-radius:50%;
                margin-right:7px;
            "></span>

            Low / Stable

        </div>

        <hr style="
            border-color:#385477;
            margin:10px 0;
        ">

        <div style="
            color:#9bb1cc;
            font-size:10px;
        ">
            Click anywhere on the map to inspect a location.
        </div>

    </div>

    """

    risk_map.get_root().html.add_child(
        folium.Element(legend_html)
    )

    # -----------------------------
    # LAYER CONTROL
    # -----------------------------
    folium.LayerControl(
        position="topright",
        collapsed=False
    ).add_to(risk_map)

    return risk_map
