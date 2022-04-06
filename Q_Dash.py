import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import plotly.express as px
import plotly.figure_factory as ff
import openpyxl
import calendar
from workalendar.europe import Germany
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import seaborn as sns
import streamlit as st


st.set_page_config(page_title="Quality", page_icon = ":bar_chart:", layout = "wide")

st.title("Quality-Dashboard")


#get data and transform for further evaluation
file = r"\\filemaster\DE_operations\3 Quality\OQC\OQC Report 2022\OQC 2022.xlsx"
def transformation():
    global data
    data = pd.read_excel(file)
    data["Projekt"] = data["Projekt"].str.strip()
    data.columns = data.columns.str.replace(' ', '')
#delete unnamed columns
    data = data[data.columns.drop(list(data.filter(regex='Unnamed')))]
#fill na with 0
    data.fillna(0, inplace = True)
#convert to numeric
    data["Partikel/Einschluss"] = pd.to_numeric(data["Partikel/Einschluss"], errors= "coerce")
    data["Mura"] = pd.to_numeric(data["Mura"], errors= "coerce")
    data["Projekt"] = data["Projekt"].replace(['AES Rechts'],'Wiko Rechts')

    data["Datum"] = pd.to_datetime(data["Datum"], format = "%YY-%m-%d")
    data[["KW", "Projekt", "Name"]] = data[["KW", "Projekt", "Name"]].astype(str)
    data[['KW', 'Week']] = data["KW"].str.split('W', 1, expand=True)
    data = data.drop(columns = ["KW"], axis = 1)
    data["Week"] = pd.to_numeric(data["Week"], errors = "coerce")
    change_column = data.pop("Week")
    data.insert(1, "Week", change_column)
    file_temp = r"C:\Users\daniel.hartmann\Python_Doks\dataframe_1.xlsx"
    data.to_excel(file_temp, index = False)

transformation()



#filter for first data_selection
st.sidebar.header("Please filter here:")
check = st.sidebar.checkbox("Select all")

if check:
    project = st.sidebar.multiselect("Choose the project:", options = data["Projekt"].unique(), default = data["Projekt"].unique())
    week = st.sidebar.multiselect("Choose the Week:", options = data["Week"].unique(), default = data["Week"].unique())
    data_selection = data.query("Projekt == @project & Week == @week")
else:
    project = st.sidebar.multiselect("Choose the project:", options = data["Projekt"].unique())
    week = st.sidebar.multiselect("Choose the Week:", options = data["Week"].unique())
    data_selection = data.query("Projekt == @project & Week == @week")

with st.expander("Raw Data from OQC Report"):
    st.write(data_selection)


st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


#subsets for charts
data_bar_input = data_selection[["Projekt", "Week", "Input"]]
data_line_trend = data_selection[["Projekt", "Week", "Input", "Gute", "Schlechte"]]

data_bar_grouped = data_bar_input.groupby(["Week"]).sum()
data_line_trend_grouped = data_line_trend.groupby(["Week"]).sum()
data_line_trend_grouped["Yield"] = data_line_trend_grouped["Gute"] / data_line_trend_grouped["Input"]*100
sums = data_line_trend[["Input", "Gute", "Schlechte"]].sum(axis = 0)
Total_Yield = int(sums["Gute"] / sums["Input"]*100)
percent_sign = "%"
Total_Yield_Displayed = str(Total_Yield) + percent_sign
#average change



data_per_project = data_selection.drop(["Input", "Gute", "Yield", "Schlechte"], axis = 1)

data_per_project = data_per_project.groupby(["Week"]).sum()

with st.expander("Total Data per selection"):
    col1, col2 = st.columns(2)

    with col1:
        st.header("Total Input on selection")
        st.bar_chart(data_bar_grouped)

    with col2:
        st.header("Dataset")
        st.write(data_bar_grouped)


    col1, col2 = st.columns(2)

    with col1:
        st.header("Quality Trend")
        st.bar_chart(data_line_trend_grouped["Yield"])

    with col2:
        st.header("Dataset")
        st.write(data_line_trend_grouped)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Totals")
        st.write(sums)

    with col2:
        st.header("Total YIELD:")
        st.text(Total_Yield_Displayed)

st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


cols = list(data_per_project.columns)


st.sidebar.header("Error-Filter:")

error = st.sidebar.selectbox("Choose the error:", options = cols)

errordata = data_per_project[error]

with st.expander("Data per week"):

    st.header("Data accumulated per week")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Selected set per project")
        st.bar_chart(data_per_project)

    with col2:
        st.header("Dataset per project")
        st.write(data_per_project)


    col1, col2 = st.columns(2)

    with col1:
        st.header("Trend-Chart Errors")
        st.line_chart(errordata)










#sidebar
