import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Smart Medicine Storage Guardian", page_icon="🌡️", layout="wide")
st.title("🌡️ AI Smart Medicine Storage Guardian")
st.caption("Student proof-of-concept • not for real medicine safety decisions")
st.warning("Do not use this prototype to decide whether a real medicine is safe or spoiled. Confirm exact product storage guidance and refer excursions to responsible staff.")

with st.sidebar:
    st.header("Demo settings")
    low = st.number_input("Demo lower limit (°C)", value=2.0, step=0.5)
    high = st.number_input("Demo upper limit (°C)", value=8.0, step=0.5)
    st.caption("Example limits only; use manufacturer guidance for real products.")

up = st.file_uploader("Upload CSV: timestamp, temperature_c (optional humidity_pct)", type=["csv"])
if up:
    df = pd.read_csv(up)
else:
    rng = np.random.default_rng(7)
    n = 60
    t = pd.date_range("2026-10-22 08:00", periods=n, freq="min")
    temp = 4.5 + rng.normal(0, .18, n)
    temp[35:45] += np.linspace(0, 4.5, 10)
    temp[45:] += 4.5
    df = pd.DataFrame({"timestamp": t, "temperature_c": temp})

if not {"timestamp", "temperature_c"}.issubset(df.columns):
    st.error("CSV must contain timestamp and temperature_c columns.")
    st.stop()
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["temperature_c"] = pd.to_numeric(df["temperature_c"], errors="coerce")
df = df.dropna(subset=["timestamp", "temperature_c"]).sort_values("timestamp").reset_index(drop=True)
if df.empty:
    st.error("No valid readings found.")
    st.stop()

df["out_of_range"] = (df.temperature_c < low) | (df.temperature_c > high)
df["change_5"] = df.temperature_c.diff(5)
df["rapid_change"] = df.change_5.abs() >= 1.5
df["data_gap"] = df.timestamp.diff().dt.total_seconds().fillna(0) > 120
df["status"] = np.select(
    [df.out_of_range, df.rapid_change, df.data_gap],
    ["Outside configured range", "Unusual 5-reading change", "Possible data gap"],
    default="No flag from current checks"
)
a,b,c = st.columns(3)
a.metric("Latest temperature", f"{df.iloc[-1].temperature_c:.2f} °C")
b.metric("Out-of-range readings", int(df.out_of_range.sum()))
c.metric("Flagged readings", int((df.status != "No flag from current checks").sum()))

fig = px.line(df, x="timestamp", y="temperature_c", title="Temperature history", markers=True)
fig.add_hline(y=low, line_dash="dash", annotation_text="Demo lower limit")
fig.add_hline(y=high, line_dash="dash", annotation_text="Demo upper limit")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Explainable flags")
flags = df[df.status != "No flag from current checks"]
if flags.empty:
    st.success("No flags from these simple prototype checks.")
else:
    st.dataframe(flags[["timestamp","temperature_c","status"]], use_container_width=True, hide_index=True)

last = df.iloc[-1]
if last.out_of_range:
    st.error("Latest reading is outside the configured demo range. Verify sensor and storage conditions; follow the product-specific procedure.")
elif last.rapid_change:
    st.warning("Recent readings show an unusual change. Check sensor, door, and power status; this is not proof of a fault.")
else:
    st.info("Current checks did not flag the latest reading. This does not prove storage or medicine safety.")

st.download_button("Download reviewed readings CSV", df.to_csv(index=False).encode(), "storage_readings_review.csv", "text/csv")
st.caption("This starter uses transparent threshold/trend heuristics, not a trained AI model. Validate on labelled data before making performance claims.")
