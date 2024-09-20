import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('c:\\Users\\Lenovo\\OneDrive - American University of Beirut\\Desktop\\MSBA 325\\Assignment\\Assignment 1\\health_resouces.csv')

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Description", "Visualizations"])

if page == "Description":
  st.markdown("<h1 style='text-align: center;'>Healthcare Resources</h1>", unsafe_allow_html=True)
    
  st.write("""This page presents insights into data about healthcare resources. We will explore the availability and shortage of care centers, pharmacies, 
              and other healthcare facilities through different regions with the help of interactive visuals.""")

  st.write("""This dataset provides comprehensive information on the availability of medical resources across various towns in Lebanon. It includes data on the existence 
              and types of healthcare facilities such as pharmacies, hospitals, clinics, medical centers, and labs.""")

  st.write("""Additionally, the dataset tracks whether nearby care centers and special needs centers exist in each town. The data also provides insights 
              into the percentage of towns with and without individuals with special needs.""")

  st.write("""The resource is part of an open data initiative aimed at improving public accessibility to healthcare resource distribution across Lebanon.""")

  st.subheader("Preview of the First 5 Rows")
  st.dataframe(df.head())

  st.subheader("Description of the Columns")
  st.write(df.columns)
  st.write("""
  - **Type and size of medical resources** - Pharmacies, Medical Centers, Hospitals, Clinics, and Labs and Radiology: 
    5 different columns indicating the number and type of each medical resource available in each town.

  - **Total number of care centers, first aid centers**: 
    2 columns showing the total count of care centers and first aid centers in the town.

  - **Existence of nearby care centers - exists and not exists**: 
    Shows whether nearby care centers exist (1 for yes, 0 for no).

  - **Existence of health resources - exists and not exists**: 
    Indicates if general health resources exist in the town.

  - **Town**: 
    The name of the town being described.

  - **refArea**: 
    Refers to the geographical area or governorate where the town is located.

  - **Observation URI**: 
    A link to the URI containing detailed observations of the town’s health resources.

  - **Percentage of towns with special needs individuals - With and Without special needs**: 
    2 columns showing the percentage of the population with and without special needs.

  - **Existence of special needs care centers - exists and not exists**: 
    Indicates whether care centers for individuals with special needs exist (1 for yes, 0 for no).

  The column **refArea** was engineered to contain only the name of the area without the entire link for easier visualization.
  """)

elif page == "Visualizations":
  st.markdown("<h1 style='text-align: center;'>Healthcare Resources Visualization</h1>", unsafe_allow_html=True)
    
  df['refArea'] = df['refArea'].apply(lambda x: x.split('/')[-1])

  # Figure 1
  grp_data = df.groupby('refArea')[['Type and size of medical resources - Hospitals', 
                                     'Type and size of medical resources - Clinics', 
                                     'Type and size of medical resources - Labs and Radiology ']].sum().reset_index()

  resource_types = ['Type and size of medical resources - Hospitals', 
                    'Type and size of medical resources - Clinics', 
                    'Type and size of medical resources - Labs and Radiology ']

  grp_data.fillna(0, inplace=True)

  st.title("Medical Resources by Region")

  selected_resources = st.multiselect('Select Medical Resources to Display', resource_types, default=resource_types)

  if selected_resources:
      fig1 = px.line(grp_data, 
                     x='refArea', 
                     y=selected_resources,
                     labels={'refArea': 'Region', 'value': 'Number of Resources'},
                     title="Availability of Medical Resources by Region",
                     markers=True)

      fig1.update_layout(xaxis_tickangle=45)

      st.plotly_chart(fig1)
  else:
      st.warning("Please select at least one medical resource to display.")

  # Figure 2
  df['Percentage of towns with special needs indiciduals - With special needs'] = pd.to_numeric(df['Percentage of towns with special needs indiciduals - With special needs'], errors='coerce')
  df['Percentage of towns with special needs indiciduals - Without special needs'] = pd.to_numeric(df['Percentage of towns with special needs indiciduals - Without special needs'], errors='coerce')
  df['Existence of special needs care centers - exists'] = pd.to_numeric(df['Existence of special needs care centers - exists'], errors='coerce')
  df['Existence of special needs care centers - does not exist'] = pd.to_numeric(df['Existence of special needs care centers - does not exist'], errors='coerce')

  chart_type = st.selectbox("Choose the pie chart to display", 
                            ["Percentage of towns with special needs individuals", 
                             "Existence of special needs care centers"])

  if chart_type == "Percentage of towns with special needs individuals":
      labels = ['With Special Needs', 'Without Special Needs']
      values = [df['Percentage of towns with special needs indiciduals - With special needs'].sum(),
                df['Percentage of towns with special needs indiciduals - Without special needs'].sum()]

      fig2 = px.pie(values=values, names=labels, title="Percentage of Towns with Special Needs Individuals",
                     color_discrete_sequence=['#FFFF00', '#FFA500'])
      st.plotly_chart(fig2)

  elif chart_type == "Existence of special needs care centers":
      labels = ['Care Centers Exist', 'Care Centers Do Not Exist']
      values = [df['Existence of special needs care centers - exists'].sum(),
                df['Existence of special needs care centers - does not exist'].sum()]

      fig2 = px.pie(values=values, names=labels, title="Existence of Special Needs Care Centers",
                    color_discrete_sequence=['#FFB6C1', '#90EE90'])
      st.plotly_chart(fig2)