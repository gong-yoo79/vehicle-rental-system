# app.py (Complete Streamlit Vehicle Rental App)

```python
import streamlit as st
import sqlite3
import bcrypt
import os

# ================= CONFIG =================
st.set_page_config(
    page_title="Vehicle Rental System",
    page_icon="🚗",
    layout="wide"
)

# ================= DATABASE =================
conn = sqlite3.connect("vehicle_rental.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

# BOOKINGS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    vehicle TEXT,
    price INTEGER
)
''')

conn.commit()

# ================= CSS =================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #e0f7fa, #e8f5e9);
}

.hero {
    background: linear-gradient(135deg, #14b8a6, #38bdf8);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #14b8a6, #38bdf8);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ================= CAR DATA =================
TOP_SELLING_CARS = [
    {
        "name": "Brezza AT 2024-25",
        "brand": "Maruti",
        "type": "SUV",
        "transmission": "Automatic",
        "price": 3888,
        "rating": 4.5,
        "image": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140113/brezza-exterior-right-front-three-quarter-3.jpeg"
    },
    {
        "name": "Innova Hycross",
        "brand": "Toyota",
        "type": "MUV",
        "transmission": "Automatic",
        "price": 7104,
        "rating": 4.7,
        "image": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115777/innova-hycross-exterior-right-front-three-quarter.jpeg"
    },
    {
        "name": "Hyundai Santro",
        "brand": "Hyundai",
        "type": "Hatchback",
        "transmission": "Manual",
        "price": 2616,
        "rating": 4.2,
        "image": "https://imgd.aeplcdn.com/664x374/n/cw/ec/45951/santro-exterior-right-front-three-quarter.jpeg"
    }
]

# ================= CAR CARD =================
def car_card(car):
    st.image(car["image"], use_container_width=True)

    stars = "⭐" * int(car["rating"])

    st.markdown(f"""
    <div class="card">
        <h3>🚘 {car['name']}</h3>
        <p>🏷 {car['brand']} | 🚙 {car['type']} | ⚙ {car['transmission']}</p>
        <p>{stars} ({car['rating']})</p>
        <h3 style="color:#14b8a6;">₹{car['price']:,} / day</h3>
    </div>
    """, unsafe_allow_html=True)

# ================= LOGIN / SIGNUP =================
if not st.session_state.logged_in:

    st.title("🔐 Vehicle Rental Login")

    mode = st.radio("Choose", ["Login", "Signup"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Signup":

        if st.button("Create Account"):

            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

            try:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?,?,?)",
                    (username, hashed_pw.decode(), "user")
                )

                conn.commit()
                st.success("Account Created Successfully")

            except:
                st.error("Username already exists")

    else:

        if st.button("Login"):

            cursor.execute(
                "SELECT * FROM users WHERE username=?",
                (username,)
            )

            user = cursor.fetchone()

            if user:

                if bcrypt.checkpw(password.encode(), user[2].encode()):

                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()

                else:
                    st.error("Wrong Password")

            else:
                st.error("User Not Found")

    st.stop()

# ================= SIDEBAR =================
st.sidebar.title("🚗 AutoRent Pro")
st.sidebar.write(f"👋 Welcome {st.session_state.username}")

menu = [
    "Dashboard",
    "Top Selling Cars",
    "Book Vehicle",
    "My Bookings"
]

choice = st.sidebar.selectbox("Menu", menu)

# ================= DASHBOARD =================
if choice == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🚗 Premium Car Rentals</h1>
        <p>Luxury • Affordable • Fast Booking</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("🚗 Cars", 3)
    col2.metric("📦 Bookings", 12)
    col3.metric("⭐ Rating", "4.8")

# ================= TOP CARS =================
elif choice == "Top Selling Cars":

    st.title("🔥 Top Selling Cars")

    cols = st.columns(3)

    for i, car in enumerate(TOP_SELLING_CARS):
        with cols[i % 3]:
            car_card(car)

# ================= BOOK VEHICLE =================
elif choice == "Book Vehicle":

    st.title("🚗 Book Your Ride")

    car_names = [car["name"] for car in TOP_SELLING_CARS]

    selected = st.selectbox("Select Vehicle", car_names)

    days = st.slider("Rental Days", 1, 30, 1)

    selected_car = next(car for car in TOP_SELLING_CARS if car["name"] == selected)

    total = selected_car["price"] * days

    st.success(f"Total Price: ₹{total:,}")

    if st.button("Book Now"):

        cursor.execute(
            "INSERT INTO bookings (username, vehicle, price) VALUES (?,?,?)",
            (st.session_state.username, selected, total)
        )

        conn.commit()

        st.success("🎉 Booking Confirmed Successfully")
        st.balloons()

# ================= MY BOOKINGS =================
elif choice == "My Bookings":

    st.title("📦 My Bookings")

    cursor.execute(
        "SELECT vehicle, price FROM bookings WHERE username=?",
        (st.session_state.username,)
    )

    bookings = cursor.fetchall()

    if bookings:

        for booking in bookings:

            st.markdown(f"""
            <div class="card">
                <h3>🚘 {booking[0]}</h3>
                <h4 style="color:#14b8a6;">₹{booking[1]:,}</h4>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No bookings yet")

# ================= LOGOUT =================
if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

```

# requirements.txt

```text
streamlit==1.35.0
bcrypt==4.1.2
```

# Deployment Safe Changes (IMPORTANT)

This app now uses SQLite instead of MySQL.

So you DO NOT need:

* mysql-connector-python
* localhost database
* XAMPP
* phpMyAdmin

SQLite automatically creates:

```text
vehicle_rental.db
```

when app runs on Streamlit Cloud.

This removes deployment database issues completely.

# How to Run

```bash
streamlit run app.py
```

# How to Deploy

1. Upload project to GitHub
2. Open Streamlit Cloud
3. Connect GitHub repo
4. Select app.py
5. Deploy

