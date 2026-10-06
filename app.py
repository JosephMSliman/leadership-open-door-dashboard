import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Leadership Open Door Dashboard",
    page_icon="🏛️",
    layout="wide",
)

st.title("Leadership Open Door Dashboard")
st.caption("Monthly engagement overview for leadership sessions")

# Load sample data if present, otherwise use generated mock data
DATA_PATH = Path("data/attendance_data.csv")

if DATA_PATH.exists():
    df = pd.read_csv(DATA_PATH)
else:
    # Generate mock data for demonstration
    months = pd.date_range("2024-01-01", periods=12, freq="MS")
    records = []
    for i, month in enumerate(months):
        for j in range(1, 8):
            attendee_count = 14 + (i * 2) + j
            records.append({
                "session_date": month.strftime("%Y-%m-%d"),
                "session_name": f"Leadership Open Door {month.strftime('%b %Y')}",
                "attendees": attendee_count,
                "attendance_rate_pct": min(100, 65 + (j * 4) + (i * 3)),
                "unique_participants": max(10, attendee_count - 4),
                "department": ["Engineering", "Operations", "Finance", "People", "Product", "Marketing", "Sales"][j % 7],
                "category": "Monthly"
            })
    df = pd.DataFrame(records)
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

# Clean up date column
if "session_date" in df.columns:
    df["session_date"] = pd.to_datetime(df["session_date"])

# Sidebar filters
st.sidebar.header("Filters")
if "session_name" in df.columns:
    session_options = sorted(df["session_name"].dropna().unique().tolist())
    selected_session = st.sidebar.multiselect("Session", session_options, default=session_options)
    df_filter = df[df["session_name"].isin(selected_session)] if selected_session else df
else:
    df_filter = df.copy()

if "department" in df.columns:
    dept_options = sorted(df["department"].dropna().unique().tolist())
    selected_dept = st.sidebar.multiselect("Department", dept_options, default=dept_options)
    df_filter = df_filter[df_filter["department"].isin(selected_dept)] if selected_dept else df_filter

# KPI calculations
if df_filter.empty:
    st.warning("No data matches the current filters.")
    st.stop()

latest_session = df_filter.sort_values("session_date").iloc[-1]
previous_session = df_filter.sort_values("session_date").iloc[-2] if len(df_filter) > 1 else latest_session

current_attendees = float(latest_session.get("attendees", 0) or 0)
previous_attendees = float(previous_session.get("attendees", 0) or 0)
trend_attendees = ((current_attendees - previous_attendees) / previous_attendees * 100) if previous_attendees else 0

current_rate = float(latest_session.get("attendance_rate_pct", 0) or 0)

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Attendees", f"{int(current_attendees):,}", f"{trend_attendees:+.1f}% vs last session")
col2.metric("Attendance Rate", f"{current_rate:.1f}%", "Target: 80%+")
col3.metric("Unique Participants", f"{int(latest_session.get('unique_participants', current_attendees) or 0):,}", "Across this session")
col4.metric("Monthly Sessions", f"{len(df_filter):,}", "Current filtered view")

# Charts
chart_col1, chart_col2 = st.columns(2)

if {"session_date", "attendees"}.issubset(df_filter.columns):
    trend_df = df_filter.sort_values("session_date").copy()
    trend_df["month_label"] = trend_df["session_date"].dt.strftime("%b %Y")
    fig = px.line(
        trend_df,
        x="month_label",
        y="attendees",
        markers=True,
        title="Attendance Trend",
        color_discrete_sequence=["#2E5BFF"],
    )
    fig.update_layout(xaxis_title="Session", yaxis_title="Attendees", template="plotly_white")
    chart_col1.plotly_chart(fig, use_container_width=True)

if "department" in df_filter.columns and "attendees" in df_filter.columns:
    dept_df = df_filter.groupby("department", as_index=False)["attendees"].sum()
    dept_df = dept_df.sort_values("attendees", ascending=False)
    fig2 = px.bar(
        dept_df,
        x="department",
        y="attendees",
        title="Attendance by Department",
        color="department",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig2.update_layout(xaxis_title="Department", yaxis_title="Attendees", template="plotly_white", showlegend=False)
    chart_col2.plotly_chart(fig2, use_container_width=True)

# Detail tables
st.subheader("Session Detail")
show_columns = [
    col for col in ["session_name", "session_date", "attendees", "attendance_rate_pct", "unique_participants", "department"]
    if col in df_filter.columns
]
if show_columns:
    st.dataframe(df_filter[show_columns].sort_values("session_date", ascending=False), use_container_width=True)
else:
    st.dataframe(df_filter, use_container_width=True)

# Simple notes section
st.subheader("Leadership Notes")
notes = [
    "Attendance remains strongest in engineering and product roles.",
    "Monthly engagement is trending above the prior quarter baseline.",
    "Continue to support onboarding for new participants and leadership visibility."
]
for note in notes:
    st.write(f"• {note}")

# Footer
st.markdown("---")
st.caption("Prepared for leadership reviews and monthly executive updates.")








































































































































































































