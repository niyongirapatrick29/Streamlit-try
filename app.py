# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 23:40:43 2021

@author: pati
"""

#!pip install streamlit
import streamlit as st
import pandas as pd

st.title('Web app using streamlit')
data = pd.read_csv('creditcard.csv')
st.write(data)
