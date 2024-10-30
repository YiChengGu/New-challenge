import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import ssl
import certifi
import urllib.request
from io import BytesIO

st.title("Data Dashboard")
uploaded_file = st.file_uploader("Choose an excel file", type=["xlsx", "xls"])
if uploaded_file is not None:
    st.write("File uploaded")
    df = pd.read_excel(uploaded_file)
    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("filter data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot data")
    x_column = st.selectbox("select x-axis column", columns)
    y_column = st.selectbox("select y-axis column", columns)


    if st.button("Generate Plot"):
        st.bar_chart(filtered_df.set_index(x_column)[y_column])
else:
    st.write("waiting on file upload")

import streamlit as st
import pandas as pd

st.title("Data related jobs prospect")

DATA_URL = ('https://github.com/Saitetha/DATA-SCIENCE-JOBS-SALARIES/raw/main/Data%20science%20Salaries%20raw%20data.xlsx')

@st.cache_data
def load_data(nrows):
    # Load the data from the provided URL
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    response = urllib.request.urlopen(DATA_URL, context=ssl_context)
    excel_data = BytesIO(response.read())
    data = pd.read_excel(excel_data, nrows=nrows, engine='openpyxl')
    
    # Rename columns to lowercase
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    
    # Ensure work_year stays as an integer or string (no datetime conversion)
    data['work_year'] = data['work_year'].astype(str)  # or int if needed

    return data

# Load the data and store it in a variable
data = load_data(10000)  # Adjust the number of rows as needed

# Display the raw data
st.subheader('Raw data')
st.write(data)

st.subheader("Job title vs salary")

job_titles = data['job_title'].unique()
selected_job_title = st.selectbox("Select a Job Title", job_titles)

# Filter data based on selected job title
filtered_data = data[data['job_title'] == selected_job_title]

# Create histogram plot for salary
fig, ax = plt.subplots()
ax.hist(filtered_data['salary_in_usd'], bins=20, edgecolor='black')
ax.set_xlabel('Salary in USD')
ax.set_ylabel('Frequency')
ax.set_title(f'Salary Distribution for {selected_job_title}')

# Display the plot in Streamlit
st.pyplot(fig)

st.subheader("Company Location vs Salary (USD)")

# Group data by company location and calculate the mean salary for each location
avg_salary_by_location = data.groupby('company_location')['salary_in_usd'].mean().reset_index()

# Create a bar plot for average salary by location
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(avg_salary_by_location['company_location'], avg_salary_by_location['salary_in_usd'], color='skyblue')
ax.set_xlabel('Company Location')
ax.set_ylabel('Average Salary (USD)')
ax.set_title('Average Salary by Company Location')
plt.xticks(rotation=90)  # Rotate the x-axis labels for better readability

# Display the plot in Streamlit
st.pyplot(fig)

import plotly.express as px

fig = px.scatter(
    data, 
    x='work_year', 
    y='salary_in_usd', 
    color='job_title', 
    title='Work Year vs Salary (USD) by Job Title',
    size_max=10, 
    opacity=0.7
)

st.plotly_chart(fig)
