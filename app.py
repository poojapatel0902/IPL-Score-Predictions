

# import streamlit as st
# import pickle
# import pandas as pd
# import numpy as np
# import base64

# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as file:
#         encoded_string = base64.b64encode(file.read()).decode()
#     st.markdown(
# f"""
#     <style>
#     /* 1. BACKGROUND IMAGE */
#     .stApp::before {{
#         content: "";
#         background-image: url(data:image/{"png"};base64,{encoded_string});
#         background-size: cover;
#         background-attachment: fixed;
#         background-position: center top;
#         position: fixed;
#         top: 0; left: 0; right: 0; bottom: 0;
#         filter: blur(0.5px); 
#         z-index: -1;
#     }}
#     .stApp {{ background: transparent; }}

#     /* 2. HEADING (TITLE) */
#     h1 {{
#         font-size: 65px !important; 
#         color: #F7CB1B !important; /* Gold */
#         text-align: center;
#         text-shadow: 3px 3px 6px #000000;
#     }}

#     /* 3. BAAKI NORMAL TEXT (Labels jaise 'Select City') */
#     p, label {{
#         color:black !important; /* Dark / Black */
#         font-size: 20px !important;
#         font-weight: bold;
#     }}

#     /* 4. SAARE DABBE AUR MENU (Ekdum Safed, BINA BORDER KE) */
#     div[data-baseweb="select"] > div, 
#     div[data-testid="stNumberInputContainer"],
#     ul[role="listbox"] {{
#         background-color: rgba(255, 255, 255, 0.6) !important; /* <--- Dabbe ekdum safed */
#         border: none !important;            /* <--- KOI BORDER NAHI HAI */
#         border-radius: 8px !important; 
#     }}

#     /* 5. DABBO KE ANDAR KA TEXT (Black Color) */
#     input, 
#     div[data-baseweb="select"] span, 
#     li[role="option"] {{
#         color: black !important; /* <--- Text ekdum kaala */
#         font-size: 18px !important; 
        
#     }}

#     /* Dropdown list par mouse le jane par halka grey effect (taaki pata chale kya select ho raha hai) */
#     li[role="option"]:hover {{
#         background-color: #E0E0E0 !important; 
#         color: black !important;
#     }}

#     /* 6. PREDICT BUTTON (Simple, Bina Border, Bina Hover) */
#     div.stButton > button {{
#         background-color: white !important;
#         color: #F7CB1B !important; /* Gold Text */
#         font-size: 24px !important;
#         font-weight: bold !important;
#         font-color:black;
#         border: none !important; /* <--- Button par bhi koi border nahi */
#         border-radius: 8px !important;
#         width: 100%;
#         height: 55px;
#         margin-top: 15px;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )

# try:
#     add_bg_from_local('image1.jpg') 
# except FileNotFoundError:
#     st.warning("Background image nahi mili! Kripya image ka naam aur folder check karein.")

# # 1. Trained Model ko load karna (Dhyaan rahe 'pipe.pkl' isi folder mein ho)
# pipe = pickle.load(open('pipe.pkl', 'rb'))

# # 2. IPL Teams ki list
# teams = [
#     'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 
#     'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians', 
#     'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bangalore', 
#     'Sunrisers Hyderabad'
# ]

# # 3. IPL Cities ki list
# cities = [
#     'Ahmedabad', 'Bengaluru', 'Chandigarh', 'Chennai', 'Delhi', 
#     'Dharamsala', 'Hyderabad', 'Jaipur', 'Kolkata', 'Lucknow', 
#     'Mumbai', 'Pune', 'Visakhapatnam'
# ]

# # 4. Website ka Title aur Design
# st.title('🏏 IPL Score Predictor')

# col1, col2 = st.columns(2)

# with col1:
#     batting_team = st.selectbox('Select Batting Team', sorted(teams))
# with col2:
#     bowling_team = st.selectbox('Select Bowling Team', sorted(teams))

# city = st.selectbox('Select City', sorted(cities))



# col3, col4, col5 = st.columns(3)

