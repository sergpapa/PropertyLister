import streamlit as st
import pandas as pd

import folium
from streamlit_folium import st_folium

from main import set_data, assemble_coordinates


def main():
    """
    Main function for the map page. Displays a map with markers for each property listing.
    """

    st.title('Property Listings - Map')

    lang = st.session_state.lang

    # Check if a file has been uploaded and set data accordingly. if errors are found, display them
    if 'file' not in st.session_state:
        data, subtitle, err_data = set_data(None)
    else:
        data, subtitle, err_data = set_data(st.session_state.file)

    if err_data:
        for err in err_data:
            st.error(f"Errors in data: {err[0]}")

    st.write(f"***Reading Data From:*** *{subtitle}*")

    # Create map
    m = folium.Map(location=(37.983810, 23.727539), zoom_start=16)
    bounds = [37.983810 ,23.727539]

    # check if image exists and render accordingly
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
           
        
        # check if lat and lng exist and render accordingly
        if row_data['lat'] and str(row_data['lat']) != 'nan' and row_data['lng'] and str(row_data['lng']) != 'nan':
        
            lat, lng = assemble_coordinates(str(row_data['lat']), str(row_data['lng']))

            if lat and lng:
                if float(lat) > bounds[0] - 0.5 and float(lat) < bounds[0] + 0.5:

                    popup_html = create_popup_html(row_data, image, lang)
                    popup = folium.Popup(popup_html, max_width=500)
                    folium.Marker(location=[lat, lng], popup=popup, lazy=True).add_to(m)
    
    st_folium(m, use_container_width=True)
    
    return


def create_popup_html(row_data, image, lang):
    """
    Create the HTML for the popup that appears when a marker is clicked.
    """

    # check if parking and storage exist and render accordingly
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

    # validate data
    if type(row_data['address_gr']) == str:
        row_data['address_gr'] = f"{row_data['address_gr']}"
    else:
        row_data['address_gr'] = '-'

    if type(row_data['price']) == float or type(row_data['price']) == int and not pd.isnull(row_data['price']):
        row_data['price'] = f"{row_data['price']}"
    else:
        row_data['price'] = '-'
    
    if type(row_data['surface']) == float or type(row_data['surface']) == int and not pd.isnull(row_data['surface']):
        row_data['surface'] = f"{row_data['surface']}"
    else:
        row_data['surface'] = '-'
    
    if type(row_data['category_gr']) == str:
        row_data['category_gr'] = f"{row_data['category_gr']}"
    else:
        row_data['category_gr'] = '-'
    
    if type(row_data['description_gr']) == str:
        row_data['description_gr'] = f"{row_data['description_gr']}"
    else:
        row_data['description_gr'] = '-'
    

    # create the popup html
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