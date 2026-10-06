# Leadership Open Door Dashboard

This project is a Streamlit dashboard for tracking Leadership Open Door session attendance.

## Features
- Executive-friendly KPI cards
- Monthly attendance trend view
- Department breakdown
- Detailed attendance table
- Easy to extend for real Excel upload later

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes
- Current version uses mock data for quick dashboard validation.
- Replace mock data with an Excel import or API feed when ready.
