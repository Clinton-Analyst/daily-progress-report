import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title = "Daily Site Progress Report", layout = "wide")
st.title("Daily Progress Report - Dashboard")

# Load Dataset
df = pd.read_csv("daily_progress.csv")
#df.head()
#print(df)

# Daily Progress Report--DPR
st.header("Daily Progress Report(DPR)")

# KPI Cards
col1, col2,col3 = st.columns(3)
col1.metric("Avg Crew Count", f"{df['crew_count'].mean():.0f}")
col2.metric("Avg Work Completed", f"{df['work_completed_%'].mean():.1f}")
col3.metric("Total Equipment Hours", df['equipment_hours'].sum())

# Line Chart-- Work Progress over time
fig = px.line(df, x='date', y='work_completed_%', title='Work Completion Over Time',)
st.plotly_chart(fig, use_container_width=True)

# Bar chart - Crew count
fig2=px.bar(df, x='date', y='crew_count', title='Daily Crew Count', color='weather_impact')
st.plotly_chart(fig2, use_container_width=True)

#Streamlit form that lets users submit new daily reports
st.subheader("Submit Today's Report") 
with st.form("dpr_form", clear_on_submit=True):
    date=st.date_input("Date")
    crew=st.number_input("Crew Count", min_value=0)
    work_pct=st.slider("Work Completed (%)", 0, 100)
    equip_hours=st.number_input("Equipment Hours")
    weather=st.selectbox("Weather Impact", ["Low", "Medium", "High"])
    notes=st.text_area('Notes')
    submitted=st.form_submit_button("Submit")


    if submitted:
        # Append to CSV
        new_row={
            "date": date, 
            'crew_count': crew, 
            'work_completed_%': work_pct, 
            'equipment_hours': equip_hours, 
            'weather_impact': weather, 
            'notes': notes, 
        }
        # 2. Update Session State (The "Live" data)
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        
        # 3. Save to CSV (Permanent storage)
        df.to_csv("daily_progress.csv", index=False)
        
        st.success("Report Submitted Successfully!!")

 #Display the updated dataframe
st.write("### Current Dataset")
st.dataframe(df)

# Safety and Incident report
st.header("Safety & Incident Report")

df_safety=pd.read_csv("safety_incidents.csv")

# Display Safety data
st.write("Safety Data")
st.dataframe(df_safety)

# Summary KPIs
col1, col2, col3=st.columns(3)
col1.metric("Total incidents", len(df_safety))
col2.metric("PPE Non-Compliance", len(df_safety[df_safety['ppe_compliant']=='No']))
col3.metric("High Severity", len(df_safety[df_safety['severity']=='High']))

# Heatmap Floor vs Trade incident count
heatmap_data=df_safety.pivot_table(
    index='location_floor',
    columns="trade",
    values="incident_type",
    aggfunc="count",
    fill_value=0
)

fig, ax=plt.subplots(figsize=(10,5))
sns.heatmap(heatmap_data, annot=True, fmt='d', ax=ax)
ax.set_title("Incident Heatmap: Floor vs Trade")
st.pyplot(fig)

# Bar: Incident by Severity
fig3=px.bar(df_safety, x='incident_type', color='severity', title='Incidents by Type & Severity', barmode='group')
st.plotly_chart(fig3, use_container_width=True)

# PPE Compliance Pie
ppe_counts = df_safety['ppe_compliant'].value_counts().reset_index()
fig4 = px.pie(ppe_counts, names='ppe_compliant', values='count',
title='PPE Compliance Rate',
color_discrete_sequence=['#EF553B', '#00CC96'])
st.plotly_chart(fig4, use_container_width=True)
