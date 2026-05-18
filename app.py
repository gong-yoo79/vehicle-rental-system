import streamlit as st
import bcrypt
import matplotlib.pyplot as plt
import os
from db import connect_db



params = st.query_params

if not st.session_state.get("logged_in"):
    if "user_id" in params and "role" in params:
        st.session_state.logged_in = True
        st.session_state.user_id = int(params["user_id"])
        st.session_state.role = params["role"]

if "page" in params:
    st.session_state.page = params["page"]        
        

if "selected_vehicle" not in st.session_state:
    st.session_state.selected_vehicle = None

if "booking_done_for" not in st.session_state:
    st.session_state.booking_done_for = None

st.markdown("""
<style>
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    transition: 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* Better spacing */
.card {
    padding: 20px;
    border-radius: 18px;
    background: white;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

/* Hover effect */
.card:hover {
    transform: translateY(-5px);
    transition: 0.3s;
}

/* Section titles */
h2, h3 {
    font-weight: 600;
}

/* Buttons spacing */
.stButton {
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)



# ================== CONFIG ==================
st.set_page_config(page_title="Vehicle Rental", page_icon="🚗", layout="wide")

st.markdown("""
<style>

/* ===== GLOBAL BACKGROUND (LIGHT MODE) ===== */
.stApp {
    background: linear-gradient(135deg, #e0f7fa, #e8f5e9);
    color: #0f172a;
}

/* ===== SIDEBAR (Clean Light Glass) ===== */
section[data-testid="stSidebar"] {
    background: #f8fffd;
    border-right: 1px solid #cce7e2;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

/* ===== HERO CARD (SeaGreen + Light Blue) ===== */
.hero {
    background: linear-gradient(135deg, #2dd4bf, #38bdf8);
    padding: 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.12);
}

/* ===== MODERN CARDS ===== */
.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #dbeafe;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.10);
}

/* ===== BUTTONS (Fresh Gradient) ===== */
.stButton>button {
    background: linear-gradient(90deg, #14b8a6, #38bdf8);
    color: white;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #0d9488, #0ea5e9);
}

/* ===== METRICS (Light Cards) ===== */
[data-testid="metric-container"] {
    background: #ffffff;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* ===== TEXT INPUT CLEAN STYLE ===== */
input, textarea {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
}

/* ===== REMOVE DARK FEEL COMPLETELY ===== */
.css-1d391kg, .css-12oz5g7 {
    background-color: transparent !important;
}

</style>
""", unsafe_allow_html=True)
# ================== THEME (STEP C HERE) ==================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    bg = "#0e1117"
    card = "#1a1c23"
    text = "white"
else:
    bg = "white"
    card = "white"
    text = "black"


# ================== DB ==================
conn = connect_db()
cursor = conn.cursor()

# ================== SESSION ==================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""
    st.session_state.user_id = None
    
# ================== DARK MODE STATE ==================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False    

# ================== TOP CARS ==================
TOP_SELLING_CARS = [
    {
        "name": "Brezza AT 2024-25",
        "brand": "Maruti",
        "type": "SUV",
        "transmission": "Automatic",
        "price": 3888,
        "rating": 4.5,
        "image": "assets/brezza.jpg"
    },
    {
        "name": "Innova Hycross",
        "brand": "Toyota",
        "type": "MUV",
        "transmission": "Automatic",
        "price": 7104,
        "rating": 4.7,
        "image": "assets/innova.jpg"
    },
    {
        "name": "Hyundai Santro",
        "brand": "Hyundai",
        "type": "Hatchback",
        "transmission": "Manual",
        "price": 2616,
        "rating": 4.2,
        "image": "assets/santro.jpg"
    }
]
def car_card(car):
    st.image(car["image"], width="stretch")

    stars = "⭐" * int(car["rating"])

    st.markdown(f"""
    ### 🚘 {car['name']}
    🏷 {car['brand']} | 🚙 {car['type']} | ⚙ {car['transmission']}

    {stars} ({car['rating']})

    ### 💰 ₹{car['price']:,} / day
    """)


# ================== ADMIN GUARD ==================
def admin_only():
    if st.session_state.role != "admin":
        st.error("⛔ Access Denied: Admin only page")
        st.stop()

# ================== LOGIN UI ==================
if not st.session_state.logged_in:

    # ===== TOP BRAND NAME =====
    st.markdown("""
    <h1 style='text-align:center; margin-bottom:20px;'>
        🚗 Premium Car Rentals
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .auth-card {
        background: rgba(255,255,255,0.95);
        padding: 35px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
    }
    .title {
        font-size: 26px;
        font-weight: 700;
        color: #111827;
    }
    .subtitle {
        color: #6b7280;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ✅ CREATE COLUMNS INSIDE IF
    left, right = st.columns([1.2, 1])

    # ===== LEFT IMAGE =====
    with left:
        st.markdown("""
        <div style="
            background-image: url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7');
            height: 520px;
            background-size: cover;
            background-position: center;
            border-radius: 20px;
            position: relative;
        ">
            <div style="
                position:absolute;
                top:0;
                left:0;
                width:100%;
                height:100%;
                background: rgba(0,0,0,0.45);
                border-radius:20px;
            "></div>

            
        </div>
        """, unsafe_allow_html=True)

    # ===== RIGHT LOGIN =====
    with right:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        st.markdown('<div class="title">Welcome Back 👋</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Login to continue</div>', unsafe_allow_html=True)

        mode = st.radio("Mode", ["Sign In", "Sign Up"], horizontal=True)

        # LOGIN
        if mode == "Sign In":

            role = st.radio("Login as", ["Admin", "Customer"], horizontal=True)

            username = st.text_input("Username / Email", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("🚀 Login", key="login_btn"):

                db_role = "admin" if role == "Admin" else "user"

                cursor.execute(
                    "SELECT * FROM users WHERE username=%s AND role=%s",
                    (username, db_role)
                )
                user = cursor.fetchone()

                if user:
                    stored_hash = user[2]

                    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.session_state.role = user[3]
                        
                        st.query_params["user_id"] = user[0]
                        st.query_params["role"] = user[3]

                        
                        st.success("Login Successful ✅")
                        st.rerun()
                    else:
                        st.error("Invalid password")
                else:
                    st.error("User not found")




        # SIGNUP
        else:
            name = st.text_input("Full Name", key="su_name")
            email = st.text_input("Email", key="su_email")
            mobile = st.text_input("Mobile", key="su_mobile")
            password = st.text_input("Password", type="password", key="su_pass")

            if st.button("✨ Sign Up", key="signup_btn"):

                if name == "" or email == "" or password == "":
                    st.warning("Fill all required fields")
                    st.stop()

                hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

                cursor.execute(
                    "INSERT INTO users (username, password, role, email, mobile) VALUES (%s,%s,%s,%s,%s)",
                    (email, hashed_pw, "user",email,mobile)
                )
                
                conn.commit()

                st.success("Account Created 🎉")
                st.info("Now login")

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ================== SIDEBAR ==================
st.sidebar.markdown("## 🚗 CarRent")


# MENU
if st.session_state.role == "admin":
    menu = ["Dashboard", "Admin Dashboard"]
else:
    menu = ["Dashboard", "View Vehicles", "Wishlist", "My Bookings"]

# INIT PAGE
if "page" not in st.session_state:
    st.session_state.page = menu[0]

# 🔥 FIX: ensure page is valid
if st.session_state.page not in menu:
    st.session_state.page = menu[0]

# SIDEBAR-radio button
selected = st.sidebar.radio(
    "Menu",
    menu,
    index=menu.index(st.session_state.page)
)
if selected != st.session_state.page:
    st.session_state.page = selected
    st.query_params["page"] = selected   # 🔥 IMPORTANT
    st.rerun()

# ================== DASHBOARD ==================
# ================== DASHBOARD ==================
if st.session_state.page == "Dashboard":

    # ================= ADMIN =================
    if st.session_state.role == "admin":

        st.markdown("## 🛠 Admin Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        cursor.execute("SELECT COUNT(*) FROM vehicles")
        vehicles = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM bookings")
        bookings = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total_price) FROM bookings")
        revenue = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM users")
        users = cursor.fetchone()[0]

        col1.metric("🚗 Vehicles", vehicles)
        col2.metric("📦 Bookings", bookings)
        col3.metric("💰 Revenue", f"₹{revenue}")
        col4.metric("👤 Users", users)

    # ================= CUSTOMER =================
    else:

        st.markdown("## 👋 Welcome Back")

        st.markdown("""
        <div class="hero">
            <h2>🚗 Book Your Ride</h2>
            <p>Fast • Affordable • Premium Cars</p>
        </div>
        """, unsafe_allow_html=True)

        # ===== STATS =====
        col1, col2 = st.columns(2)

        cursor.execute(
            "SELECT COUNT(*) FROM bookings WHERE user_id=%s",
            (st.session_state.user_id,)
        )
        my_bookings = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM wishlist WHERE user_id=%s",
            (st.session_state.user_id,)
        )
        wishlist = cursor.fetchone()[0]

        col1.metric("📦 My Bookings", my_bookings)
        col2.metric("❤️ Wishlist", wishlist)

        st.divider()

        # ===== ✅ QUICK ACTIONS (CORRECT PLACE) =====
        st.markdown("### 🚀 Quick Actions")

        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("🚗 Browse Cars"):
                st.session_state.page = "View Vehicles"
                st.query_params["page"] = "View Vehicles"
                st.rerun()

        with c2:
            if st.button("📦 My Bookings"):
                st.session_state.page = "My Bookings"
                st.query_params["page"] = "My Bookings"
                st.rerun()

        with c3:
            if st.button("❤️ Wishlist"):
                st.session_state.page = "Wishlist"
                st.query_params["page"] = "Wishlist"
                st.rerun()

        st.divider()

        # ===== ✅ TOP CARS =====
        st.subheader("🔥 Trending Cars Near You")

        cols = st.columns(3)

        for i, car in enumerate(TOP_SELLING_CARS):
            with cols[i % 3]:
                st.image(car["image"], width="stretch")

                stars = "⭐" * int(car["rating"])

                st.markdown(f"""
                <div class="card">
                    <h4>{car['name']}</h4>
                    <p>{car['brand']} • {car['type']}</p>
                    <p>{stars} ({car['rating']})</p>
                    <h4 style="color:#14b8a6;">₹{car['price']:,} / day</h4>
                </div>
                """, unsafe_allow_html=True)
                





# ================== ADMIN DASHBOARD ==================
elif st.session_state.page == "Admin Dashboard":

    admin_only()

    st.markdown("## 📊 Advanced Admin Analytics")

    # ===== TOP METRICS =====
    col1, col2, col3 = st.columns(3)

    cursor.execute("SELECT SUM(total_price) FROM bookings")
    revenue = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM bookings")
    bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    col1.metric("💰 Revenue", f"₹{revenue}")
    col2.metric("📦 Bookings", bookings)
    col3.metric("👤 Users", users)

    st.divider()

    # ===== VEHICLE PIE =====
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚗 Vehicle Distribution")

        cursor.execute("SELECT type, COUNT(*) FROM vehicles GROUP BY type")
        data = cursor.fetchall()

        if data:
            labels = [x[0] for x in data]
            sizes = [x[1] for x in data]

            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')
            st.pyplot(fig)

    with col2:
        st.subheader("📊 Bookings per Vehicle")

        cursor.execute("""
            SELECT v.name, COUNT(b.id)
            FROM bookings b
            JOIN vehicles v ON v.id=b.vehicle_id
            GROUP BY v.name
        """)
        data = cursor.fetchall()

        if data:
            names = [x[0] for x in data]
            counts = [x[1] for x in data]

            fig, ax = plt.subplots()
            ax.bar(names, counts)
            st.pyplot(fig)

    st.divider()

    # ===== USERS TABLE (FINAL CLEAN VERSION) =====
    st.subheader("👥 System Users Management")

    cursor.execute("""
        SELECT 
            u.username,
            COALESCE(GROUP_CONCAT(DISTINCT v.name SEPARATOR ', '), 'No Booking') AS vehicles,
            COALESCE(SUM(b.total_price), 0) AS total_spent,
            COALESCE(GROUP_CONCAT(
                CONCAT(DATE(b.start_date), ' to ', DATE(b.end_date))
                SEPARATOR ' | '
            ), 'No Dates') AS booking_dates
        FROM users u
        LEFT JOIN bookings b ON u.id = b.user_id
        LEFT JOIN vehicles v ON v.id = b.vehicle_id
        GROUP BY u.id
    """)


    data = cursor.fetchall()

    if data:
        import pandas as pd
        df = pd.DataFrame(data, columns=["User", "Booked Vehicles", "💰 Total Spent",
        "📅 Booking Dates"
])
        st.dataframe(df, width="stretch")
    else:
        st.warning("No users found")
                
                
                
if "selected_vehicle" not in st.session_state:
    st.session_state.selected_vehicle = None                
#=============view vehicles=================                
elif st.session_state.page == "View Vehicles":

    st.title("🚗 Explore & Book Vehicles")

    import os

    cursor.execute("SELECT * FROM vehicles")
    vehicles = cursor.fetchall()

    for i, v in enumerate(vehicles):
        vid, name, v_type, price, available, rating, image_url, seats, image = v

        st.markdown("---")

        col1, col2 = st.columns([1, 2])

        # ===== IMAGE =====
        with col1:
            if image and os.path.exists(image):
                st.image(image, width="stretch")
            else:
                st.image("https://via.placeholder.com/300x200?text=Car", width="stretch")

        # ===== DETAILS =====
        with col2:
            st.markdown(f"""
            <div class="card">
                <h3>🚗 {name.title()}</h3>
                <p>🚘 Type: {v_type}</p>
                <h4 style="color:#14b8a6;">₹{price:,} / day</h4>
            </div>
            """, unsafe_allow_html=True)

            # ✅ SHOW SUCCESS ONLY FOR THAT CAR
            if st.session_state.get("booking_done_for") == vid:
                st.success(f"🎉 {name} booked successfully!")
                #st.balloons()
                st.session_state.booking_done_for = None

            
            # ===== BUTTONS =====
            colA, colB = st.columns(2)

            with colA:
                if st.button("❤️ Wishlist", key=f"wish{vid}"):
                    # 🔥 PREVENT DUPLICATE WISHLIST
                    cursor.execute("""
                        SELECT 1 FROM wishlist 
                        WHERE user_id=%s AND vehicle_id=%s
                    """, (st.session_state.user_id, vid))

                    if cursor.fetchone():
                        st.warning("Already in wishlist ❤️")
                    else:

                    
                    
                        cursor.execute(
                            "INSERT INTO wishlist (user_id, vehicle_id) VALUES (%s,%s)",
                            (st.session_state.user_id, vid)
                        )
                        conn.commit()
                        st.success("Added to wishlist ❤️")
            #BOOK BUTTON
            with colB:
                if st.button("📅 Book Now", key=f"open{vid}"):
                    st.session_state.selected_vehicle = vid
            # BOOK PANEL
            if st.session_state.get("selected_vehicle") == vid:

                st.markdown("### 📅 Select Dates")

                start = st.date_input("Start Date", key=f"start_{vid}")
                end = st.date_input("End Date", key=f"end_{vid}")

                if start and end and end >= start:

                    days = max((end - start).days,1)
                    total = price * days

                    st.success(f"💰 Total Price: ₹{total}")
                    payment = st.radio(
                        "💳 Payment Method",
                        ["UPI", "Card", "Cash"],
                        key=f"pay{vid}_{i}")
                        
                    if st.button("🚀 Confirm Booking", key=f"book{vid}_{i}"):

                        # 🔥 FETCH USER DATA
                        cursor.execute(
                            "SELECT username, mobile FROM users WHERE id=%s",
                            (st.session_state.user_id,)
                        )
                        user_data = cursor.fetchone()

                        customer_name = user_data[0] if user_data else "Guest"
                        customer_phone = user_data[1] if user_data else ""

                        # INSERT BOOKING
                        cursor.execute("""
                            INSERT INTO bookings 
                            (vehicle_id, user_id, customer_name, customer_phone, start_date, end_date, total_price)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                        """, (
                            vid,
                            st.session_state.user_id,
                            customer_name,
                            customer_phone,
                            start,
                            end,
                            total
                        ))

                        # mark unavailable
                        cursor.execute(
                            "UPDATE vehicles SET available=0 WHERE id=%s",
                            (vid,)
                        )

                        conn.commit()

                        # ✅ SUCCESS STATE
                        st.session_state.booking_done_for = vid
                        st.session_state.selected_vehicle = None
                        
                        st.rerun()

                else:
                    st.warning("⚠️ Select valid dates")

#==========================wishlist==========================
elif st.session_state.page == "Wishlist":

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="font-size:28px;">❤️</div>
        <div>
            <h2 style="margin:0;">Wishlist</h2>
            <p style="margin:0;color:gray;">Saved Cars</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("""
        SELECT v.id, v.name, v.type, v.price_per_day
        FROM vehicles v
        JOIN wishlist w ON v.id=w.vehicle_id
        WHERE w.user_id=%s
    """, (st.session_state.user_id,))

    data = cursor.fetchall()

    if not data:
        st.info("No items in wishlist ❤️")

    else:
        for vid, name, v_type, price in data:

            col1, col2 = st.columns([3, 1])

            # DETAILS
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>🚗 {name.title()}</h3>
                    <p>🚘 {v_type}</p>
                    <h4 style="color:#14b8a6;">₹{price:,} / day</h4>
                </div>
                """, unsafe_allow_html=True)

            # ACTIONS
            with col2:
                if st.button("🧺 Book", key=f"wish_book{vid}"):
                    st.success("Go to View Vehicles to book 🚀")

                if st.button("💔 Remove", key=f"remove{vid}"):
                    cursor.execute(
                        "DELETE FROM wishlist WHERE user_id=%s AND vehicle_id=%s",
                        (st.session_state.user_id, vid)
                    )
                    conn.commit()
                    st.rerun()
#=================My Bookings===============
elif st.session_state.page == "My Bookings":

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="font-size:28px;">🧺</div>
        <div>
            <h2 style="margin:0;">My Bookings</h2>
            <p style="margin:0;color:gray;">Your Orders</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cursor.execute("""
        SELECT v.name, b.total_price
        FROM bookings b
        JOIN vehicles v ON v.id=b.vehicle_id
        WHERE b.user_id=%s
    """, (st.session_state.user_id,))

    data = cursor.fetchall()

    if not data:
        st.info("No bookings yet 🚗")

    else:
        for i, (name, price) in enumerate(data):

            col1, col2 = st.columns([3, 1])

            # DETAILS
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>🚗 {name.title()}</h3>
                    <p>Booking ID: #{i+1}</p>
                    <h4 style="color:#14b8a6;">₹{price:,}</h4>
                </div>
                """, unsafe_allow_html=True)

            # ACTIONS
            with col2:
                if st.button("📄 Invoice", key=f"inv{i}"):
                    st.success("Invoice feature coming soon")

                if st.button("❌ Cancel", key=f"cancel{i}"):
                    st.warning("Cancel feature coming soon")
# ================== LOGOUT ==================
if st.sidebar.button("Logout"):
    st.session_state.clear()   # 🔥 clears everything
    st.query_params.clear()  # 🔥 removes user_id from URL
    st.rerun()
