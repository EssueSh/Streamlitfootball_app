import streamlit as st
import json

st.title("⚽ Player Stat Comparison")

# Load data from the local JSON file
with open("laliga_player_data.json", "r") as f:
    data = json.load(f)

player_names = list(data.keys())

# Player selection
player1 = st.selectbox("Select First Player", player_names)
player2 = st.selectbox("Select Second Player", player_names, index=1 if len(player_names) > 1 else 0)

# Extract player data for the selected players
data1 = data.get(player1, [])[0]  # Get the stats of the first player
data2 = data.get(player2, [])[0]  # Get the stats of the second player

# Display stats side by side for comparison
stat_keys = ["Goals", "Assists", "Minutes", "Yellow", "Red", "xG", "Pass Completion %"]  # Example stats

col1, col2, col3 = st.columns([2, 1, 2])  # Create three columns

with col1:
    for key in stat_keys:
        value1 = str(data1.get(key, 0))  # Safe .get() usage for stats
        st.metric(label=f"{key} ({player1})", value=value1)

with col2:
    st.markdown("### VS")

with col3:
    for key in stat_keys:
        value2 = str(data2.get(key, 0))  # Safe .get() usage for stats
        st.metric(label=f"{key} ({player2})", value=value2)
