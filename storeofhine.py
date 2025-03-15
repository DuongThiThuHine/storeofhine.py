import streamlit as st
import pandas as pd

# Load the product data
df_products = pd.read_csv('san_pham_tien_loi_100.csv', encoding='latin1')

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Title of the web page
st.title("Product List")

# Loop through the products and display them
for index, row in df_products.iterrows():
    st.subheader(row['Product'])
    st.write(f"Price: {row['Price (VND)']} VND")
    st.write(f"Category: {row['Product Type']}")
    st.image(row['Image'], caption=row['Product'], use_container_width=True)
    
    # Add unique key for each button to avoid StreamlitDuplicateElementId error
    if st.button(f"Add {row['Product']} to Cart", key=row['ID']):
        st.session_state.cart.append(row['Product'])
        st.success(f"{row['Product']} added to your cart!")

# Display Cart in Sidebar
st.sidebar.header("🛒 Your Cart")
if st.session_state.cart:
    st.sidebar.write(", ".join(st.session_state.cart))
else:
    st.sidebar.write("Your cart is empty.")
