import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelBinarizer
import streamlit as st
import re
import pickle
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ["Basic Overview", "Data Prediction"],
                           styles={"nav-link": {"font": "sans serif", "font-size": "25px", "text-align": "centre"},
                                   "nav-link-selected": {"font": "sans serif", "background-color": "#ff0bab"},
                                   "icon": {"font-size": "20px"}
                                   }
                           )

# -------------------------------------------------------------------------------------------------

if selected == "Basic Overview":
    st.markdown(
        "<h1 style='text-align: center; font-size: 40px; color: #ff0bab;' ><u> Industrial Copper - Predictions </u> </h1>",
        unsafe_allow_html=True)
    st.markdown(
        "### :green[Overview :] In this project, the goal is to design and implement a machine learning model to predict the selling price and status. The model leverage historical data from past transactions in Copper to predict accurate prices. ")
    st.markdown(
        "### :blue The primary objective is to learn about ML predictions but it also provides a valuable tool which can be used for multiple prediction purposes")
    st.markdown(
        "### :green[Libraries Used :] Streamlit, Pandas, numpy, pickle, Sklearn - Decision Tree Regression, etc")
    st.markdown("<h1 style='text-align: center; font-size: 40px; color: #ff0bab;'> </h1", unsafe_allow_html=True)

if selected == "Data Prediction":

    st.write("""
    <div style='text-align:center'>
        <h1 style='color:#ff0bab;'>Industrial Copper - Predictions</h1>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Predict Selling Price", "Predict Status"])
    with tab1:
        status_options = ['Won', 'Draft', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised',
                          'Offered', 'Offerable']
        item_type_options = ['W', 'WI', 'S', 'Others', 'PL', 'IPL', 'SLAWR']
        country_options = [28., 25., 30., 32., 38., 78., 27., 77., 113., 79., 26., 39., 40., 84., 80., 107., 89.]
        application_options = [10., 41., 28., 59., 15., 4., 38., 56., 42., 26., 27., 19., 20., 66., 29., 22., 40., 25.,
                               67., 79., 3., 99., 2., 5., 39., 69., 70., 65., 58., 68.]
        product = ['611112', '611728', '628112', '628117', '628377', '640400', '640405', '640665',
                   '611993', '929423819', '1282007633', '1332077137', '164141591', '164336407',
                   '164337175', '1665572032', '1665572374', '1665584320', '1665584642', '1665584662',
                   '1668701376', '1668701698', '1668701718', '1668701725', '1670798778', '1671863738',
                   '1671876026', '1690738206', '1690738219', '1693867550', '1693867563', '1721130331', '1722207579']

        with st.form("my_form"):
            col1, col2, col3 = st.columns([5, 2, 5])
            with col1:
                st.write(' ')
                status = st.selectbox("Status", status_options, key=1)
                item_type = st.selectbox("Item Type", item_type_options, key=3)
                country = st.selectbox("Country", sorted(country_options), key=4)
                application = st.selectbox("Application", sorted(application_options), key=5)
                product_ref = st.selectbox("Product Reference", product, key=6)
            with col3:
                quantity_tons = st.text_input("Enter Quantity Tons (Min:611728 & Max:1722207579)")
                thickness = st.text_input("Enter thickness (Min:0.18 & Max:400)")
                width = st.text_input("Enter width (Min:1, Max:2990)")
                customer = st.text_input("customer ID (Min:12458, Max:30408185)")
                submit_button = st.form_submit_button(label="PREDICT SELLING PRICE")
                st.markdown("""
                        <style>
                        div.stButton > button:first-child {
                            background-color: #ff0bab;
                            color: white;
                            width: 100%;
                        }
                        </style>
                    """, unsafe_allow_html=True)

            flag = 0
            pattern = "^(?:\d+|\d*\.\d+)$"
            for i in [quantity_tons, thickness, width, customer]:
                if re.match(pattern, i):
                    pass
                else:
                    flag = 1
                    break

        if submit_button and flag == 1:
            if len(i) == 0:
                st.write("please enter a valid number space not allowed")
            else:
                st.write("You have entered an invalid value: ", i)

        if submit_button and flag == 0:
            with open(r"C:\Users\ADMIN\Downloads\best_model.pkl", 'rb') as f:
                loaded_model = pickle.load(f)
            with open(r'C:\Users\ADMIN\Downloads\scaler.pkl', 'rb') as f:
                scaler_loaded = pickle.load(f)

            with open(r"C:\Users\ADMIN\Downloads\item_type.pkl", 'rb') as f:
                t_loaded = pickle.load(f)

            with open(r"C:\Users\ADMIN\Downloads\status.pkl", 'rb') as f:
                s_loaded = pickle.load(f)

            new_sample = np.array([[np.log(float(quantity_tons)), application, np.log(float(thickness)), float(width),
                                    country, float(customer), int(product_ref), item_type, status]])
            new_sample_ohe = t_loaded.transform(new_sample[:, [7]]).toarray()
            new_sample_be = s_loaded.transform(new_sample[:, [8]]).toarray()
            new_sample = np.concatenate((new_sample[:, [0, 1, 2, 3, 4, 5, 6, ]], new_sample_ohe, new_sample_be), axis=1)
            new_sample1 = scaler_loaded.transform(new_sample)
            new_pred = loaded_model.predict(new_sample1)[0]
            st.write('## :green[Predicted selling price:] ', np.exp(new_pred))

    with tab2:

        with st.form("my_form1"):
            col1, col2, col3 = st.columns([5, 2, 5])
            with col1:
                cquantity_tons = st.text_input("Enter Quantity Tons (Min:611728 & Max:1722207579)")
                cthickness = st.text_input("Enter thickness (Min:0.18 & Max:400)")
                cwidth = st.text_input("Enter width (Min:1, Max:2990)")
                ccustomer = st.text_input("customer ID (Min:12458, Max:30408185)")
                cselling = st.text_input("Selling Price")

            with col3:
                st.write(' ')
                citem_type = st.selectbox("Item Type", item_type_options, key=10)
                ccountry = st.selectbox("Country", sorted(country_options), key=11)
                capplication = st.selectbox("Application", sorted(application_options), key=21)
                cproduct_ref = st.selectbox("Product Reference", product, key=31)
                csubmit_button = st.form_submit_button(label="PREDICT STATUS")

            cflag = 0
            pattern = "^(?:\d+|\d*\.\d+)$"
            for k in [cquantity_tons, cthickness, cwidth, ccustomer, cselling]:
                if re.match(pattern, k):
                    pass
                else:
                    cflag = 1
                    break

        if csubmit_button and cflag == 1:
            if len(k) == 0:
                st.write("please enter a valid number space not allowed")
            else:
                st.write("You have entered an invalid value: ", k)

        if csubmit_button and cflag == 0:
            import pickle

            with open(r"C:\Users\ADMIN\Downloads\c_bestmodel.pkl", 'rb') as f:
                cloaded_model = pickle.load(f)

            with open(r'C:\Users\ADMIN\Downloads\cscaler.pkl', 'rb') as f:
                cscaler_loaded = pickle.load(f)

            with open(r"C:\Users\ADMIN\Downloads\c_item_type.pkl", 'rb') as f:
                ct_loaded = pickle.load(f)

            # Predict the status for a new sample
            # 'quantity tons_log', 'selling_price_log','application', 'thickness_log', 'width','country','customer','product_ref']].values, X_ohe
            new_sample = np.array([[np.log(float(cquantity_tons)), np.log(float(cselling)), capplication,
                                    np.log(float(cthickness)), float(cwidth), ccountry, int(ccustomer),
                                    int(product_ref), citem_type]])
            new_sample_ohe = ct_loaded.transform(new_sample[:, [8]]).toarray()
            new_sample = np.concatenate((new_sample[:, [0, 1, 2, 3, 4, 5, 6, 7]], new_sample_ohe), axis=1)
            new_sample = cscaler_loaded.transform(new_sample)
            new_pred = cloaded_model.predict(new_sample)
            if new_pred == 1:
                st.write('## :green[The Status is Won] ')
            else:
                st.write('## :red[The status is Lost] ')
