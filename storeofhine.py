import streamlit as st
import pandas as pd
import os

# Kiểm tra tệp CSV có tồn tại không
file_path = 'san_pham_tien_loi_100.csv'
if not os.path.exists(file_path):
    st.error("⚠️ Error: File 'san_pham_tien_loi_100.csv' not found. Please upload it to GitHub.")
else:
    # Load the product data
    df_products = pd.read_csv(file_path, encoding='latin1')

    # Kiểm tra cột có tồn tại không
    st.write("🛠️ Debugging Columns:", df_products.columns)

    # Initialize session state for cart
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # Title of the web page
    st.title("🛍️ Product List")

    # Loop through the products and display them
    for index, row in df_products.iterrows():
        # Kiểm tra nếu cột 'Product' có tồn tại
        if 'Product' not in row:
            continue  # Bỏ qua nếu không có dữ liệu sản phẩm
        
        st.subheader(row['Product'])
        st.write(f"💰 Price: {row.get('Price (VND)', 'N/A')} VND")
        st.write(f"📦 Category: {row.get('Product Type', 'Unknown')}")

        # Hiển thị ảnh sản phẩm (kiểm tra nếu đường dẫn hợp lệ)
        if isinstance(row.get('Image', ''), str) and row['Image'].startswith('http'):
            st.image(row['Image'], caption=row['Product'], use_column_width=True)
        else:
            st.warning("🚫 No image available for this product.")

        # Kiểm tra nếu 'ID' tồn tại, nếu không sử dụng index để tránh lỗi
        key_value = row['ID'] if 'ID' in row else f"cart_{index}"
        
        if st.button(f"🛒 Add {row['Product']} to Cart", key=key_value):
            st.session_state.cart.append(row['Product'])
            st.success(f"{row['Product']} added to your cart!")

    # Display Cart in Sidebar
    st.sidebar.header("🛒 Your Cart")
    if st.session_state.cart:
        st.sidebar.write(", ".join(st.session_state.cart))
    else:
        st.sidebar.write("Your cart is empty.")
