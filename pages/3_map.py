import streamlit as st
import pandas as pd

import folium
from streamlit_folium import st_folium

from main import open_details


def main():
    st.title('Property Listings - Map')

    data = pd.read_csv('real_estate_property_catalog.csv')

    m = folium.Map(location=(37.983810, 23.727539), zoom_start=16)
    bounds = [37.983810 ,23.727539]

    for i, row in data.iterrows():
        row_data = data.iloc[i].astype(object).to_dict()

        if str(row_data['lat']) != 'nan' and str(row_data['lng']) != 'nan':
        
            lat, lng = assemble_coordinates(str(row_data['lat']), str(row_data['lng']))

            if lat and lng:
                if float(lat) > bounds[0] - 0.5 and float(lat) < bounds[0] + 0.5:
                    folium.Marker(location=[lat,lng], popup=row_data['address_gr']).add_to(m)

    
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

main()