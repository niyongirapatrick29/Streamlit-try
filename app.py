# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:40:43 2021

@author: pati
"""

#!pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
#pip install plotly
import plotly.express as px

DATA_URL = "archive/nypd-motor-vehicle-collisions.csv"
st.title('Web app using streamlit')

st.cache(persist=True)
def loaddata(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows,parse_dates=[['ACCIDENT DATE','ACCIDENT TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis=1, inplace=True)
    data.rename(columns={'accident date_accident time':'date/line'}, inplace=True)
    return data
data = loaddata(1000)
original_data = data
st.header('Where are the most people injured in NYC')
injured_people = st.slider("Number of persons injured in vehicle collision",0,19)
data.rename(columns={'number of persons injured':'number_of_persons_injured'}, inplace=True)
data['number_of_persons_injured'] = data['number_of_persons_injured'].astype('int32')
st.map(data.query("number_of_persons_injured >= @injured_people")[["latitude","longitude"]].dropna(how="any"))


st.header("How many collision occurs in each state")
#state = st.selectbox("Select State: ",data['borough'].unique())
hours = st.slider("Select hours", 0,23)
data = data[data['date/line'].dt.hour==hours]
#data = data[data['borough']== state]

st.markdown("Vehicle collision between %i:00 and %i:00" %(hours,(hours + 1) % 24))
midpoint = (np.average(data['latitude'])), np.average(data['longitude'])
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude":midpoint[0],
        "longitude":midpoint[1],
        "zoom":11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data = data[['date/line','latitude','longitude']],
        get_position=['longitude','latitude'],
        radius=100,
        extruded = True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ]
    ))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hours,( hours+1) % 24))
filtered = data[
    (data['date/line'].dt.hour>=hours)&(data['date/line'].dt.hour<(hours+1))
]
hist = np.histogram(filtered['date/line'].dt.minute, bins=60,range=(0,60))[0]
chart_data = pd.DataFrame({'minute':range(60),'crashes':hist})
fig = px.bar(chart_data, x='minute',y='crashes',hover_data=['minute','crashes'],height=400)
st.write(fig)


#Last task

st.header("Top 5 dangerous street by affected type")
select = st.selectbox('Affected type of peaple',['Pedestrians','Cyclists','Motorists'])
original_data.rename(columns={"number of pedestrians injured": 'number_of_pedestrians',
    'number of cyclist injured':'number_of_cyclist_injured',
    'number of motorist injured':'number_of_motorist_injured'
    }, inplace=True)

if select=='Pedestrians':
    st.write(original_data.query("number_of_pedestrians>=1")[['on street name','number_of_pedestrians']].sort_values(by=["number_of_pedestrians"], ascending=False).dropna(how="any")[:5])

elif select=='Cyclists':
    st.write(original_data.query("number_of_cyclist_injured>=1")[['on street name','number_of_cyclist_injured']].sort_values(by=["number_of_cyclist_injured"], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("number_of_motorist_injured>=1")[['on street name','number_of_motorist_injured']].sort_values(by=["number_of_motorist_injured"], ascending=False).dropna(how="any")[:5])



if st.checkbox("Show raw data", False):
    st.subheader("Raw data for credit cards")
    st.write(data)


st.header('Claculation using pandas')

#data_per_class = st.slider("Number of fraudirant transactions")
#st.map(data.query("Class>=@data_per_class")[["PC3"],["PC4"]])

#st.markdown('##### Developed by Patrick 🎈')
