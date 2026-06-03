import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"

st.title("🛍️ Store Intelligence Dashboard")

# -----------------------------
# Load Data
# -----------------------------

try:
    events = requests.get(
        f"{API_URL}/events"
    ).json()

    footfall = requests.get(
        f"{API_URL}/analytics/footfall"
    ).json()

    zones = requests.get(
        f"{API_URL}/analytics/zones"
    ).json()

    alerts = requests.get(
        f"{API_URL}/alerts"
    ).json()

except Exception as e:

    st.error(f"API Connection Error: {e}")
    st.stop()

# -----------------------------
# KPI Cards
# -----------------------------

df = pd.DataFrame(events)

total_events = len(df)

entry_count = len(
    df[df["event_type"] == "entry"]
) if not df.empty else 0

queue_alerts = len(alerts)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Footfall",
    footfall.get("footfall", 0)
)

c2.metric(
    "Total Events",
    total_events
)

c3.metric(
    "Queue Alerts",
    queue_alerts
)

st.divider()

# -----------------------------
# Zone Analytics
# -----------------------------

st.subheader("📊 Zone Analytics")

if zones:

    zone_df = pd.DataFrame(
        list(zones.items()),
        columns=["Zone", "Visits"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.bar_chart(
            zone_df.set_index("Zone")
        )

    with col2:

        fig = px.pie(
            zone_df,
            names="Zone",
            values="Visits",
            title="Zone Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info("No zone analytics available")

st.divider()

# -----------------------------
# Queue Alerts
# -----------------------------

st.subheader("🚨 Queue Alerts")

if alerts:

    st.dataframe(
        pd.DataFrame(alerts).fillna("-"),
        use_container_width=True
    )

else:

    st.success("No queue alerts detected")

st.divider()

# -----------------------------
# Recent Events
# -----------------------------

st.subheader("📋 Recent Events")

if not df.empty:

    st.dataframe(
        df.fillna("-"),
        use_container_width=True
    )

else:

    st.info("No events available")

# -----------------------------
# Event Type Breakdown
# -----------------------------

st.subheader("📈 Event Breakdown")

if not df.empty:

    event_counts = (
        df["event_type"]
        .value_counts()
        .reset_index()
    )

    event_counts.columns = [
        "Event Type",
        "Count"
    ]

    fig = px.bar(
        event_counts,
        x="Event Type",
        y="Count",
        title="Event Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )