# AI Smart Medicine Storage Guardian
Student proof-of-concept for temperature-trend monitoring and explainable alerts in medicine-storage environments.

## Features
- Upload CSV readings or view demo data
- Configurable demo temperature range
- Out-of-range alerts
- Simple trend/anomaly flags
- Timestamped event history and CSV export

## Run
1. Install Python 3.10+
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

CSV columns required: `timestamp,temperature_c`. Optional: `humidity_pct,door_open,power_status`.

## AI status
This starter uses transparent threshold and trend heuristics to demonstrate the workflow. It does **not** include a trained predictive model. A trained model is a future extension and must be evaluated on representative labelled data.

## Safety
Not validated for clinical or commercial use. Do not use it to decide whether real medicines are safe, spoiled, or usable. Storage limits must come from the exact product's manufacturer guidance, and excursions must be reviewed by responsible staff.
