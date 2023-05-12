import streamlit as st
from product_handler import ProductHandler
import pandas as pd

st.set_page_config(
    page_title="庫存管理系統",
    layout="wide",
)

@st.cache_resource
def ph():
    # Create a database connection object that points to the URL.
    ph = ProductHandler()
    return ph

st.session_state['temp_product'] = []
st.session_state['ph'] = ph