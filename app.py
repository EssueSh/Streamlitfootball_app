import streamlit as st
import json

st.title("⚽ Player Stat Comparison")

# Load data from single JSON file
with open("laliga_player_data.json", "r") as f:
    data = json.load(f)

player_names = list(data.keys())

# Player selection
player1 = st.selectbox("Select First Player", player_names)
player2 = st.selectbox("Select Second Player", player_names, index=1 if len(player_names) > 1 else 0)

data1 = data[player1]
data2 = data[player2]

# Display comparison
st.header("📊 Stat Comparison")
stat_keys = ["goals", "assists", "xG", "xAG", "pass_pct", "shots"]

for key in stat_keys:
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        # Ensure the value is a number and convert it to a string for display
        value1 = str(data1.get(key, 0))
        st.metric(label=f"{key} ({player1})", value=value1)
    with col2:
        st.markdown("### VS")
    with col3:
        # Ensure the value is a number and convert it to a string for display
        value2 = str(data2.get(key, 0))
        st.metric(label=f"{key} ({player2})", value=value2)

# Optional raw view
with st.expander("🔍 View Full Data"):
    st.subheader(player1)
    st.json(data1)
    st.subheader(player2)
    st.json(data2)