# with col3:
#     current_score = st.number_input('Current Score', min_value=0, step=1)
# with col4:
#     overs = st.number_input('Overs Bowled (e.g., 5.3)', min_value=5.0, max_value=19.5, step=0.1)
# with col5:
#     wickets = st.number_input('Wickets Fallen', min_value=0, max_value=9, step=1)

# last_5_over = st.number_input('Runs scored in last 5 overs', min_value=0, step=1)

# # 5. Prediction Logic (Jab user button dabaye)
# if st.button('Predict Score'):
#     if batting_team == bowling_team:
#         st.error("Batting and Bowling team cannot be the same! Please select different teams.")
#     else:
#         # Overs ko balls mein convert karna (e.g., 5.3 overs = 33 balls)
#         overs_completed = int(overs)
#         balls_in_current_over = int(round((overs - overs_completed) * 10))
#         balls_bowled = (overs_completed * 6) + balls_in_current_over
        
#         # Model ke liye zaroori features calculate karna
#         balls_left = 120 - balls_bowled
#         wickets_left = 10 - wickets
        
#         current_run_rate = 0
#         if balls_bowled > 0:
#             current_run_rate = (current_score * 6) / balls_bowled

#         # DataFrame tayyar karna (Model ko yahi format chahiye)
#         input_df = pd.DataFrame({
#             'batting_team': [batting_team],
#             'bowling_team': [bowling_team],
#             'city': [city],
#             'current_score': [current_score],
#             'balls_left': [balls_left],
#             'wickets_left': [wickets_left],
#             'current_run_rate': [current_run_rate],
#             'last_5_over': [last_5_over]
#         })

#         # Score Predict karna
#         result = pipe.predict(input_df)
#         predicted_score = int(result[0])
        
#         # Final Score Screen par dikhana
#         st.success(f"🏆 Predicted Final Score: {predicted_score}")


import streamlit as st
import pickle
import pandas as pd
import base64
import time
import streamlit.components.v1 as components


# ---------------- BACKGROUND FUNCTION ---------------- #
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()

    # Dhyan dein: st.markdown ke aage 4 spaces (1 Tab) zaroori hai
    st.markdown(
        f"""
        <style>
        /* 1. BACKGROUND IMAGE */
        .stApp::before {{
            content: "";
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-attachment: fixed;
            background-position: center top;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            filter: blur(2px); 
            z-index: -1;
        }}
        .stApp {{ background: transparent; }}

        /* 2. HEADING (TITLE) */
        h1 {{
            font-size: 65px !important; 
            color: #FFD700!important; 
            text-align: center;
            text-shadow: 3px 3px 6px #000000;
        }}

        /* 3. BAAKI NORMAL TEXT (Labels) */
        p, label {{
            color: #F55C92!important; 
            font-size: 23px !important;
            font-weight: bold;
        }}

        /* 4. SAARE DABBE (Outer Box) KI TRANSPARENCY */
        div[data-baseweb="select"] > div, 
        div[data-testid="stNumberInputContainer"],
        ul[role="listbox"] {{
            background-color: rgba(255, 255, 255, 0.4) !important;
            border: none !important;            
            border-radius: 8px !important; 
        }}

        /* 5. ANDAR KE CHHUPE HUE SAFED RANG KO GAYAB KARNA */
        div[data-baseweb="input"],
        div[data-baseweb="base-input"],
        div[data-baseweb="input"] > div,
        input, 
        div[data-baseweb="select"] span, 
        li[role="option"] {{
            background-color: transparent !important; 
            color: black !important; 
            font-size: 20px !important; 
            
            border: none !important;
            box-shadow: none !important;
        }}

        /* 6. YAHAN SE + AUR - BUTTONS POORI TARAH GAYAB HONGE */
        div[data-testid="stNumberInputContainer"] button {{
            display: none !important; 
        }}

        /* Dropdown list par mouse le jane par effect */
        li[role="option"]:hover {{
            background-color: rgba(0, 0, 0, 0.4) !important; 
            color: black !important;
        }}

        /* 7. PREDICT BUTTON */
        div.stButton > button {{
            background-color: rgba(255, 215, 0, 0.4) !important; 
            color: #000000 !important; 
            font-size: 24px !important;
            font-weight: bold !important;
            border: none !important; 
            border-radius: 8px !important;
            width: 100%;
            height: 55px;
            margin-top: 15px;
        }}
/* 8. PAGE KO "MEDIUM" WIDTH DENA */
        .block-container {{
            max-width: 1050px !important; /* <--- YAHAN SE AAP PAGE KI CHAUDHAAI SET KAR SAKTE HAIN */
            padding-top: 10rem !important;
            padding-bottom: 2rem !important;
        }}
        
        </style>
        """,
        unsafe_allow_html=True
    )

