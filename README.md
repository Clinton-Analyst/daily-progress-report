# Daily Site Progress Report — Dashboard

> A dual-module Streamlit dashboard for construction site management — combining daily progress tracking with safety and incident reporting in one deployable web app.

---

## Overview

Construction sites generate two critical streams of daily data: work progress and safety incidents. Managing both through paper logs or scattered spreadsheets creates blind spots that delay decisions and put projects at risk. This dashboard centralises both into a single, structured interface — giving site managers, safety officers, and project leads a live view of what is happening on site, every day.

The app runs two independent modules accessible from the sidebar: a **Daily Progress Report (DPR)** for tracking crew, work completion, and equipment, and a **Safety & Incident Report** for monitoring PPE compliance, incident types, and severity across floors and trades.

---

## Features

### Daily Progress Report (DPR)

| Feature | Description |
|---|---|
| **KPI cards** | Average crew count, average work completion (%), and total equipment hours |
| **Work completion trend** | Interactive Plotly line chart tracking `work_completed_%` over time |
| **Crew count by weather** | Bar chart showing daily crew count coloured by weather impact level |
| **Live report submission** | Form to submit date, crew count, work %, equipment hours, weather impact, and notes |
| **Persistent CSV storage** | Submitted records are appended to `daily_progress.csv` and persisted between sessions |
| **Dataset viewer** | Full dataframe displayed below the form after each update |

### Safety & Incident Report

| Feature | Description |
|---|---|
| **KPI cards** | Total incidents, PPE non-compliance count, and high severity incident count |
| **Incident heatmap** | Seaborn heatmap of incident counts by floor and trade — pinpoints high-risk zones |
| **Incidents by type & severity** | Grouped Plotly bar chart breaking down incident types across severity levels |
| **PPE compliance pie chart** | Plotly pie showing the ratio of compliant vs non-compliant records |
| **Live incident submission** | Form to log incident type, floor, trade, severity, and PPE compliance |
| **Persistent CSV storage** | New incidents appended to `safety_incidents.csv` on every submission |
| **Dataset viewer** | Full safety dataset displayed after each submission |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| `Python 3.8+` | Core language |
| `Streamlit` | Web app framework, UI components, and form handling |
| `Pandas` | Data loading, filtering, and aggregation |
| `Plotly Express` | Interactive line, bar, and pie charts |
| `Seaborn` | Incident heatmap rendering |
| `Matplotlib` | Figure backend for Seaborn charts |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/site-progress-dashboard.git
cd site-progress-dashboard
```

### 2. Install dependencies

```bash
pip install streamlit pandas plotly seaborn matplotlib
```

### 3. Prepare your data files

The app expects two CSV files in the root directory:

```
daily_progress.csv
safety_incidents.csv
```

See the **CSV Format** section below for required column names. If these files do not exist, create them with the correct headers before running.

### 4. Run the dashboard

```bash
streamlit run app.py
```

Opens in your browser at `http://localhost:8501`.

---

## CSV Format

### `daily_progress.csv`

Required columns:

| Column | Type | Description |
|---|---|---|
| `date` | date | Date of the report (e.g. `2026-01-15`) |
| `crew_count` | integer | Number of workers on site that day |
| `work_completed_%` | float | Percentage of work completed (0–100) |
| `equipment_hours` | float | Total equipment operating hours |
| `weather_impact` | string | Weather severity — `Low`, `Medium`, or `High` |
| `notes` | string | Free-text site notes (optional) |

**Example:**

```
date,crew_count,work_completed_%,equipment_hours,weather_impact,notes
2026-01-01,12,45.5,8.0,Low,Foundation work started
2026-01-02,10,52.0,6.5,Medium,Light rain in afternoon
```

---

### `safety_incidents.csv`

Required columns:

| Column | Type | Description |
|---|---|---|
| `date` | date | Date of the incident |
| `incident_type` | string | `Near-Miss`, `PPE Violation`, `First Aid`, `Property Damage`, `Other` |
| `location_floor` | string | Floor where incident occurred (e.g. `Floor 1`) |
| `trade` | string | `Electrical`, `Masonry`, `Steel`, `Carpentry`, `Plumbing`, `Others` |
| `severity` | string | `High`, `Medium`, or `Low` |
| `ppe_compliant` | string | `Yes` or `No` |

**Example:**

```
date,incident_type,location_floor,trade,severity,ppe_compliant
2026-01-03,Near-Miss,Floor 2,Electrical,Medium,Yes
2026-01-04,PPE Violation,Floor 1,Masonry,Low,No
```

---

## Project Structure

```
site-progress-dashboard/
│
├── app.py                   # Main Streamlit application
├── daily_progress.csv       # DPR data store (auto-updated on submission)
├── safety_incidents.csv     # Safety incident data store (auto-updated on submission)
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## Requirements File

Create a `requirements.txt` with the following:

```
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.14.0
seaborn>=0.12.0
matplotlib>=3.6.0
```

---

## Navigation

The sidebar controls all navigation and filtering:

| Control | Function |
|---|---|
| **Navigate** radio | Switch between DPR and Safety modules |
| **Date Range** picker | Global date filter applied across the selected period |

> **Note:** The date filter is wired to the sidebar but not yet connected to the chart and KPI logic. See Known Limitations below.

---

## Use Cases

- **Site managers** submitting and reviewing daily crew and progress reports without paper forms
- **Safety officers** logging and monitoring incidents by floor, trade, and severity in real time
- **Project directors** reviewing weekly trends in work completion and safety compliance
- **Construction companies** replacing manual spreadsheet reporting with a structured digital workflow

## Roadmap

- [ ] Connect date range filter to KPI cards and charts
- [ ] Add monthly and weekly trend views for safety incidents
- [ ] Integrate a database backend (SQLite or PostgreSQL) to replace CSV storage
- [ ] Add CSV and PDF export for both modules
- [ ] Implement user authentication for site-specific access control



*Built with Python · Streamlit · Pandas · Plotly · Seaborn · Matplotlib*