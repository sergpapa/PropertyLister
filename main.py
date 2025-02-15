import streamlit as st
import pandas as pd
import numpy as np


@st.dialog("Περιγραφή Ιδιοκτησίας", width='large')
def open_details(row_data, image, lang):
    main_dtls_1, main_dtls_2 = st.columns([3,1])
    img = st.columns(1)
    sub_dtls_1, sub_dtls_2 = st.columns([1,1])
    sub_dtls_3, sub_dtls_4 = st.columns([1,1])
    cat = st.columns(1)
    summary = st.columns(1)

    main_dtls_1.markdown(f"<p class='head_dtls' style='font-size:24px;'>{row_data['address_gr']}</p>", unsafe_allow_html=True)
    main_dtls_2.markdown(f"<p class='head_dtls' style='text-align:right;font-size:24px;'><strong>&#8364; {row_data['price']}</strong></p>", unsafe_allow_html=True)

    img[0].markdown(f"<img class='image_modal' src='{image}' style='width:100%;'>", unsafe_allow_html=True)
    
    if type(row_data['surface']) == str:
        sub_dtls_1.markdown(f"<strong>Εμβαδόν:</strong> {row_data['surface']} τ.μ.", unsafe_allow_html=True)
    else:
        sub_dtls_1.markdown(f"<strong>Εμβαδόν:</strong> -", unsafe_allow_html=True)
    
    if type(row_data['price_per_m2']) == str:
        sub_dtls_2.markdown(f"<strong>Τιμή ανά τ.μ.:</strong> {row_data['price_per_m2']} &#8364;", unsafe_allow_html=True)
    else:
        sub_dtls_2.markdown(f"<strong>Τιμή ανά τ.μ.:</strong> -", unsafe_allow_html=True)
    
    if str(row_data['construction_year']) != 'nan':
        year = int(row_data['construction_year'])
        sub_dtls_3.markdown(f"<strong>Έτος Κατασκευής:</strong> {year}", unsafe_allow_html=True)
    else:
        sub_dtls_3.markdown(f"<strong>Έτος Κατασκευής:</strong> -", unsafe_allow_html=True)
    
    if type(row_data['floor_num']) == str:
        sub_dtls_4.markdown(f"<strong>Όροφος:</strong> {row_data['floor_num']}", unsafe_allow_html=True)
    else:
        sub_dtls_4.markdown(f"<strong>Όροφος:</strong> -", unsafe_allow_html=True)

    category = f"category_{lang}"
    cat[0].markdown(F"<strong>Κατηγρία:</strong> {row_data[category]}", unsafe_allow_html=True)
        
    summary[0].markdown(f"<p class='summary_modal'><strong>Περιγραφή:</strong> {row_data['description_gr']}</p>", unsafe_allow_html=True)

    return

def main():

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

if __name__ == "__main__":
    main()