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
    
    if type(row_data['has_parking']) == str:
        if row_data['has_parking'] == 'TRUE':
            sub_dtls_3.markdown(f"<strong>Χώρος Στάθμευσης:</strong> Ναι", unsafe_allow_html=True)
        else:
            sub_dtls_3.markdown(f"<strong>Χώρος Στάθμευσης:</strong> Όχι", unsafe_allow_html=True)

    category = f"category_{lang}"
    cat[0].markdown(F"<strong>Κατηγρία:</strong> {row_data[category]}", unsafe_allow_html=True)
        
    summary[0].markdown(f"<p class='summary_modal'><strong>Περιγραφή:</strong> {row_data['description_gr']}</p>", unsafe_allow_html=True)

    return


def apply_style():

    st.markdown("""
    <style>
    .st-emotion-cache-ue6h4q {
        font-size: 14px;
        font-weight: 600;
        color: rgb(85, 88, 103);
        line-height: 1.5;
        padding-right: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

    return


def create_sidebar():

    sidebar = st.sidebar
    search_term = sidebar.text_input('##### Search Properties', key='search', placeholder='Search by address, price, etc.')

    if search_term:
        if st.session_state.search_term != search_term:
            st.session_state.search_term = search_term
            st.rerun() 
    
    sidebar.write('##### Filter Properties')

    has_parking = sidebar.toggle('Parking')
    has_storage = sidebar.toggle('Storage')

    filter_data = False

    if st.session_state.parking != has_parking:
        if has_parking:
            st.session_state.parking = True
            filter_data = True
        else:
            st.session_state.parking = False
            filter_data = True
    
    if st.session_state.storage != has_storage:
        if has_storage:
            st.session_state.storage = True
            filter_data = True
        else:
            st.session_state.storage = False
            filter_data = True
    
    if filter_data:
        st.rerun()

    return sidebar


def set_data(file_name):
    if file_name:
        st.session_state.file = file_name
    else:
        if 'file' not in st.session_state:
            st.session_state.file = 'real_estate_property_catalog.csv'

    data = pd.read_csv(st.session_state.file)

    data['has_parking'] = data['has_parking'].fillna('FALSE').astype(str).str.upper() == 'TRUE'
    data['has_storage'] = data['has_storage'].fillna('FALSE').astype(str).str.upper() == 'TRUE'


    d = data.iloc[10].astype(object).to_dict()

    if 'search_term' in st.session_state and st.session_state.search_term:
        data = search_query(data, st.session_state.search_term)
    
    filters = []

    if st.session_state.parking:
        filters.append('parking')
    if st.session_state.storage:
        filters.append('storage')
    
    if len(filters) > 0:
        data = search_query(data, filters)
    
    return data, st.session_state.file


def search_query(data, keywords):

    if isinstance(keywords, list):
        query = []
        if 'parking' in keywords:
            query.append('has_parking == True')
        if 'storage' in keywords:
            query.append('has_storage == True')
        
        if query:
            query_str = ' & '.join(query)
            filtered_data = data.query(query_str, engine='python')
        else:
            filtered_data = data
    else:
     filtered_data = data.query('address_gr.str.contains(@keywords) & description_gr.str.contains(@keywords)', engine='python')

    return filtered_data


def main():

    st.set_page_config(layout="wide")

    apply_style()

    pages = {
        "Home": [st.Page("pages/1_home.py", title="Real Estate Property Catalog")],
        "Property Listings": [
            st.Page("pages/2_list.py", title="Property Listings - List"),
            st.Page("pages/3_map.py", title="Property Listings - Map"), 
        ],
    }

    if 'lang' not in st.session_state:
        st.session_state.lang = 'gr'
    if 'search_term' not in st.session_state:
        st.session_state.search_term = None
    if 'parking' not in st.session_state:
        st.session_state.parking = False
    if 'storage' not in st.session_state:
        st.session_state.storage = False

    col = st.columns(1)
    en = col[0].toggle("GR/EN", False, help="Change language")
    if en:
        st.session_state.lang = 'en'
    else:
        st.session_state.lang = 'gr'


    pg = st.navigation(pages)
    pg.run()

    sidebar = create_sidebar()

    return


if __name__ == "__main__":
    main()