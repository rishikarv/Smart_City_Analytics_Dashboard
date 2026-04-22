import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import folium
from sklearn.preprocessing import LabelEncoder
import numpy as np

st.markdown("""
    <style>
    /* Background */
.stApp {
    background-color: #0d1117;
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22;
}

/* TEXT COLORS */
h1, h2, h3 {
    color: #ffffff;
}

p, label, div {
    color: #e6edf3 !important;
}

/* Inputs */
.stNumberInput input {
    color: white !important;
    background-color: #161b22 !important;
}

/* Buttons */
.stButton>button {
    background-color: #238636;
    color: white;
    border-radius: 8px;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #2ea043;
}
    /* Cards effect */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
    }
            /* REMOVE TOP SPACE */
.block-container {
    padding-top: 1rem;
}
[data-testid="stSidebarCollapsedControl"]:hover {
    background-color: #2ea043 !important;
    border-radius: 8px;
}
/* Fix selectbox text visibility */
div[data-baseweb="select"] > div {
    color: white !important;
    background-color: #161b22 !important;
}

/* Dropdown menu */
ul {
    background-color: #161b22 !important;
    color: white !important;
}



/* REMOVE HEADER SPACE */
header {
    background: transparent !important;
}
footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🌆 Smart City Analytics Dashboard</h1>", unsafe_allow_html=True)


st.sidebar.markdown("## 🚀Modules")
st.sidebar.markdown("Select a module to explore:")
option = st.sidebar.radio(
    "Select Module",
    ["Overview","Energy Consumption", "Traffic Congestion", "Crime Hotspots", "Air Quality Level", "Waste Collection Route"]
)
if option == "Overview":
   if option == "Overview":
    st.markdown("""
    
    #### ⚡ Energy Consumption Prediction
    Forecasts energy usage (kWh) based on time factors (month, day, hour, minute), temperature, and weekday/weekend patterns.
    #### 🚦 Traffic Congestion Prediction
    Predicts traffic levels (Low, Medium, High) using inputs like vehicle count, speed, lane occupancy, and flow rate.
    #### 🚓 Crime Hotspot Detection
    Uses clustering (K-Means) on real crime location data to identify high-risk zones and visualize them on a heatmap.
    #### 🌫️ Air Pollution (AQI) Prediction
    Estimates Air Quality Index using environmental parameters such as PM2.5, PM10, NO₂, CO, temperature, and humidity.
    #### 🗑️ Waste Route Optimization
    Identifies high-fill waste bins (>70%) and generates an optimized collection route using distance-based algorithms.

   ---
    💡 This project demonstrates the practical use of Machine Learning, Data Visualization, and Optimization techniques in smart city development.
    """)
if option == "Energy Consumption":
    st.header("⚡ Energy Conusmption Prediction")

    model = joblib.load("models/EnergyConsumption.pkl")
    colE1, colE2 = st.columns(2)

    with colE1:
       month = st.slider("Month", 1, 12)
       day = st.slider("Day", 1, 31)
       hour = st.slider("Hour", 0, 23)
       minute = st.slider("Minute", 0, 59)

    with colE2:
       temp = st.number_input("Temperature")
       st.markdown("<br>", unsafe_allow_html=True)

       dayofweek = st.selectbox(
    "Day of Week",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

       day_map = {
    "Monday":0, "Tuesday":1, "Wednesday":2,
    "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6
}

       dayofweek = day_map[dayofweek]
       

    isweekend_text = st.selectbox("Is Weekend?", ["No", "Yes"])
    isweekend = 1 if isweekend_text == "Yes" else 0

    if st.button("Predict Energy"):
        pred = model.predict([[month,day,hour, temp , dayofweek, minute, isweekend]])
        st.markdown(f"""
<div style='background-color:#161b22;padding:15px;border-radius:10px'>
<h3 style='color:#58a6ff;'>⚡Energy Consumed </h3>
<p style='font-size:20px'>{pred[0]:.2f}Kwh</p>
</div>
""", unsafe_allow_html=True)


# TRAFFIC PREDICTION
if option == "Traffic Congestion":
    st.header("🚦 Traffic Congestion Prediction")

    model = joblib.load("models/Traffic_Congestion.pkl")

    colT1, colT2 = st.columns(2)

    with colT1:
       vehicle_count = st.number_input("Vehicle Count", min_value=0)
       avg_speed = st.number_input("Average Speed (km/h)", min_value=0)

    with colT2:
       occupancy = st.number_input("Road Occupancy (%)", min_value=0)
       hour = st.slider("Hour of Day", 0, 23)

    def get_traffic_level(volume):
       if volume > 400:
        return "🔴 High Traffic"
       elif volume > 150:
        return "🟡 Medium Traffic"
       else:
        return "🟢 Low Traffic"

    if st.button("Predict Traffic"):

       input_data = np.array([[vehicle_count, avg_speed, occupancy, hour]])

       predicted_volume = model.predict(input_data)[0]
       traffic_level = get_traffic_level(predicted_volume)

       st.markdown(f"""
        <div style='background-color:#161b22;padding:20px;border-radius:12px'>
        <h3 style='color:#58a6ff;'>🚦 Traffic Prediction Result</h3>
        <p style='font-size:20px;'>Traffic Volume: <b>{predicted_volume:.2f}</b></p>
        <p style='font-size:18px;'>Traffic Level: <b>{traffic_level}</b></p>
        </div>
    """, unsafe_allow_html=True)



# AIR QUALITY INDEX PREDICTION
if option == "Air Quality Level":
    st.header("🌫️ Air Quality Level Prediction")

    model = joblib.load("models/air_model.pkl")

    col1, col2 = st.columns(2)

    with col1:
       pm25 = st.number_input("PM2.5")
       pm10 = st.number_input("PM10")
       no2 = st.number_input("NO2")

    with col2:
       co = st.number_input("CO")
       temp = st.number_input("Temperature")
       hum = st.number_input("Humidity")
    st.markdown("<br>", unsafe_allow_html=True)

    center_col1, center_col2, center_col3 = st.columns([1,1,1])

    with center_col2:
     predict_clicked = st.button("Predict AQI")

# RESULT
    if predict_clicked:
        pred = model.predict([[pm25, pm10, no2,co,temp,hum]])
        aqi=pred[0]
        if aqi <= 50:
            status = "Good 😊"
        elif aqi <= 100:
            status = "Satisfactory 🙂"
        elif aqi <= 200:
            status = "Moderate 😐"
        elif aqi <= 300:
            status = "Poor 😷"
        elif aqi <= 400:
            status = "Very Poor 🤢"
        else:
            status = "Severe ☠️"

        st.markdown(f"""
<div style='background-color:#161b22;padding:20px;border-radius:12px'>
<h3 style='color:#58a6ff;'>🌫️ AQI Result</h3>
<p style='font-size:22px;'>AQI: <b>{aqi:.2f}</b></p>
<p style='font-size:18px;'>Air Quality: <b>{status}</b></p>
</div>
""", unsafe_allow_html=True)


# CRIME HOTSPOT DETECTION
if option == "Crime Hotspots":
    st.header("🚓 Crime Hotspots Detection")

    import pandas as pd
    import folium
    import matplotlib.pyplot as plt
    from scipy.spatial.distance import cdist
    from sklearn.cluster import KMeans
    from folium.plugins import HeatMap

    # =========================
    # LOAD DATA
    # =========================
    df = pd.read_csv("data/india_crime_data.csv")

    # =========================
    # MAPPING (NO API)
    # =========================
    city_map = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Bangalore": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639)
    }

    # UI
    colC1, colC2 = st.columns(2)

    with colC1:
        location_input = st.selectbox("Select Location", list(city_map.keys()))

    with colC2:
        radius = st.slider("Select Radius", 0.01, 0.5, 0.1)

    # BUTTON CENTER
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        detect_clicked = st.button("🔥 Detect Hotspots")

    if detect_clicked:

        # =========================
        # GET LAT/LON
        # =========================
        user_lat, user_lon = city_map[location_input]

        st.success(f"📍 {location_input}: {user_lat}, {user_lon}")

        # =========================
        # FILTER NEARBY
        # =========================
        coords = df[["latitude", "longitude"]].values
        user_point = [[user_lat, user_lon]]

        distances = cdist(user_point, coords)
        df["distance"] = distances[0]

        nearby = df[df["distance"] < radius].copy()

        if len(nearby) == 0:
            st.warning("⚠️ No crime data found. Increase radius.")
        else:
            # =========================
            # KMEANS
            # =========================
            kmeans = KMeans(n_clusters=3, random_state=42)
            nearby["cluster"] = kmeans.fit_predict(
                nearby[["latitude", "longitude"]]
            )

            centers = kmeans.cluster_centers_

            # =========================
            # MAP
            # =========================
            m = folium.Map()

            m.fit_bounds([
                [nearby["latitude"].min(), nearby["longitude"].min()],
                [nearby["latitude"].max(), nearby["longitude"].max()]
            ])

            # Heatmap
            heat_data = nearby[["latitude", "longitude"]].values.tolist()
            HeatMap(heat_data).add_to(m)

            # Hotspots
            for center in centers:
                folium.Marker(
                    location=[center[0], center[1]],
                    icon=folium.Icon(color="red", icon="fire")
                ).add_to(m)

            st.markdown("### 🗺️ Crime Hotspot Map")
            st.components.v1.html(m._repr_html_(), height=500)

            # =========================
            # SCATTER PLOT
            # =========================
            st.markdown("### 📊 Scatter Analysis")

            fig, ax = plt.subplots()

            colors = ["blue", "green", "orange"]

            for i in range(3):
                cluster_data = nearby[nearby["cluster"] == i]

                ax.scatter(
                    cluster_data["longitude"],
                    cluster_data["latitude"],
                    color=colors[i],
                    label=f"Cluster {i}",
                    s=25
                )

            # 🔴 RED CROSS
            ax.scatter(
                centers[:,1],
                centers[:,0],
                color="red",
                marker="X",
                s=200,
                edgecolors="black",
                label="Hotspots"
            )

            ax.set_title("Crime Hotspot Scatter Plot")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            ax.legend()

            st.pyplot(fig)

            # =========================
            # RISK LEVEL (BONUS)
            # =========================
            if len(nearby) > 100:
                st.error("🔴 High Crime Area")
            elif len(nearby) > 50:
                st.warning("🟡 Medium Crime Area")
            else:
                st.success("🟢 Low Crime Area")

if option == "Waste Collection Route":
    st.header("🗑️ Waste Collection Route Optimization")

    import pandas as pd
    import folium
    from scipy.spatial.distance import cdist

    # -------------------------
    # LOAD DATA
    # -------------------------
    df = pd.read_csv("data/waste_data.csv")

    # -------------------------
    # FILTER HIGH BINS
    # -------------------------
    high_bins = df[df["fill_level"] > 70].copy()

    # -------------------------
    # MAPPING (FIXED LOCATIONS)
    # -------------------------
    area_map = {
        "Connaught Place": (28.6315, 77.2167),
        "Rohini": (28.7495, 77.0565),
        "Dwarka": (28.5921, 77.0460),
        "Saket": (28.5245, 77.2066),
        "Karol Bagh": (28.6519, 77.1909)
    }

    # -------------------------
    # DUMP LOCATION
    # -------------------------
    DUMP_LOCATION = (28.7041, 77.1025)

    # -------------------------
    # UI
    # -------------------------
    col1, col2 = st.columns(2)

    with col1:
        pickup_area = st.selectbox("Select Pickup Area", list(area_map.keys()))

    with col2:
        num_points = st.slider("Number of Bins", 5, 50, 20)

    # Center button
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        run_clicked = st.button("🚛 Optimize Route")

    if run_clicked:

        pickup_point = area_map[pickup_area]

        # Select bins
        points = high_bins[["latitude", "longitude"]].values[:num_points]

        # -------------------------
        # ROUTE (PICKUP → BINS → DUMP)
        # -------------------------
        route = [pickup_point]
        visited = set()
        points_list = list(points)

        for _ in range(len(points_list)):
            last = route[-1]

            distances = cdist([last], points_list)[0]

            for i in visited:
                distances[i] = float('inf')

            next_index = distances.argmin()

            route.append(points_list[next_index])
            visited.add(next_index)

        # Add dump at end
        route.append(DUMP_LOCATION)

        # -------------------------
        # MAP
        # -------------------------
        m = folium.Map(location=pickup_point, zoom_start=11)

        # Route line
        folium.PolyLine(route, color="blue", weight=4).add_to(m)

        # Bins
        for p in points:
            folium.CircleMarker(
                location=p,
                radius=3,
                color="red",
                fill=True
            ).add_to(m)

        # Pickup (START)
        folium.Marker(
            location=pickup_point,
            tooltip="Pickup Start",
            icon=folium.Icon(color="green")
        ).add_to(m)

        # Dump (END)
        folium.Marker(
            location=DUMP_LOCATION,
            tooltip="Dump Site",
            icon=folium.Icon(color="black")
        ).add_to(m)

        # Display map
        st.markdown("### 🗺️ Optimized Route")
        st.components.v1.html(m._repr_html_(), height=500)

        # -------------------------
        # INFO
        # -------------------------
        st.success(f"Pickup: {pickup_area}")
        st.info(f"Bins Covered: {len(points)}")