# Uske baad function ko call karna hai bina space ke


# ---------------- LOAD BACKGROUND ---------------- #
add_bg_from_local("image.jpg")
# ---------------- LOAD MODEL ---------------- #
# ---------------- LOAD MODEL ---------------- #
pipe = pickle.load(open("pipe.pkl", "rb"))

# ---------------- DATA ---------------- #
teams = [
    'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans',
    'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians',
    'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

cities = [
    'Ahmedabad', 'Bengaluru', 'Chandigarh', 'Chennai', 'Delhi',
    'Dharamsala', 'Hyderabad', 'Jaipur', 'Kolkata', 'Lucknow',
    'Mumbai', 'Pune', 'Visakhapatnam'
]

# --- NAYA MAGIC TRICK: RESET COUNTER ---
# Yeh Streamlit ko batayega ki dabbo ka naya ID kya rakhna hai
if "reset_count" not in st.session_state:
    st.session_state["reset_count"] = 0

rk = st.session_state["reset_count"]

# ---------------- UI ---------------- #
st.title("🏏 IPL Score Predictor")

col1, col2 = st.columns(2)

# Har dabbe ke key mein humne "_rk" (reset counter) jod diya hai
with col1:
    batting_team = st.selectbox("Select Batting Team", sorted(teams), key=f"bat_{rk}")

with col2:
    bowling_team = st.selectbox("Select Bowling Team", sorted(teams), key=f"bowl_{rk}")

city = st.selectbox("Select City", sorted(cities), key=f"city_{rk}")

col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input("Current Score", min_value=0, step=1, key=f"score_{rk}")

with col4:
    overs = st.number_input("Overs Bowled (e.g., 5.3)", min_value=5.0, max_value=19.5, step=0.1, key=f"overs_{rk}")

with col5:
    wickets = st.number_input("Wickets Fallen", min_value=0, max_value=9, step=1, key=f"wickets_{rk}")

last_5_over = st.number_input("Runs scored in last 5 overs", min_value=0, step=1, key=f"last_5_{rk}")


# ---------------- PREDICTION ---------------- #
if st.button("Predict Score"):

    if batting_team == bowling_team:
        st.error("Batting and Bowling team cannot be the same!")
    else:

        overs_completed = int(overs)
        balls_in_current_over = int(round((overs - overs_completed) * 10))
        balls_bowled = (overs_completed * 6) + balls_in_current_over

        balls_left = 120 - balls_bowled
        wickets_left = 10 - wickets

        current_run_rate = 0
        if balls_bowled > 0:
            current_run_rate = (current_score * 6) / balls_bowled

        input_df = pd.DataFrame({
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "city": [city],
            "current_score": [current_score],
            "balls_left": [balls_left],
            "wickets_left": [wickets_left],
            "current_run_rate": [current_run_rate],
            "last_5_over": [last_5_over]
        })

        result = pipe.predict(input_df)
        predicted_score = int(result[0])

        st.success(f"🏆 Predicted Final Score: {predicted_score}")
        
        # --- TIMER AUR ASLI FULL REFRESH ---
        countdown_msg = st.empty()
        
        for i in range(10, 0, -1):
            countdown_msg.info(f"⏳ Page will refresh in {i} seconds ")
            time.sleep(1)
            
        # YAHAN HAI JADOO: Hum reset_count ko badha denge jisse dabbo ke saare IDs badal jayenge!
        st.session_state["reset_count"] += 1
        st.rerun()