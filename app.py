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
        
        /* UPAR KA SAFED PATTA (WHITE SPACE) GAYAB KARNE KE LIYE */
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        
        /* UPAR KA MENU (Deploy, 3-dots) VISIBLE KARNA */
        header[data-testid="stHeader"] * {{
            color: #FFFFFF !important; 
        }}
        
        /* 2. HEADING (TITLE) - Default Laptop Size */
        h1 {{
            font-size: 65px !important; 
            color:#FFD166!important; 
            text-align: center;
            text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
        }}

        /* 3. BAAKI NORMAL TEXT (Labels) - Default Laptop Size */
        p, label {{
            color: #FAFAFA!important; 
            font-size: 25px !important;
            font-weight: bold;
            text-shadow: 0px 2px 6px rgba(0,0,0,0.6);;
        }}

        /* 4. SAARE DABBE (Outer Box) KI TRANSPARENCY - UPDATE KIYA GAYA */
        div[data-baseweb="select"] > div, 
        div[data-testid="stNumberInputContainer"],
        ul[role="listbox"] {{
            background-color: rgba(255, 255, 255, 0.4) !important; 
            border:none !important;
            border-radius: 8px !important;
            min-height: 45px ;
            font-size: 20px;
            color: black !important; 
        }}

        /* 5. ANDAR KE CHHUPE HUE SAFED RANG KO GAYAB KARNA AUR TEXT WHITE KARNA */
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

        li[role="option"]:hover {{
            background-color: rgba(0, 0, 0, 0.4) !important; 
            color: black !important;
        }}

        /* 7. PREDICT BUTTON */
        div.stButton > button {{
            background: linear-gradient(90deg,#ff9800,#ff5722)!important; 
            border: 2px  #FFD700 !important; 
            width: 100%;
            height: 55px;
            margin-top: 25px;
            padding: 20px !important;
            border-radius: 8px !important; 
        }}

        div.stButton > button p {{
            color: #FFFFFF !important;  
            font-size: 25px !important;
            font-weight: bold !important;
            background: transparent !important; 
            margin: 0px !important;
        }}
        
        /* 8. PAGE KO "MEDIUM" WIDTH DENA */
        .block-container {{
            max-width: 1050px !important; 
            padding-top: 10rem !important; 
            padding-bottom: 2rem !important;
        }}
        
        /* 9. ERROR AUR SUCCESS MESSAGE KA CSS */
        div[data-testid="stAlert"] {{
            background-color: rgba(225,225,225, 0.5) !important; 
            border-radius: 8px !important;
        }}

        div[data-testid="stAlert"] p {{
            color: black !important; 
            font-size: 22px !important;
            text-shadow: none !important;
        }}

        /* =========================================
           10. 📱 MOBILE AUR TABLET RESPONSIVE CSS
           ========================================= */
        @media screen and (max-width: 768px) {{
            /* 768px (Tablets aur bade phones) ke liye */
            h1 {{
                font-size: 65px !important; 
                line-height: 1.1 !important;
            }}
            .block-container {{         
                padding-top: 6rem !important; 
                padding-bottom: 2rem !important;
            }}
            p, label {{
                font-size: 18px !important;
            }}
            div[data-baseweb="select"] > div, 
            div[data-testid="stNumberInputContainer"], input, span {{
                font-size: 16px !important;
                min-height: 40px !important;
            }}
            div.stButton > button {{
                height: 45px !important;
                margin-top: 15px !important;
            }}
            div.stButton > button p {{
                font-size: 20px !important;
            }}
        }}

        @media screen and (max-width: 480px) {{
            /* 480px (Chhote phones) ke liye special size */
            h1 {{
                font-size: 50px !important; 
            }}
        }}
        </style>

        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 10px; padding-bottom: 15px;">
            <h1 style="margin: 0; padding: 0;">IPL Score Predictor</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

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
if "reset_count" not in st.session_state:
    st.session_state["reset_count"] = 0

rk = st.session_state["reset_count"]

# ---------------- UI ---------------- #

col1, col2 = st.columns(2)

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
        })

        result = pipe.predict(input_df)
        predicted_score = int(result[0])

        st.success(f"🏆 Predicted Final Score: {predicted_score}")
        
        # --- TIMER AUR ASLI FULL REFRESH ---
        countdown_msg = st.empty()
        
        for i in range(10, 0, -1):
            countdown_msg.info(f"⏳ Page will refresh in {i} seconds ")
            time.sleep(1)
            
        st.session_state["reset_count"] += 1
        st.rerun()