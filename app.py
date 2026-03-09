import streamlit as st
import pickle
import pandas as pd
import base64
import time
import streamlit.components.v1 as components


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
        /* UPAR KA SAFED PATTA (WHITE SPACE) GAYAB KARNE KE LIYE */
       header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        /* UPAR KA MENU (Deploy, 3-dots) VISIBLE KARNA */
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        header[data-testid="stHeader"] * {{
            color: #FFFFFF !important; /* Deploy aur Always rerun ko safed karne ke liye */
        }}
        /* 2. HEADING (TITLE) */
        h1 {{
            font-size: 65px !important; 
            color:#FFD166!important; 
            text-align: center;
            text-shadow: 0px 2px 8px rgba(0,0,0,0.7);
        }}

        /* 3. BAAKI NORMAL TEXT (Labels) */
        p, label {{
            color: #FAFAFA!important; 
            font-size: 25px !important;
            font-weight: bold;
            text-shadow: 0px 2px 6px rgba(0,0,0,0.6);;
        }}

        /* 4. SAARE DABBE (Outer Box) KI TRANSPARENCY */
        div[data-baseweb="select"] > div, 
        div[data-testid="stNumberInputContainer"],
        ul[role="listbox"] {{
            background-color: rgba(255, 255, 255, 0.4) !important;
            border: none !important;            
            border-radius: 8px !important;
            min-height: 45px ;
            font-size: 20px;
            color: black; 
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
            background: linear-gradient(90deg,#ff9800,#ff5722)!important; /* Button ka color */
            border: 2px  #FFD700 !important; 
           
            width: 100%;
            height: 55px;
            margin-top: 25px;
            padding: 20px !important;
        }}

        /* B. SIRF ANDAR KA TEXT (Font Color aur Size) */
        div.stButton > button p {{
            color: #FFFFFF !important;  /* <--- YAHAN TEXT KA COLOR DALEIN (Jaise Safed ke liye #FFFFFF) */
            font-size: 25px !important;
            font-weight: bold !important;
            background: transparent !important; /* <--- YEH LINE DOUBLE BOX BANNE SE ROKEGI */
            margin: 0px !important;
        }}
/* 8. PAGE KO "MEDIUM" WIDTH DENA */
        .block-container {{
            max-width: 1050px !important; /* <--- YAHAN SE AAP PAGE KI CHAUDHAAI SET KAR SAKTE HAIN */
            padding-top: 10rem !important;
            padding-bottom: 2rem !important;
        }}
        /* 9. ERROR AUR SUCCESS MESSAGE KA CSS */
        /* Message wale dabbe (Box) ka design */
        div[data-testid="stAlert"] {{
            background-color: rgba(225,225,225, 0.5) !important; /* <--- Box ka background (Abhi dark hai) */
            
            border-radius: 8px !important;
        }}

        /* Message ke andar ke TEXT ka design */
        div[data-testid="stAlert"] p {{
            color: black !important; /* <--- TEXT KA COLOR (Yahan se aap pink hata kar Safed/White kar sakte hain) */
            font-size: 22px !important;
            text-shadow: none !important;
            
        }}
        /* 10. IPL LOGO (Top Left) */
    .ipl-logo {{
        position: fixed !important;
        top: 85px !important; 
        left: 900px !important; 
        width: 150px !important; 
        z-index: 9999 !important; 
    }}
    </style>
<img src="data:image/png;base64,{logo_encoded}" class="ipl-logo">
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