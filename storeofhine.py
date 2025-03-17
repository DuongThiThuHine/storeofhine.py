import streamlit as st
import pandas as pd
import os
import hashlib
import urllib.parse
import datetime

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
    VNPAY_TMNCODE = "YOUR_TMN_CODE"
    VNPAY_HASHSECRET = "YOUR_SECRET_KEY"
    RETURN_URL = "https://storeofhine.streamlit.app"  # URL trang của bạn
    
    # Hàm tạo URL thanh toán VNPAY
    def create_vnpay_url(order_id, amount):
        params = {
            "vnp_Version": "2.1.0",
            "vnp_Command": "pay",
            "vnp_TmnCode": VNPAY_TMNCODE,
            "vnp_Amount": amount * 100,  # VNPAY yêu cầu đơn vị là VND * 100
            "vnp_CreateDate": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "vnp_CurrCode": "VND",
            "vnp_IpAddr": "0.0.0.0",  # Đặt IP mặc định
            "vnp_Locale": "vn",
            "vnp_OrderInfo": f"Thanh toan don hang {order_id}",
            "vnp_OrderType": "other",
            "vnp_ReturnUrl": RETURN_URL,
            "vnp_TxnRef": str(order_id),
        }
    
        # Sắp xếp tham số theo thứ tự alphabet
        sorted_params = sorted(params.items())
        query_string = "&".join(f"{k}={v}" for k, v in sorted_params)
    
        # Tạo chữ ký (signature) để bảo mật
        hash_data = "&".join(f"{k}={v}" for k, v in sorted_params)
        hash_value = hashlib.sha256((VNPAY_HASHSECRET + hash_data).encode()).hexdigest()
    
        # Thêm chữ ký vào URL
        payment_url = f"{VNPAY_URL}?{query_string}&vnp_SecureHash={hash_value}"
        return payment_url
    
    # Hiển thị nút thanh toán
    if st.button("🛒 Thanh toán qua VNPAY"):
        total_amount = 100000  # Định giá đơn hàng (hoặc lấy từ giỏ hàng)
        payment_url = create_vnpay_url(order_id="12345", amount=total_amount)
        st.markdown(f"[Nhấn vào đây để thanh toán](<{payment_url}>)", unsafe_allow_html=True)
