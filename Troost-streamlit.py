#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import streamlit as st


# In[5]:


def process_file(uploaded_file, start_date, end_date):
    if uploaded_file is not None:
        # Read the uploaded file into a DataFrame
        data = pd.read_table(uploaded_file)

        # Perform your data processing
        data['Datum'] = pd.to_datetime(data['Datum'], format='%d-%m-%Y %H:%M:%S')
        data['Bedrag'] = data['Bedrag'].str.replace(',', '.')
        data['Bedrag'] = pd.to_numeric(data['Bedrag'], errors='coerce')

        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        for day in date_range:
            start_datetime = day + pd.DateOffset(hours=6)
            end_datetime = day + pd.DateOffset(days=1, hours=6)

            dag = data[data['Datum'].between(start_datetime, end_datetime)]

            failures = dag[dag['Status'] == 'FAILURE']
            dagelijkse_som = dag['Bedrag'].sum()
            failures_totaal = failures['Bedrag'].sum()
            dagelijks_totaal = dagelijkse_som - failures_totaal

            st.write(f"Total for {day.date()}: {dagelijkse_som} , failures: {failures_totaal} , pintotaal: {dagelijks_totaal}")

def main():
    st.title("File Upload and Processing App")

    # Display a file uploader widget
    uploaded_file = st.file_uploader("Choose a file", type=["csv"])

    # Display date input widgets for start and end dates
    start_date = st.date_input("Select start date", pd.to_datetime('2023-10-01'))
    end_date = st.date_input("Select end date", pd.to_datetime('2023-11-01'))

    # Check if a file is uploaded
    if uploaded_file is not None:
        st.success("File uploaded successfully!")

        # Display file details
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": f"{uploaded_file.size} bytes"}
        st.write(file_details)

        # Process the uploaded file with dynamic start and end dates
        process_file(uploaded_file, start_date, end_date)

if __name__ == "__main__":
    main()


# In[ ]:




