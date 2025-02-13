import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

pages = {
    "Home": [st.Page("pages/1_home.py", title="Real Estate Property Catalog")],
    "Property Listings": [
        st.Page("pages/2_list.py", title="Property Listings - List"),
        st.Page("pages/3_map.py", title="Property Listings - Map"), 
    ],
}

pg = st.navigation(pages)
pg.run()