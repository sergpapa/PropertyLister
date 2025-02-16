import streamlit as st
import pandas as pd
import numpy as np

from main import open_details, set_data

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

def apply_styles():
    st.markdown(
        """
        <style>
        .st-key-remove_file button {
            display: flex;
            align-items: center;
            justify-content: end;
        }
        .st-key-next_page button,.st-key-prev_page button {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: auto;
        }
        div[data-testid='stVerticalBlockBorderWrapper'] {
                                    overflow: hidden;
        }
        .image {
            float: left;
            width:  250px;
            height: 250px;
            object-fit: cover;
            border-radius: 2%;
        }
        .head_dtls {
            padding-bottom: 10px;
        }
        .summary {
            height: 50px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;  /* Limits text to 2 lines */
            -webkit-box-orient: vertical;
            text-overflow: ellipsis;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    return


def main():
    apply_styles()
    
    col1, col2 = st.columns([2,1])
    lang = st.session_state.lang

    col1.title('Property Listings - List')
    file = col2.file_uploader('Upload a CSV file', type=['csv'])

    if file:
        data, subtitle = set_data(file.name)
    else:
        data, subtitle = set_data(None)
        
    st.write(f"***Reading Data From:*** *{subtitle}*")

    if 'page' not in st.session_state:
        st.session_state.page = 1

    pages = len(data) // 21
    if pages == 0:
        pages = 1

    # Display data page
    show_page(data, st.session_state.page, lang)

    # Add pagination buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Previous Page', key='prev_page', disabled=st.session_state.page <= 1):
            if st.session_state.page > 1:
                st.session_state.page -= 1
                st.session_state.page -= 1
                st.rerun()
    with col2:
        st.markdown(f"<div class='page_count' style='text-align: center;height:40px;'>Page {st.session_state.page} of {pages}</div>", unsafe_allow_html=True)
    with col3:
        if st.button('Next Page', key='next_page', disabled=st.session_state.page >= pages):
            if st.session_state.page < pages:
                st.session_state.page += 1
                st.rerun()
    return


def show_page(data, page, lang):
    # Calculate the indexes for the current page
    page_indicator = page * 21  
    indexes = [page_indicator - 21, page_indicator]

    # handle display of page data in rows of 4
    for i in range(indexes[0], min(indexes[1], len(data)), 3):
        row = st.columns(3)
        for j, r in enumerate(row):
            if i + j < len(data):
                with r:
                    try:
                        row_data = data.iloc[i + j].astype(object).to_dict()

                        container = st.container(key=f"card_container_{i+j}", height=450, border=True)

                        main_dtls_1, main_dtls_2 = container.columns([3,1])
                        img = container.columns(1)
                        sub_dtls_1, sub_dtls_2 = container.columns([4,1])
                        summary = container.columns(1)

                        main_dtls_1.markdown(f"{row_data['address_gr']}")
                        main_dtls_2.markdown(f"<p class='head_dtls' style='text-align:right;'><strong>&#8364; {row_data['price']}</strong></p>", unsafe_allow_html=True)

                        img_url = row_data['img_url']
        
                        if type(img_url) == str:

                            img_urls = img_url.split("'")

                            for img_url in img_urls:
                                if img_url != '[' and img_url != ']' and img_url != ',' and img_url != ' ':

                                    image = img_url
                                    img[0].markdown(f"<img class='image' src='{(img_url)}' style='width:100%;'>", unsafe_allow_html=True)
                                
                                    break
                        else:
                            image = 'https://placehold.co/250x250'
                            img[0].markdown(f"<img class='image' src='https://placehold.co/250x250' style='width:100%;'>", unsafe_allow_html=True)
                        
                        category = f"category_{lang}"
                        sub_dtls_1.write(F"<strong>Κατηγρία:</strong> {row_data[category]}", unsafe_allow_html=True)

                        if sub_dtls_2.button('More', key=f"more_{i+j}"):
                            open_details(row_data, image, lang)
                            
                        summary[0].markdown(f"<p class='summary'><strong>Περιγραφή:</strong> {row_data['description_gr']}</p>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Error displaying row {i + j}: {e}")
    return


main()
