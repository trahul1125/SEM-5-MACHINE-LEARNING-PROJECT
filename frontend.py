import streamlit as st
import pickle
import pandas as pd


import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# add_bg_from_local("bg1.jpg")
add_bg_from_local("bg2.png")


teams = [
    "Sunrisers Hyderabad",
    "Mumbai Indians",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Kings XI Punjab",
    "Chennai Super Kings",
    "Rajasthan Royals",
    "Delhi Capitals",
]

cities = [
    "Hyderabad",
    "Bangalore",
    "Mumbai",
    "Indore",
    "Kolkata",
    "Delhi",
    "Chandigarh",
    "Jaipur",
    "Chennai",
    "Cape Town",
    "Port Elizabeth",
    "Durban",
    "Centurion",
    "East London",
    "Johannesburg",
    "Kimberley",
    "Bloemfontein",
    "Ahmedabad",
    "Cuttack",
    "Nagpur",
    "Dharamsala",
    "Visakhapatnam",
    "Pune",
    "Raipur",
    "Ranchi",
    "Abu Dhabi",
    "Sharjah",
    "Mohali",
    "Bengaluru",
]

pipe = pickle.load(open("pipe.pkl", "rb"))


# st.title("IPL cricket match outcome predictor")
st.markdown(
    f'<h1 style="color:#33ff33;font-size:24px;">{"IPL cricket match outcome predictor"}</h1>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select batting team", sorted(teams))
with col2:
    bowling_team = st.selectbox("Select fielding team", sorted(teams))

selected_city = st.selectbox("Match venue", sorted(cities))

target = st.number_input("Target")

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input("Current Score")
with col4:
    overs = st.number_input("Overs Bowled")
with col5:
    wickets = st.number_input("Wickets taken")

if st.button("Predict"):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame(
        {
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "city": [selected_city],
            "runs_left": [runs_left],
            "balls_left": [balls_left],
            "wickets": [wickets],
            "total_runs_x": [target],
            "crr": [crr],
            "rrr": [rrr],
        }
    )

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win * 100)) + "%")
    st.header(bowling_team + "- " + str(round(loss * 100)) + "%")
