import streamlit as st
import pandas as pd
import numpy as np

# fields = [
#     "created_at",
#     "updated_at",
#     "category_en",
#     "category_gr",
#     "category_source_en",
#     "type_gr",
#     "operation",
#     "lng",
#     "lat",
#     "surface",
#     "construction_year",
#     "price",
#     "price_per_m2",
#     "has_parking",
#     "has_storage",
#     "floor_num",
#     "floor_cnt",
#     "floor_min",
#     "address_gr",
#     "description_gr",
#     "url",
#     "img_url",
#     "postcode"
# ]

def main():
    st.title('Property Listings - List')

    # Load the data
    try:
        data = pd.read_csv('real_estate_property_catalog.csv')
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return

    if 'page' not in st.session_state:
        st.session_state.page = 1

    pages = len(data) // 24

    # Display data page
    show_page(data, st.session_state.page)

    # Add pagination buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Previous Page', key='prev_page', disabled=st.session_state.page <= 1):
            if st.session_state.page > 1:
                st.session_state.page -= 1
                st.session_state.page -= 1
                st.rerun()
    with col2:
        st.markdown(f"<div style='text-align: center;'>Page {st.session_state.page} of {pages}</div>", unsafe_allow_html=True)
    with col3:
        if st.button('Next Page', key='next_page', disabled=st.session_state.page >= pages):
            if st.session_state.page < pages:
                st.session_state.page += 1
                st.rerun()

    # Center the buttons using CSS
    st.markdown(
        """
        <style>
        .stButton > button {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_page(data, page):
    # Calculate the indexes for the current page
    page_indicator = page * 24  
    indexes = [page_indicator - 24, page_indicator]

    # handle display of page data in rows of 4
    for i in range(indexes[0], min(indexes[1], len(data)), 4):
        row = st.columns(4)
        for j, r in enumerate(row):
            if i + j < len(data):
                with r:
                    try:
                        # Convert the problematic column to string to avoid type mismatch
                        row_data = data.iloc[i + j].astype(str)
                        st.write(row_data)
                    except Exception as e:
                        st.error(f"Error displaying row {i + j}: {e}")


main()
