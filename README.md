## IPL Score Predictor

# Project Overview
The IPL Score Predictor is a machine learning-based web application designed to forecast the final first-innings score of an Indian Premier League (IPL) match in real-time. By leveraging historical match data and current match dynamics, this tool empowers cricket fans, analysts, and enthusiasts with data-driven score projections.

# Dataset


# Project Process
1. Data Engineering & Preprocessing
Extracted and cleaned historical IPL ball-by-ball data.
Engineered crucial real-time features including balls_left, wickets_left, and current_run_rate (CRR) to accurately capture the match situation at any given over.
2. Machine Learning Modeling
Developed a robust prediction pipeline using Python and scikit-learn.
Trained an XGBoost Regressor model to understand complex, non-linear patterns in T20 cricket (e.g., the sudden acceleration in run-scoring during the "death overs").
Serialized the trained model pipeline for rapid inference in a production environment.
3. UI/UX & Web Development
Built a highly interactive and responsive frontend using Streamlit.
Designed a custom, modern "Dark Glassmorphism" user interface using advanced CSS, ensuring the application looks sleek and performs flawlessly on both desktop and mobile devices.
4. Cloud Deployment
Successfully deployed the fully functional web application to the cloud.

# Live Application:
iplscorecast.streamlit.app

# Project Insights
The Wicket Multiplier: The model strongly indicates that wickets in hand during the final 5 overs have an exponentially higher impact on the projected final score than the current run rate alone.
Venue Dynamics: The city feature acts as a significant weight in the algorithm. High-altitude or historically high-scoring grounds (like Bengaluru) aggressively bump up the predicted score compared to slower, spin-friendly pitches (like Lucknow or Chennai).
Early Overs Volatility: Predictions made within the first 6 overs (Powerplay) rely heavily on the batting team's historical strength, while predictions in the middle overs shift heavily toward the current_run_rate and wickets_left

# Conclusion
This project successfully bridges raw historical sports data with an accessible, real-time web application. By combining a highly accurate XGBoost prediction model with a premium, responsive frontend, the IPL Score Predictor transforms complex predictive analytics into an intuitive user experience. It stands as a complete end-to-end data science and web development lifecycle—from raw data processing to a live, cloud-hosted application.
