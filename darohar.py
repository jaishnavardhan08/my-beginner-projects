import streamlit as st
import pandas as pd
import os
import random
from pathlib import Path

IMAGE_DIR = Path("images")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DHAROHAR - Smart Travel Assistant",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# ============================================================
# FILES & SAMPLE DATA
# ============================================================
HOTEL_FILE = "hotels.csv"
PLACE_FILE = "places.csv"
REGISTRATION_FILE = "hotel_registrations.csv"

hotel_data = [
    {"name": "Golden Heritage Hotel", "city": "Amritsar", "type": "Hotel", "price": 2500, "purpose": "Religious", "hospitality": 5, "food": 4, "view": 4, "cleanliness": 5, "location": 5},
    {"name": "Punjab Palace Resort", "city": "Amritsar", "type": "Resort", "price": 5000, "purpose": "Recreation", "hospitality": 4, "food": 5, "view": 5, "cleanliness": 5, "location": 3},
    {"name": "Seva Dharamshala", "city": "Amritsar", "type": "Dharamshala", "price": 800, "purpose": "Religious", "hospitality": 4, "food": 3, "view": 2, "cleanliness": 4, "location": 5},
    {"name": "Amritsar Homestay", "city": "Amritsar", "type": "Homestay", "price": 1500, "purpose": "Family", "hospitality": 5, "food": 4, "view": 4, "cleanliness": 4, "location": 4},
    {"name": "City Business Inn", "city": "Amritsar", "type": "Hotel", "price": 3200, "purpose": "Business", "hospitality": 4, "food": 5, "view": 3, "cleanliness": 5, "location": 5},
    {"name": "Backpackers Hub", "city": "Amritsar", "type": "Hostel", "price": 900, "purpose": "Recreation", "hospitality": 4, "food": 3, "view": 3, "cleanliness": 4, "location": 5},
    {"name": "Heritage View Hotel", "city": "Amritsar", "type": "Hotel", "price": 2200, "purpose": "Education", "hospitality": 5, "food": 4, "view": 5, "cleanliness": 5, "location": 4}
]
hotel_images = {
    "Golden Heritage Hotel": "goldenheritagehoetel.jpg",
    "Punjab Palace Resort": "images/hotel2.jpg",
    "Seva Dharamshala": "dharamshala.jpg",
    "Amritsar Homestay": "images/hotel1.jpg",
    "City Business Inn": "images/hotel2.jpg",
    "Backpackers Hub": "images/hotel3.jpg",
    "Heritage View Hotel": "hotelheritageview.jpg",
}

place_data = [
    {"name": "Golden Temple", "city": "Amritsar", "category": "Religious", "description": "The famous spiritual centre of Amritsar."},
    {"name": "Jallianwala Bagh", "city": "Amritsar", "category": "Education", "description": "An important historical site in Indian history."},
    {"name": "Partition Museum", "city": "Amritsar", "category": "Education", "description": "A museum documenting the history of the Partition."},
    {"name": "Wagah Border", "city": "Amritsar", "category": "Recreation", "description": "Known for its famous border ceremony."},
    {"name": "Gobindgarh Fort", "city": "Amritsar", "category": "Recreation", "description": "A historic fort with cultural attractions."},
    {"name": "Durgiana Temple", "city": "Amritsar", "category": "Religious", "description": "A beautiful Hindu temple in Amritsar."},
    {"name": "Amritsar Heritage Walk", "city": "Amritsar", "category": "Family", "description": "Explore the historic streets and culture of the city."}
]

if not os.path.exists(HOTEL_FILE):
    pd.DataFrame(hotel_data).to_csv(HOTEL_FILE, index=False)

if not os.path.exists(PLACE_FILE):
    pd.DataFrame(place_data).to_csv(PLACE_FILE, index=False)

hotels = pd.read_csv(HOTEL_FILE)
places = pd.read_csv(PLACE_FILE)

# Initialize Session State Variables
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_idx" not in st.session_state:
    st.session_state.quiz_idx = 0

