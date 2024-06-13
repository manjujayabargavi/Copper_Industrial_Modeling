import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import datetime

st.set_page_config(page_title="Copper Industrial Modelling", page_icon=":anchor:", layout="wide", menu_items=None)

select= option_menu(menu_title=None,
                    options = ["Price Prediction","Status Prediction"],
                    default_index=0,
                    orientation="horizontal",
                    styles={
            "container": {"padding": "0!important", "background-color": "white","size":"cover"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "brown"},
            "nav-link-selected": {"background-color": "brown"}
        } )


item_list=['W', 'S', 'Others', 'PL', 'WI', 'IPL']
status_list=['Won', 'To be approved', 'Lost', 'Not lost for AM', 'Wonderful', 'Revised','Offered', 'Offerable']
country_list=['28', '32', '38', '78', '27', '30', '25', '77', '39', '40', '26', '84', '80', '79','113', '89']
application_list=[10, 41, 28, 59, 15, 4, 38, 56, 42, 26, 27, 19, 20, 66,
                    29, 22, 40, 25, 67, 79, 3, 99, 2, 5,39, 69, 70, 65, 58, 68]

product_list=[1670798778, 1668701718, 628377, 640665, 611993, 1668701376,
                164141591, 1671863738, 1332077137,640405, 1693867550, 1665572374,
                1282007633, 1668701698, 628117, 1690738206, 628112, 640400,
                1671876026, 164336407, 164337175, 1668701725, 1665572032, 611728,
                1721130331, 1693867563, 611733, 1690738219, 1722207579, 929423819,
                1665584320, 1665584662, 1665584642]

if select == "Price Prediction":

    st.markdown("<h1 style='color:brown;'>PRICE PREDICTION</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")

    c1,c2,c3=st.columns([2,2,2])
    with c1:
        quantity=st.text_input('Enter Quantity  (Min:611728 & Max:1722207579) in tons')
        thickness = st.text_input('Enter Thickness (Min:0.18 & Max:400)')
        width = st.text_input('Enter Width  (Min:1, Max:2990)')
        application = st.selectbox('Application Type', application_list)

    with c2:
        country = st.selectbox('Country Code', country_list)
        status = st.selectbox('Status', status_list)
        item = st.selectbox('Item Type', item_list)
        product = st.selectbox('Product Reference', product_list)

    with c3:
        item_order_date = st.date_input("Order Date", datetime.date(2023, 1, 1))
        item_delivery_date = st.date_input("Estimated Delivery Date", datetime.date(2023, 1, 1))

    with c2:
        st.write('')
        st.write('')
        
        if st.button('PREDICT PRICE'):
            price = []
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/country.pkl', 'rb') as file:
                encode_country = pickle.load(file)
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/status.pkl', 'rb') as file:
                encode_status = pickle.load(file)
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/item.pkl', 'rb') as file:
                encode_item = pickle.load(file)
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/Extratreeregressor.pkl', 'rb') as file:
                trained_model = pickle.load(file)

            transformed_country = encode_country.transform(country_list)
            encoded_ct = None
            for i, j in zip(country_list, transformed_country):
                if country == i:
                    encoded_ct = j
                    break
            else:
                st.error("Country not found.")
                exit()

            transformed_status = encode_status.transform(status_list)
            encode_st = None
            for i, j in zip(status_list, transformed_status):
                if status == i:
                    encode_st = j
                    break
            else:
                st.error("Status not found.")
                exit()


            transformed_item = encode_item.transform(item_list)
            encode_it = None
            for i, j in zip(item_list, transformed_item):
                if item == i:
                    encode_it = j
                    break
            else:
                st.error("Item type not found.")
                exit()

            order = datetime.datetime.strptime(str(item_order_date), "%Y-%m-%d")
            delivery = datetime.datetime.strptime(str(item_delivery_date), "%Y-%m-%d")
            day = delivery - order


            price.append(quantity)
            price.append(thickness)
            price.append(width)
            price.append(encoded_ct)
            price.append(encode_st)
            price.append(encode_it)
            price.append(application)
            price.append(product)
            price.append(day.days)

            x = np.array(price).reshape(1, -1)
            price_predict= trained_model.predict(x)
            predicted_price = str(price_predict)[1:-1]
            st.write(f'Predicted Selling Price: :red[₹ {predicted_price}]')


if select == 'Status Prediction':

    st.markdown("<h1 style='color:brown;'>STATUS PREDICTION</h1>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")
    cc1, cc2, cc3 = st.columns([2, 2, 2])
    with cc1:
        quantity_cls = st.text_input('Enter Quantity  (Min:611728 & Max:1722207579) in tons')
        thickness_cls = st.text_input('Enter Thickness (Min:0.18 & Max:400)')
        width_cls= st.text_input('Enter Width  (Min:1, Max:2990)')
        application_cls = st.selectbox('Application Type', application_list)

    with cc2:
        selling_price_cls= st.text_input('Enter Selling Price  (Min:1, Max:100001015)')
        item_cls = st.selectbox('Item Type', item_list)
        country_cls= st.selectbox('Country Code', country_list)
        product_cls = st.selectbox('Product Reference', product_list)

    with cc3:
        item_order_date_cls = st.date_input("Order Date", datetime.date(2023, 1, 1))
        item_delivery_date_cls = st.date_input("Estimated Delivery Date", datetime.date(2023,1, 1))
    with cc2:
        st.write('')
        st.write('')
        st.write('')
        if st.button('PREDICT STATUS'):
            status = []
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/country.pkl', 'rb') as file:
                encode_country_cls = pickle.load(file)
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/item.pkl', 'rb') as file:
                encode_item_cls = pickle.load(file)
            with open('C:/Users/Happy/Desktop/capstone/Copper industrials/randomforest_classification.pkl', 'rb') as file:
                trained_model_cls = pickle.load(file)

            transformed_country_cls = encode_country_cls.transform(country_list)
            encoded_ct_cls = None
            for i, j in zip(country_list, transformed_country_cls):
                if country_cls == i:
                    encoded_ct_cls = j
                    break
            else:
                st.error("Country not found.")
                exit()

            transformed_item_cls = encode_item_cls.transform(item_list)
            encode_it_cls = None
            for i, j in zip(item_list, transformed_item_cls):
                if item_cls == i:
                    encode_it_cls = j
                    break
            else:
                st.error("Item type not found.")
                exit()

            order_cls = datetime.datetime.strptime(str(item_order_date_cls), "%Y-%m-%d")
            delivery_cls = datetime.datetime.strptime(str(item_delivery_date_cls), "%Y-%m-%d")
            day_cls = delivery_cls- order_cls

            status.append(quantity_cls)
            status.append(thickness_cls)
            status.append(width_cls)
            status.append(selling_price_cls)
            status.append(encoded_ct_cls)
            status.append(encode_it_cls)
            status.append(application_cls)
            status.append(product_cls)
            status.append(day_cls.days)

            x_cls = np.array(status).reshape(1, -1)
            pred_status = trained_model_cls.predict(x_cls)
            if pred_status==1:
                st.write(f'Predicted Status : :green[WON]')
            else:
                st.write(f'Predicted Status : :red[LOST]')



