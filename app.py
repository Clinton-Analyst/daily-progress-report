import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date


st.set_page_config(page_title = "Daily Site Progress Report", layout = "wide")
st.title("Daily Progress Report - Dashboard")


# sidebar navigation to switch between modules
st.sidebar.title("Site Analytics")
page = st.sidebar.radio("Navigate", ["DPR", "Safety", "QA/QC"])

st.sidebar.markdown("---")
st.sidebar.header("Global Filters")

# Add date inputs to the sidebar
# This returns a tuple (start_date, end_date) if you use a range
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(date(2026, 1, 1), date(2026, 3, 17)),
    help="Select the start and end date for filtering"
)


# DPR-Navigation 
if page == "DPR":
    #st.title("Daily Progress Report - Dashboard")

    # Load Dataset
    df = pd.read_csv("daily_progress.csv")
    #df.head()
    #print(df)
    # st.write(f"Showing data from **{date_range[0]}** to **{date_range[1]}**")
    # Your filtering logic here: 
    # df_filtered = df[(df['date'] >= date_range[0]) & (df['date'] <= date_range[1])]



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
    st.subheader("Submit Today's Daily Progress Report") 
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



# Safety and Incident report-Navigation
elif page == "Safety":
    st.title("Safety & Incident Report")


    st.header("Key Performance Indicators (KPI)")

    df_safety=pd.read_csv("safety_incidents.csv")
    #df_safety['date'] = pd.to_datetime(df_safety['date']).dt.strftime("%Y-%m-%d")

    # Display Safety data
    #st.write("Safety Data")
    #st.dataframe(df_safety)

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

    #Streamlit form that lets users submit new daily reports
    st.subheader("Submit Today's Safety Incidents Report") 
    with st.form("safety_form", clear_on_submit=True):
        date=st.date_input("Date")
        #crew=st.number_input("Crew Count", min_value=0)
        #work_pct=st.slider("Work Completed (%)", 0, 100)
        #equip_hours=st.number_input("Equipment Hours")
        incident_type=st.selectbox("Incident Type", ["Near-Miss", "PPE Violation", "First Aid", "Property Damage", "Other"])
        location_floor=st.selectbox("Location Floor", ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", "Others"])
        trade=st.selectbox("Trade", ["Electrical", "Masonry", "Steel", "Carpentry", "Plumbing", "Others"])
        severity=st.selectbox("Severity", ["High", "Medium", "Low"])
        ppe_compliant=st.selectbox("PPE Compliant", ["Yes", "No"])

        #notes=st.text_area('Notes')
        submitted=st.form_submit_button("Submit")


    if submitted:
        # Append to CSV
        new_row={
            "date": date, 
            'incident_type': incident_type, 
            'location_floor': location_floor, 
            'trade': trade, 
            'severity': severity, 
            'ppe_compliant': ppe_compliant, 
        }
        # 2. Update Session State (The "Live" data)
        new_df = pd.DataFrame([new_row])
        df_safety = pd.concat([df_safety, new_df], ignore_index=True)
        
        # 3. Save to CSV (Permanent storage)
        df_safety.to_csv("safety_incidents.csv", index=False)
        
        st.success("Report Submitted Successfully!!")

    #Display the updated dataframe
    st.write("### Current Dataset")
    st.dataframe(df_safety)

# Quality CONTROL-Navigation
#elif page == "QA/QC":
 #   st.title("Quality Control-QA/QC")
  #  df_qaqc=pd.read_csv("qaqc_punchlist.csv")

    # Display the qaqc data
   # st.write("qaqc data")
    #st.dataframe(df_qaqc)

    # Rework rate by subcontractor
    #rework = df_qaqc.groupby('subcontractor')['rework_required'].apply(
    #lambda x: (x == 'Yes').sum() / len(x) * 100
    #).reset_index()
    #rework.columns = ['subcontractor', 'rework_rate_%']
    #fig5 = px.bar(rework, x='subcontractor', y='rework_rate_%',
    #title='Rework Rate by Subcontractor (%)',
    #color='rework_rate_%',
    #color_continuous_scale='Reds')
    #st.plotly_chart(fig5, use_container_width=True)


    # Trend over time per subcontractor
    #df_qaqc['date'] = pd.to_datetime(df_qaqc['date'])
    #trend = df_qaqc[df_qaqc['rework_required'] == 'Yes'].groupby(
    #['date', 'subcontractor']
    #).size().reset_index(name='defect_count')
    #fig6 = px.line(trend, x='date', y='defect_count',
    #color='subcontractor',
    #title='Defect Trend Over Time by Subcontractor',
    #markers=True)
    #st.plotly_chart(fig6, use_container_width=True)


    # Pass/Fail rate
    #results = df_qaqc['inspection_result'].value_counts().reset_index()
    #fig7 = px.pie(results, names='inspection_result', values='count',
    #title='Inspection Pass/Fail Rate',
    #color_discrete_sequence=['#00CC96', '#EF553B'])
    #st.plotly_chart(fig7, use_container_width=True)


    # Flag high-risk subcontractors
    #st.subheader("High-Risk Subcontractors (Rework Rate > 70%)")
    #high_risk = rework[rework['rework_rate_%'] > 70]
    #if not high_risk.empty:
     #st.dataframe(high_risk.style.highlight_max(color='red'))
    #else:
     #   st.success("✅ No high-risk subcontractors currently!")


    #Streamlit form that lets users submit new daily reports
    #st.subheader("Submit Today's QAQC Incidents Report") 
    #with st.form("qaqc_form", clear_on_submit=True):
     #   date=st.date_input("Date")
        #crew=st.number_input("Crew Count", min_value=0)
        #work_pct=st.slider("Work Completed (%)", 0, 100)
        #equip_hours=st.number_input("Equipment Hours")
      #  subcontractor=st.selectbox("Subcontractor", ["ABC Plumbing", "XYZ Electric", "BuildRight Masonry", "SteelPro Inc", "Other"])
        #defect_type=st.selectbox("Location Floor", ["Floor 1", "Floor 2", "Floor 3", "Floor 4", "Floor 5", "Floor 6", "Others"])
        #trade=st.selectbox("Trade", ["Electrical", "Masonry", "Steel", "Carpentry", "Plumbing", "Others"])
       # rework_required=st.selectbox("Rework Required", ["Yes", "No"])
        #inspection_result=st.selectbox("Inspection Result", ["Pass", "Fail"])

        #defect_type=st.text_area('Defect Type')
        #submitted=st.form_submit_button("Submit")


    #if submitted:
        # Append to CSV
     #   new_row={
      #      "date": date, 
       #     'subcontractor': subcontractor, 
        #    'defect_type': defect_type, 
         #   'inspection_result': inspection_result, 
          #  'rework_required': rework_required,
        #}
        # 2. Update Session State (The "Live" data)
        #new_df = pd.DataFrame([new_row])
        #df_qaqc = pd.concat([df_qaqc, new_df], ignore_index=True)
        
        # 3. Save to CSV (Permanent storage)
        #df_qaqc.to_csv("qaqc_punchlist.csv", index=False)
        
        #st.success("Report Submitted Successfully!!")

    #Display the updated dataframe
    #st.write("### Current Dataset")
    #st.dataframe(df_qaqc)