# ============================================================
# RECOMMENDATION ALGORITHM
# ============================================================
def calculate_recommendations(destination, budget_value, stay_type, purpose, priority):
    filtered = hotels[hotels["city"].str.lower() == destination.lower()].copy()
    if filtered.empty:
        return filtered, []

    scores = []
    for index, hotel in filtered.iterrows():
        score = 0
        if hotel["price"] <= budget_value:
            score += 30
        elif hotel["price"] <= budget_value * 1.2:
            score += 15

        if hotel["type"] == stay_type:
            score += 20
        if hotel["purpose"] == purpose:
            score += 20

        if priority == "Hospitality":
            score += hotel["hospitality"] * 5
        elif priority == "Food":
            score += hotel["food"] * 5
        elif priority == "View":
            score += hotel["view"] * 5
        elif priority == "Cleanliness":
            score += hotel["cleanliness"] * 5
        elif priority == "Location":
            score += hotel["location"] * 5
        elif priority == "Price" and hotel["price"] <= budget_value:
            score += 25

        scores.append((index, score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return filtered, scores

# ============================================================
# NAVIGATION & SIDEBAR
# ============================================================
st.sidebar.markdown('<div class="sidebar-brand">🪷 <span>DHAROHAR</span></div>', unsafe_allow_html=True)
page_choice = st.sidebar.radio(
    "Go to",
    ["🗺️ Home & Plan Trip", "🏨 Register Hotel", "🧠 Culture Quiz", "ℹ️ About"],
    index=["🗺️ Home & Plan Trip", "🏨 Register Hotel", "🧠 Culture Quiz", "ℹ️ About"].index(st.session_state.page if st.session_state.page in ["🗺️ Home & Plan Trip", "🏨 Register Hotel", "🧠 Culture Quiz", "ℹ️ About"] else "🗺️ Home & Plan Trip")
)

# Sync sidebar with session state page selection
st.session_state.page = page_choice

# Language selector in sidebar
st.sidebar.divider()
language = st.sidebar.selectbox("🌐 Language / भाषा", ["🇬🇧 English", "🇮🇳 हिन्दी"])

# ============================================================
# PAGE 1: HOME & PLAN MY TRIP
# ============================================================
if st.session_state.page == "🗺️ Home & Plan Trip":
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">SMART TRAVEL ASSISTANT</div>
        <div class="main-header">🪷 DHAROHAR</div>
        <div class="sub-header">Discover India beyond the map.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🧳 Trip Preferences")
        with st.form("preferences_form"):
            destination = st.selectbox("📍 Where do you want to visit?", ["Amritsar"])
            budget = st.slider("💰 Max Budget per night (₹)", min_value=500, max_value=10000, value=3000, step=100)
            stay = st.selectbox("🏠 Preferred Stay Type", ["Hotel", "Resort", "Homestay", "Dharamshala", "Hostel"])
            purpose = st.selectbox("🎯 Main Purpose", ["Religious", "Education", "Recreation", "Business", "Family"])
            priority = st.selectbox("⭐ Top Priority", ["Hospitality", "Food", "View", "Cleanliness", "Location", "Price"])
            travellers = st.selectbox("👨‍👩‍👧 Travelling With", ["Solo", "Friends", "Family"])
            duration = st.selectbox("🗓️ Duration", ["1-2 days", "3-5 days", "6-10 days", "10+ days"])

            submitted = st.form_submit_button("✨ Find My Recommendations", use_container_width=True)

    with col2:
        if submitted:
            st.subheader("✨ Recommended Stays")
            filtered, scores = calculate_recommendations(destination, budget, stay, purpose, priority)

            if filtered.empty:
                st.warning("No properties available for this destination yet.")
            else:
                for rank, (index, score) in enumerate(scores[:3], start=1):
                    hotel = filtered.loc[index]
                    image_path = hotel_images.get(
    hotel["name"],
    "images/hotel1.jpg"
)
                    percentage = min(int(score), 100)

                    with st.container():
                        st.markdown(f"#### {rank}. {hotel['name']}")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Match Score", f"{percentage}%")
                        c2.metric("Price", f"₹{hotel['price']}/night")
                        c3.metric("Type", hotel['type'])

                        st.progress(percentage / 100)
                        st.caption(f"📍 Location: {hotel['location']}/5 | ⭐ Hospitality: {hotel['hospitality']}/5 | 🍴 Food: {hotel['food']}/5")
                        st.divider()

                st.subheader("📍 Places You May Like")
                matching_places = places[
                    (places["city"].str.lower() == destination.lower()) &
                    ((places["category"] == purpose) | (places["category"] == "Family"))
                ]
                if matching_places.empty:
                    matching_places = places[places["city"].str.lower() == destination.lower()]

                for _, place in matching_places.head(4).iterrows():
                    st.markdown(f"**📍 {place['name']}** *({place['category']})*")
                    st.write(place['description'])
        else:
            st.info("👈 Fill in your travel details on the left and click **'Find My Recommendations'** to see tailored stays and places.")

# ============================================================
# PAGE 2: HOTEL REGISTRATION
# ============================================================
elif st.session_state.page == "🏨 Register Hotel":
    st.markdown('<p class="main-header">🏨 Property Registration</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">List your hotel, resort, or homestay on DHAROHAR.</p>', unsafe_allow_html=True)

    with st.form("hotel_reg_form"):
        col1, col2 = st.columns(2)
        with col1:
            h_name = st.text_input("Hotel Name")
            city = st.text_input("City", value="Amritsar")
            h_type = st.selectbox("Type", ["Hotel", "Resort", "Homestay", "Dharamshala", "Hostel"])
            price = st.number_input("Price per Night (₹)", min_value=100, step=100, value=2000)
        with col2:
            speciality = st.text_input("Speciality")
            food = st.selectbox("Food Option", ["Veg Only", "Non-Veg Available", "Breakfast Included"])
            facilities = st.text_input("Facilities (e.g. WiFi, Pool, Parking)")

        reg_submitted = st.form_submit_button("💾 Save & Register Hotel", use_container_width=True)

        if reg_submitted:
            if not h_name:
                st.error("Please provide a valid hotel name.")
            else:
                data = {
                    "hotel_name": h_name,
                    "city": city,
                    "type": h_type,
                    "price": price,
                    "speciality": speciality,
                    "food": food,
                    "facilities": facilities
                }
                df = pd.DataFrame([data])
                if os.path.exists(REGISTRATION_FILE):
                    df.to_csv(REGISTRATION_FILE, mode="a", header=False, index=False)
                else:
                    df.to_csv(REGISTRATION_FILE, index=False)
                st.success("🎉 Property registered successfully!")

# ============================================================
# PAGE 3: CULTURE QUIZ
# ============================================================
elif st.session_state.page == "🧠 Culture Quiz":
    st.markdown('<p class="main-header">🧠 Amritsar Culture Quiz</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Discover local history, food, and culture!</p>', unsafe_allow_html=True)

    quiz_questions = [
        {"question": "What is another name for the Golden Temple?", "options": ["Harmandir Sahib", "India Gate", "Charminar", "Red Fort"], "answer": "Harmandir Sahib"},
        {"question": "Amritsar is located in which Indian state?", "options": ["Punjab", "Rajasthan", "Gujarat", "Kerala"], "answer": "Punjab"},
        {"question": "Which famous border ceremony takes place near Amritsar?", "options": ["Wagah Border Ceremony", "Republic Day Parade", "Boat Festival", "Desert Festival"], "answer": "Wagah Border Ceremony"},
        {"question": "Which food is strongly associated with Punjabi cuisine?", "options": ["Chole Bhature", "Dhokla", "Idli", "Appam"], "answer": "Chole Bhature"},
        {"question": "Which drink is popular in Punjab?", "options": ["Sweet Lassi", "Kahwa", "Filter Coffee", "Sol Kadhi"], "answer": "Sweet Lassi"}
    ]

    with st.form("quiz_form"):
        score = 0
        answers = {}
        for idx, q in enumerate(quiz_questions):
            st.write(f"**Q{idx+1}. {q['question']}**")
            answers[idx] = st.radio("Select an answer:", q["options"], key=f"q_{idx}")
            st.divider()

        quiz_submitted = st.form_submit_button("Submit Answers", use_container_width=True)

        if quiz_submitted:
            for idx, q in enumerate(quiz_questions):
                if answers[idx] == q["answer"]:
                    score += 1

            st.balloons()
            st.success(f"🎉 Quiz Completed! Your Score: **{score} / {len(quiz_questions)}**")

# ============================================================
# PAGE 4: ABOUT
# ============================================================
elif st.session_state.page == "ℹ️ About":
    st.markdown('<p class="main-header">ℹ️ About DHAROHAR</p>', unsafe_allow_html=True)

    st.info("""
    **DHAROHAR** is a smart travel assistant designed to make travelling personal and meaningful.
    
    It considers:
    * 💰 **Budget & Rates**
    * 🏠 **Stay Preferences**
    * 🎯 **Purpose of Travel**
    * ⭐ **Specific Hotel Ratings** (Food, Location, Cleanliness)
    * 👨‍👩‍👧 **Group Dynamics**
    
    It recommends customized hotels and destinations, lets hoteliers register properties directly, and tests user local awareness via culture quizzes.
    """)
