import streamlit as st
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Define the stats to compare
stat_keys = ["Goals", "Assists", "Minutes", "Yellow", "Red", "xG", "Pass Completion %"]

# Display stats side by side for comparison
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

# Create Bar Graph to Compare Player Stats
def plot_bar_graph():
    # Extract the values for the selected stats
    stats_player1 = [data1.get(key, 0) for key in stat_keys]
    stats_player2 = [data2.get(key, 0) for key in stat_keys]

    # Create a dataframe for seaborn
    stats_df = {
        "Stat": stat_keys,
        f"{player1} Stats": stats_player1,
        f"{player2} Stats": stats_player2
    }
    
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(stat_keys))  # The label locations
    width = 0.35  # The width of the bars

    ax.bar(x - width/2, stats_player1, width, label=player1)
    ax.bar(x + width/2, stats_player2, width, label=player2)

    ax.set_xlabel('Stats')
    ax.set_ylabel('Values')
    ax.set_title(f'Comparison of {player1} and {player2} Stats')
    ax.set_xticks(x)
    ax.set_xticklabels(stat_keys, rotation=45, ha="right")
    ax.legend()

    st.pyplot(fig)

# Display the bar graph
plot_bar_graph()

# Create Radar Chart for Player Comparison
def plot_radar_chart():
    # Prepare the data for radar chart
    stats_player1 = [data1.get(key, 0) for key in stat_keys]
    stats_player2 = [data2.get(key, 0) for key in stat_keys]

    # Number of stats
    num_vars = len(stat_keys)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The radar chart is a circle, so we need to "close the circle" by appending the first value to the end
    stats_player1 += stats_player1[:1]
    stats_player2 += stats_player2[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Plot the data for player1 and player2
    ax.fill(angles, stats_player1, color='blue', alpha=0.25)
    ax.fill(angles, stats_player2, color='orange', alpha=0.25)

    ax.plot(angles, stats_player1, color='blue', linewidth=2, linestyle='solid', label=player1)
    ax.plot(angles, stats_player2, color='orange', linewidth=2, linestyle='solid', label=player2)

    ax.set_yticklabels([])  # Hide radial labels
    ax.set_xticks(angles[:-1])  # Set the labels on the axes
    ax.set_xticklabels(stat_keys, fontsize=10)

    ax.set_title(f'Radar Chart Comparison: {player1} vs {player2}', size=15)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    st.pyplot(fig)

# Display the radar chart
plot_radar_chart()
