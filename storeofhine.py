import streamlit as st
import pandas as pd
import os
import hashlib
import urllib.parse
import requests

# Kiểm tra tệp CSV có tồn tại không
file_path = 'san_pham_tien_loi_100.csv'
if not os.path.exists(file_path):
    st.error("⚠️ Error: File 'san_pham_tien_loi_100.csv' not found. Please upload it to GitHub.")
else:
    # Load the product data
    df_products = pd.read_csv(file_path, encoding='latin1')


    # Initialize session state for cart
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # Title of the web page
    st.title("🛍️ Products are available at our convenience store, please feel free to shop.")

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
            st.image(row['Image'], caption=row['Product'], use_container_width=True)
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
        
    # Product Payment
    
    # Cấu hình VNPAY API
    VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
    VNPAY_TMNCODE = "AAHR0SYM"
    VNPAY_HASHSECRET = "7I1TU9VLX9UJ8LYXX4SGKBBGN3BIS9LD"
    RETURN_URL = "https://storeofhine.streamlit.app"  # URL trang của bạn
    
    # Hàm tạo URL thanh toán VNPAY
    def create_payment_url(order_id, amount):
        params = {
            "vnp_Version": "2.1.0",
            "vnp_Command": "pay",
            "vnp_TmnCode": VNPAY_TMN_CODE,
            "vnp_Amount": int(amount) * 100,  # Chuyển đổi sang đơn vị VNĐ
            "vnp_CurrCode": "VND",
            "vnp_TxnRef": order_id,
            "vnp_OrderInfo": f"Thanh toán đơn hàng {order_id}",
            "vnp_Locale": "vn",
            "vnp_ReturnUrl": VNPAY_RETURN_URL,
            "vnp_CreateDate": "20250317120000",  # Định dạng YYYYMMDDHHmmss
        }
        
        # Sắp xếp tham số theo thứ tự alphabet
        sorted_params = sorted(params.items())
        query_string = urllib.parse.urlencode(sorted_params)
    
        # Tạo chuỗi chữ ký HMAC SHA512
        sign_data = query_string + VNPAY_HASH_SECRET
        secure_hash = hashlib.sha512(sign_data.encode()).hexdigest()
        
        # Tạo URL thanh toán
        payment_url = f"{VNPAY_URL}?{query_string}&vnp_SecureHash={secure_hash}"
        return payment_url
    
    # Giao diện Streamlit
    st.title("Cửa hàng trực tuyến - Thanh toán VNPAY")
    
    # Nhập thông tin đơn hàng
    order_id = st.text_input("Nhập mã đơn hàng", "123456")
    amount = st.number_input("Nhập số tiền thanh toán (VND)", min_value=1000, value=50000, step=1000)
    
    # Nút tạo thanh toán
    if st.button("Tạo thanh toán"):
        payment_url = create_payment_url(order_id, amount)
        st.success("Click vào nút bên dưới để thanh toán:")
        st.markdown(f"[🔗 Thanh toán ngay]({payment_url})", unsafe_allow_html=True)
