import streamlit as st
import pandas as pd

import folium
from streamlit_folium import st_folium

from main import set_data


def main():
    st.title('Property Listings - Map')

    lang = st.session_state.lang

    if 'file' not in st.session_state:
        data, subtitle, err_data = set_data(None)
    else:
        data, subtitle, err_data = set_data(st.session_state.file)

    if err_data:
        for err in err_data:
            st.error(f"Errors in data: {err[0]}")

    st.write(f"***Reading Data From:*** *{subtitle}*")

    m = folium.Map(location=(37.983810, 23.727539), zoom_start=16)
    bounds = [37.983810 ,23.727539]

    for i, row in data.iterrows():
        row_data = row.astype(object).to_dict()

        img_url = row_data['img_url']
        
        if type(img_url) == str:

            img_urls = img_url.split("'")

            for img_url in img_urls:
                if img_url != '[' and img_url != ']' and img_url != ',' and img_url != ' ':

                    image = img_url       
                    break
        else:
            image = 'https://placehold.co/250x250'
           
        

        if str(row_data['lat']) != 'nan' and str(row_data['lng']) != 'nan':
        
            lat, lng = assemble_coordinates(str(row_data['lat']), str(row_data['lng']))

            if lat and lng:
                if float(lat) > bounds[0] - 0.5 and float(lat) < bounds[0] + 0.5:

                    popup_html = create_popup_html(row_data, image, lang)
                    popup = folium.Popup(popup_html, max_width=500)
                    folium.Marker(location=[lat, lng], popup=popup, lazy=True).add_to(m)
    
    st_folium(m, use_container_width=True)
    
    return


def assemble_coordinates(lat, lng):

    lat_nums = []
    for char in lat:
        if char in '0123456789':
            lat_nums.append(char)
    if len(lat_nums) == 9:
        lat = str(lat_nums[0]+lat_nums[1]+'.'+lat_nums[2]+lat_nums[3]+lat_nums[4]+lat_nums[5]+lat_nums[6]+lat_nums[7]+lat_nums[8])
    else:
        lat = None
    
    lng_nums = []
    for char in lng:
        if char in '0123456789':
            lng_nums.append(char)
    if len(lng_nums) == 9:
        lng = str(lng_nums[0]+lng_nums[1]+'.'+lng_nums[2]+lng_nums[3]+lng_nums[4]+lng_nums[5]+lng_nums[6]+lng_nums[7]+lng_nums[8])
    else:
        lng = None

    return lat, lng


def create_popup_html(row_data, image, lang):

    has_parking = row_data['has_parking']
    if has_parking == True:
        has_parking = 'Ναι'
    else:
        has_parking = 'Όχι'

    has_storage = row_data['has_storage']
    if has_storage == True:
        has_storage = 'Ναι'
    else:
        has_storage = 'Όχι'

    popup_html = f"""
    <div style="width:450px;height:450px;overflow-y:auto;padding-right:10px;">
        <h4>{row_data['address_gr']}</h4>
        <img src="{image}" style="width:430px;height:430px;object-fit:cover;border-radius:2%;"/>
        <p><strong>Τιμή:</strong> &#8364; {row_data['price']}</p>
        <p><strong>Εμβαδόν:</strong> {row_data['surface']} τ.μ.</p>
        <p><strong>Χώρος Στάθμευσης: </strong>{has_parking}</p>
        <p><strong>Αποθήκη:</strong> {has_storage}</p>
        <p><strong>Κατηγορία:</strong> {row_data[f'category_{lang}']}</p>
        <p><strong>Περιγραφή:</strong> {row_data['description_gr']}</p>

    </div>
    """
    return popup_html


main()