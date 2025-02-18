import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

import folium
from streamlit_folium import st_folium


@st.dialog("Περιγραφή Ιδιοκτησίας", width='large')
def open_details(row_data, image, lang):
    main_dtls_1, main_dtls_2 = st.columns([3,1])
    img = st.columns(1)

    if 'show_map' not in st.session_state:
        st.session_state.show_map = False

    if st.session_state.show_map:
        map = show_map(row_data, image)
        st_folium(map, width=700, height=400)

    else:
        img[0].markdown(
            f"""<div style='position:relative;width:100%;height:400px;overflow:hidden;border-radius:2%;'>
                <img class='image_modal' src='{image}' style='width:100%;'>
            </div>""", unsafe_allow_html=True)
    
    if img[0].button('map', key='map'):
        map = show_map(row_data, image)
        st_folium(map, width=700, height=400)
        st.session_state.show_map = True
    
    show_img = st.columns(1)
    if st.session_state.show_map:
        if show_img[0].button('Close Map', key='close_map'):
            st.session_state.show_map = False
            map = show_map(row_data, image)
            st_folium(map, key='placeholder', width=1, height=1)

    sub_dtls_1, sub_dtls_2, sub_dtls_3 = st.columns([1,1,1])

    sub_dtls_4, sub_dtls_5, sub_dtls_6 = st.columns([1,1,1])
    link = st.columns(2)
    summary = st.columns(1)

    main_dtls_1.markdown(f"<p class='head_dtls' style='font-size:24px;'>{row_data['address_gr']}</p>", unsafe_allow_html=True)
    main_dtls_2.markdown(f"<p class='head_dtls' style='text-align:right;font-size:24px;'><strong>&#8364; {row_data['price']}</strong></p>", unsafe_allow_html=True)
    
    if type(row_data['surface']) == float:
        sub_dtls_1.markdown(f"<strong>Εμβαδόν:</strong> {row_data['surface']} τ.μ.", unsafe_allow_html=True)
    else:
        sub_dtls_1.markdown(f"<strong>Εμβαδόν:</strong> -", unsafe_allow_html=True)
    
    if type(row_data['price_per_m2']) == str:
        sub_dtls_2.markdown(f"<strong>Τιμή ανά τ.μ.:</strong> {row_data['price_per_m2']} &#8364;", unsafe_allow_html=True)
    else:
        sub_dtls_2.markdown(f"<strong>Τιμή ανά τ.μ.:</strong> -", unsafe_allow_html=True)
    
    category = f"category_{lang}"
    if type(category) == str:
        sub_dtls_3.markdown(F"<strong>Κατηγορία:</strong> {row_data[category]}", unsafe_allow_html=True)
    
    if str(row_data['construction_year']) != 'nan':
        year = int(row_data['construction_year'])
        sub_dtls_4.markdown(f"<strong>Έτος Κατασκευής:</strong> {year}", unsafe_allow_html=True)
    else:
        sub_dtls_4.markdown(f"<strong>Έτος Κατασκευής:</strong> -", unsafe_allow_html=True)
    
    if type(row_data['floor_num']) == float:
        sub_dtls_5.markdown(f"<strong>Όροφος:</strong> {int(row_data['floor_num'])}", unsafe_allow_html=True)
    else:
        sub_dtls_5.markdown(f"<strong>Όροφος:</strong> -", unsafe_allow_html=True)
    
    if type(row_data['has_parking']) == str:
        if row_data['has_parking'] == 'TRUE':
            sub_dtls_6.markdown(f"<strong>Χώρος Στάθμευσης:</strong> Ναι", unsafe_allow_html=True)
        else:
            sub_dtls_6.markdown(f"<strong>Χώρος Στάθμευσης:</strong> Όχι", unsafe_allow_html=True)
    elif type(row_data['has_parking']) == bool:
        if row_data['has_parking']:
            sub_dtls_6.markdown(f"<strong>Χώρος Στάθμευσης:</strong> Ναι", unsafe_allow_html=True)
        else:
            sub_dtls_6.markdown(f"<strong>Χώρος Στάθμευσης:</strong> Όχι", unsafe_allow_html=True)

    if type(row_data['url']) == str:
        link[0].markdown(f"<strong>Link:</strong> {row_data['url']}", unsafe_allow_html=True)
    else:
        link[0].markdown(f"<strong>Link:</strong> -", unsafe_allow_html=True)
        
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
    .st-key-map {
        text-align:right;
        position:absolute;
        top:5px;left:-5px;
        width:100%;height:100%;
    }
    .st-key-map button {
        color: rgb(49, 51, 63)!important;
        border-color: rgb(49, 51, 63)!important;
    }
    .st-key-map button:hover {
        background-color: rgb(49, 51, 63);
        color: rgb(255, 255, 255)!important;
    }
    .st-key-map_view .stButton, .st-key-list_view .stButton {
        display: flex;
        align-items: center;
    }
    .st-key-map_view .stButton {
        justify-content: left;
    }
    .st-key-list_view .stButton {
        justify-content: right;
    }
    .st-key-map_view button, .st-key-list_view button {
        background-color: #ff5454!important;
        color: white!important;
    }
    </style>
    """, unsafe_allow_html=True)

    return


def create_sidebar():

    sidebar = st.sidebar
    search_term = sidebar.text_input('##### Search Properties', key='search', placeholder='Search by address, price, etc.')

    sidebar.write('##### Filter Properties')

    price_min = sidebar.number_input('Price Min', placeholder='0', min_value=0)
    price_max = sidebar.number_input('Price Max', placeholder='1000000', min_value=0)

    surface_min = sidebar.number_input('Surface Min', placeholder='0', min_value=0)
    surface_max = sidebar.number_input('Surface Max', placeholder='500', min_value=0)

    construction_year = sidebar.number_input('Construction Year', placeholder='0', min_value=0)

    has_parking = sidebar.toggle('Parking')
    has_storage = sidebar.toggle('Storage')

    sidebar.button('Clear Filters', key='clear_filters', on_click=lambda: st.session_state.clear(
        price_min=None, price_max=None, surface_min=None, surface_max=None, construction_year=None, parking=False, storage=False
    ))

    filter_data = False

    if search_term:
        if st.session_state.search_term != search_term:
            st.session_state.search_term = search_term
            filter_data = True

    if st.session_state.price_min != price_min:
        st.session_state.price_min = price_min
        filter_data = True
    if st.session_state.price_max != price_max:
        st.session_state.price_max = price_max
        filter_data = True
    
    if st.session_state.surface_min != surface_min:
        st.session_state.surface_min = surface_min
        filter_data = True
    if st.session_state.surface_max != surface_max:
        st.session_state.surface_max = surface_max
        filter_data = True
    
    if st.session_state.construction_year != construction_year:
        st.session_state.construction_year = construction_year
        filter_data = True

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

    errors = []

    if file_name:
        if 'file' not in st.session_state or st.session_state.file != file_name:
            st.session_state.file = file_name
    else:
        if 'file' not in st.session_state:
            st.session_state.file = 'real_estate_property_catalog.csv'


    data = pd.read_csv(st.session_state.file)

    data['has_parking'] = data['has_parking'].fillna('FALSE').astype(str).str.upper() == 'TRUE'
    data['has_storage'] = data['has_storage'].fillna('FALSE').astype(str).str.upper() == 'TRUE'

    data['price'] = data['price'].fillna(0)
    data['price'] = data['price'].str.replace(',', '')
    data['price'] = pd.to_numeric(data['price'], errors='coerce')

    data['surface'] = data['surface'].fillna(0)
    data['surface'] = pd.to_numeric(data['surface'], errors='coerce')

    data['construction_year'] = pd.to_numeric(data['construction_year'], errors='coerce')
    
    filters = []

    if 'search_term' in st.session_state and st.session_state.search_term:
        filters.append('search_term')

    if st.session_state.price_min:
        filters.append('price_min')
    if st.session_state.price_max:
        filters.append('price_max')

    if st.session_state.surface_min:
        filters.append('surface_min')
    if st.session_state.surface_max:
        filters.append('surface_max')

    if st.session_state.construction_year:
        filters.append('construction_year')

    if st.session_state.parking:
        filters.append('parking')

    if st.session_state.storage:
        filters.append('storage')
    
    if len(filters) > 0:
        data, err_data_2 = search_query(data, filters)

        if err_data_2:
            errors.append(err_data_2)
    
    if errors:
        return data, st.session_state.file, errors
    else:
        return data, st.session_state.file, None


def search_query(data, keywords):

    errors = []

    if isinstance(keywords, list):
        query = []

        if 'price_min' in keywords:
            if st.session_state.price_min is not None:
                query.append(f'price >= {st.session_state.price_min}')
        if 'price_max' in keywords:
            if st.session_state.price_max is not None:
                query.append(f'price <= {st.session_state.price_max}')

        if 'surface_min' in keywords:
            if st.session_state.surface_min is not None:
                query.append(f'surface >= {st.session_state.surface_min}')
        if 'surface_max' in keywords:
            if st.session_state.surface_max is not None:
                query.append(f'surface <= {st.session_state.surface_max}')

        if 'construction_year' in keywords:
            if st.session_state.construction_year is not None:
                query.append(f'construction_year == {st.session_state.construction_year}')
        
        if 'parking' in keywords:
            query.append('has_parking == True')

        if 'storage' in keywords:
            query.append('has_storage == True')
        
        if 'search_term' in keywords:
            key = st.session_state.search_term
            query.append('(address_gr.str.contains(@key) | description_gr.str.contains(@key))')

        if query:
            query_str = ' & '.join(query)
            filtered_data = data.query(query_str, engine='python')
        else:
            filtered_data = data
    else:
        filtered_data = data
    
    if filtered_data.empty:
        filtered_data = data
        errors.append('No results found for the search term')
    
    if errors:
        return filtered_data, errors
    else:
        return filtered_data, None


def show_map(row_data, image_link):
    lat = row_data['lat']
    lng = row_data['lng']
    
    map = folium.Map(location=[lat, lng], zoom_start=15)
    folium.Marker(location=[lat, lng], popup=row_data['address_gr'], lazy=True).add_to(map)
    return map


def main():

    st.set_page_config(layout="wide")

    apply_style()

    pages = {
        "Home": [st.Page("1_home.py", title="Real Estate Property Catalog")],
        "Property Listings": [
            st.Page("2_list.py", title="Property Listings - List"),
            st.Page("3_map.py", title="Property Listings - Map"), 
        ],
    }

    if 'lang' not in st.session_state:
        st.session_state.lang = 'gr'
    if 'search_term' not in st.session_state:
        st.session_state.search_term = None
    
    if 'price_max' not in st.session_state:
        st.session_state.price_max = None
    if 'price_min' not in st.session_state:
        st.session_state.price_min = None
    if 'surface_max' not in st.session_state:
        st.session_state.surface_max = None
    if 'surface_min' not in st.session_state:
        st.session_state.surface_min = None
    if 'construction_year' not in st.session_state:
        st.session_state.construction_year = None
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