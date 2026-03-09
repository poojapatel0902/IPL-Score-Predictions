import streamlit as st
import pickle
import pandas as pd
import base64
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="IPL Score Predictor", layout="wide")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    with open("ipl logo.png", "rb") as logo_file:
        logo_encoded = base64.b64encode(logo_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        /* 1. BACKGROUND IMAGE AUR WHITE SPACE FIX */
        .stApp::before {{
            content: "";
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-attachment: fixed;
            background-position: center top;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            filter: blur(4px); 
            z-index: -1;
        }}
        .stApp {{ background: transparent; }}

        :root {{
            --title-size: 80px;
            --logo-size: 100px;
        }}
        
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        
        header[data-testid="stHeader"] * {{
            color: #FFFFFF !important; 
        }}
        
        /* 2. HEADING (TITLE) - Laptop Size */
        h1.page-title {{
            font-size: var(--title-size) !important;
            color:#FFD166!important; 
            text-align: center;
            text-shadow: 0px 4px 10px rgba(0,0,0,0.8);
            font-weight: 900 !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        .logo-img {{
            height: var(--logo-size) !important;
            width: auto !important;
        }}

        /* 3. NORMAL TEXT */
        p, label {{
            color: #FAFAFA!important; 
            font-size: 25px !important;
            font-weight: bold;
            text-shadow: 0px 2px 6px rgba(0,0,0,0.6);
        }}

        /* 4. INPUT BOXES */
        div[data-baseweb="select"] > div, 
        div[data-testid="stNumberInputContainer"] {{
            background-color: rgba(255, 255, 255, 0.4) !important;
            border-radius: 8px !important;
            min-height: 45px ;
            color: black; 
        }}

        input {{
            color: black !important; 
            font-size: 20px !important; 
        }}

        /* BUTTONS HIDE IN NUMBER INPUT */
        div[data-testid="stNumberInputContainer"] button {{
            display: none !important; 
        }}

        /* 7. PREDICT BUTTON */
        div.stButton > button {{
            background: linear-gradient(90deg,#ff9800,#ff5722)!important; 
            width: 100%;
            height: 55px;
            margin-top: 25px;
            border-radius: 8px !important;
        }}

        div.stButton > button p {{
            color: #FFFFFF !important;  
            font-size: 25px !important;
            font-weight: bold !important;
        }}
        
        .block-container {{
            max-width: 1050px !important; 
            padding-top: 2rem !important; 
        }}

        /* =========================================
           10. 📱 MOBILE RESPONSIVE FIX
           ========================================= */
        @media screen and (max-width: 768px) {{
            h1.page-title {{
                font-size: 45px !important; /* Mobile ma title motu thase pan screen ni bahar nahi jay */
                line-height: 1.1 !important;
                display: block !important;
            }}
            .logo-img {{
                height: 70px !important;
            }}
            p, label {{
                font-size: 20px !important;
            }}
        }}

        @media screen and (max-width: 480px) {{
            h1.page-title {{
                font-size: 38px !important; /* Small mobile mate size */
                font-weight: bold !important;
            }}
            .logo-img {{
                height: 60px !important;
            }}
        }}
        </style>

        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%;">
            <img src="data:image/png;base64,{logo_encoded}" class="logo-img">
            <h1 class="page-title">IPL Score Predictor</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

# Uske baad function ko call karna hai bina space ke


# ---------------- LOAD BACKGROUND ---------------- #
add_bg_from_local("image3.png")
# ---------------- LOAD MODEL ---------------- #
pipe = pickle.load(open("pipe.pkl", "rb"))

# ---------------- DATA ---------------- #
teams = [
    'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans',
    'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians',
    'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bengaluru',
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
#st.title("🏏 IPL Score Predictor")

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
    wickets = st.number_input("Wickets Fallen", min_value=0, max_value=10, step=1, key=f"wickets_{rk}")

#last_5_over = st.number_input("Runs scored in last 5 overs", min_value=0, step=1, key=f"last_5_{rk}")


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
           # "last_5_over": [last_5_over]
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
