import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from main import open_details, set_data


def main():
    st.title('Real Estate Property Catalog')

    errors = []

    if 'file' not in st.session_state:
        file_name = st.session_state.file = 'real_estate_property_catalog.csv'
        data, subtitle, err_data = set_data(None)
        if err_data:
            for err in err_data:
                errors.append(f"Errors in data: {err[0]}")
    else:
        file_name = st.session_state.file
        data, subtitle, err_data = set_data(file_name)
        if err_data:
            for err in err_data:
                errors.append(f"Errors in data: {err[0]}")
    
    data = pd.read_csv(file_name)

    data['has_parking'] = data['has_parking'].fillna('FALSE').astype(str).str.upper() == 'TRUE'
    data['has_storage'] = data['has_storage'].fillna('FALSE').astype(str).str.upper() == 'TRUE'

    data['price'] = data['price'].fillna(0)
    data['price'] = data['price'].str.replace(',', '')
    data['price'] = pd.to_numeric(data['price'], errors='coerce')

    data['surface'] = data['surface'].fillna(0)
    data['surface'] = pd.to_numeric(data['surface'], errors='coerce')

    data['construction_year'] = pd.to_numeric(data['construction_year'], errors='coerce')

    st.markdown("<hr>", unsafe_allow_html=True)

    description = st.columns(1)

    description[0].markdown("""
                <h4 style='text-align:center;'>Ανακαλύψτε το Ιδανικό Ακίνητο με Την Εφαρμογή Μας!</h4>
                <br>
                <p style='text-align:center;'>Καλώς ήρθατε στην απόλυτη εμπειρία αναζήτησης ακινήτων! 
                    Η εφαρμογή μας σας επιτρέπει να εξερευνήσετε εύκολα και γρήγορα μια μεγάλη ποικιλία από καταχωρήσεις, 
                    προσαρμοσμένες στις ανάγκες σας.
                </p>
                <br>
          """, unsafe_allow_html=True)

    buttons = st.columns(2)
    if buttons[0].button('List View', key='list_view'):
        st.switch_page('2_list.py')
    if buttons[1].button('Map View', key='map_view'):
        st.switch_page('3_map.py') 

    features = st.columns(3)

    for feature in features:
        feature.markdown("<br>", unsafe_allow_html=True)

    features[0].markdown("""
                <h4 style='text-align:center;'>Δύο Τρόποι Προβολής</h4>
                <p style='text-align:center;'>Καλώς ήρθατε στην απόλυτη εμπειρία αναζήτησης ακινήτων! 
                    Περιηγηθείτε μέσω λίστας για γρήγορη επισκόπηση ή χρησιμοποιήστε τον διαδραστικό χάρτη για μια πιο οπτική και στοχευμένη αναζήτηση. 
                </p>
          """, unsafe_allow_html=True)  
    features[1].markdown("""
                <h4 style='text-align:center;'>Εύκολη Ανάρτηση Δεδομένων</h4>
                <p style='text-align:center;'>Καλώς ήρθατε στην απόλυτη εμπειρία αναζήτησης ακινήτων! 
                    Ανεβάστε τις δικές σας καταχωρήσεις ακινήτων με λίγα μόνο βήματα.
                </p>
          """, unsafe_allow_html=True)  
    features[2].markdown("""
                <h4 style='text-align:center;'>Εξυπνη Αναζήτηση</h4>
                <p style='text-align:center;'>Καλώς ήρθατε στην απόλυτη εμπειρία αναζήτησης ακινήτων! 
                    Φιλτράρετε τα αποτελέσματα με βάση τις προτιμήσεις σας και βρείτε ακριβώς αυτό που ψάχνετε.
                </p>
          """, unsafe_allow_html=True)  

    metrics = st.columns(4)

    for metric in metrics:
        metric.markdown("<br>", unsafe_allow_html=True)

    mean_price = data['price'].mean()
    mean_surface = data['surface'].mean()

    metrics[0].metric('Ακίνητα', data.shape[0])
    metrics[1].metric('Μεταβλητές', data.shape[1])
    metrics[2].metric('Μέση Τιμή', f'{mean_price:.2f} €')
    metrics[3].metric('Μέσο Εμβαδόν', f'{mean_surface:.2f} m²')

    data = data.dropna(subset=['price', 'construction_year'])

    # create graph for price vs construction year


    return


main()