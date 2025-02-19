import streamlit as st
from main import open_details, set_data
from screeninfo import get_monitors


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
        div[data-testid='stMarkdownContainer'] {
            overflow: auto;
        }
        .image {
            float: left;
            width:  250px;
            height: 350px;
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
        .stFileUploaderFile {
            display: none;
        }
        @media (max-width: 1320px) {
            .st-emotion-cache-wt9exi {
                min-width: calc(100% - 1.5rem);
            }
            .st-emotion-cache-fvdmmq {
                min-width: calc(100% - 1.5rem);
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    return


def main():
    errors = []

    apply_styles()
    
    col1, col2 = st.columns([2,1])
    lang = st.session_state.lang

    col1.title('Property Listings - List')
    file = col2.file_uploader('Upload a CSV file', type=['csv'])
    if col2.button('Remove File', key='remove_file'):
        st.session_state.file = 'real_estate_property_catalog.csv'
        file= None

    if file:
        data, subtitle, err_data = set_data(file.name)

        if err_data:
            for err in err_data:
                st.error(f"Errors in data: {err[0]}")
        
    else:
        data, subtitle, err_data = set_data(None)

        if err_data:
            for err in err_data:
                st.error(f"Errors in data: {err[0]}")
        
    st.write(f"***Reading Data From:*** *{subtitle}*")

    if 'page' not in st.session_state:
        st.session_state.page = 1
    
    pages = len(data) // 14

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
    
    page_indicator = page * 14
    indexes = [page_indicator - 14, page_indicator]
    row_of = 2

    # handle display of page data in rows of 4
    for i in range(indexes[0], min(indexes[1], len(data)), row_of):
        row = st.columns(row_of)
        for j, r in enumerate(row):
            if i + j < len(data):
                with r:
                    try:
                        row_data = data.iloc[i + j].astype(object).to_dict()

                        container = st.container(key=f"card_container_{i+j}", height=550, border=True)

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
                        sub_dtls_1.write(F"<strong>Κατηγορία:</strong> {row_data[category]}", unsafe_allow_html=True)

                        if sub_dtls_2.button('More', key=f"more_{i+j}"):
                            open_details(row_data, image, lang)
                            
                        summary[0].markdown(f"<p class='summary'><strong>Περιγραφή:</strong> {row_data['description_gr']}</p>", unsafe_allow_html=True)

                    except Exception as e:
                        st.error(f"Error displaying row {i + j}: {e}")
    return


main()