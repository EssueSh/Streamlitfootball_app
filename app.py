import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel("valencia_players.xlsx")

# 1. Title and Description
st.title("La Liga 2021-2022 Player Stats - Valencia FC")
st.write("""
    This app allows you to explore the performance of Valencia FC players in the La Liga 2021-2022 season. 
    You can view the top-performing players, compare players, and visualize their performance through different metrics.
""")

# 2. Player Selection Dropdown
player = st.selectbox("Select Player to View Details", df['Player'].unique())

# Player-wise Summary
player_data = df[df['Player'] == player]
st.write(f"### {player}'s Performance Summary:")
st.write(player_data[['Player', 'Min', 'Gls', 'Ast', 'xG_y', 'xAG', 'Cmp%_x', 'PrgP', 'PrgC']])

# 3. Comparison of Multiple Players
st.write("### Compare Players:")
selected_players = st.multiselect("Select Players to Compare", df['Player'].unique())

# Filter the selected players and display their stats
if selected_players:
    comparison_data = df[df['Player'].isin(selected_players)]
    st.write(f"### Comparison Between Selected Players:")
    st.write(comparison_data[['Player', 'Min', 'Gls', 'Ast', 'xG_y', 'xAG', 'Cmp%_x', 'PrgP', 'PrgC']])

# 4. Best Player Stats Summary (Show Top Performers)
best_scorer = df.loc[df['Gls'].idxmax()]
best_assist = df.loc[df['Ast'].idxmax()]
best_xG = df.loc[df['xG_y'].idxmax()]

st.write("### Best Performing Players Stats:")
st.write(f"Top Scorer: {best_scorer['Player']} with {best_scorer['Gls']} goals")
st.write(f"Top Assister: {best_assist['Player']} with {best_assist['Ast']} assists")
st.write(f"Highest xG: {best_xG['Player']} with {best_xG['xG_y']} xG")

# 5. Ranking Players Based on Stats (Weight Goals, Assists, and xG)
df['Goal_Score'] = df['Gls'] / df['Gls'].max()
df['Assist_Score'] = df['Ast'] / df['Ast'].max()
df['xG_Score'] = df['xG_y'] / df['xG_y'].max()

weights = {'Goal_Score': 0.4, 'Assist_Score': 0.3, 'xG_Score': 0.3}
df['Player_Score'] = (df['Goal_Score'] * weights['Goal_Score'] + 
                       df['Assist_Score'] * weights['Assist_Score'] + 
                       df['xG_Score'] * weights['xG_Score'])

# Sort players by the total score
top_players = df.sort_values('Player_Score', ascending=False)
st.write("### Player Ranking Based on Stats:")
st.write(top_players[['Player', 'Goal_Score', 'Assist_Score', 'xG_Score', 'Player_Score']])

# 6. Prediction of Goals Based on xG (Optional ML)
X = df[['xG_y']]
y = df['Gls']
model = LinearRegression()
model.fit(X, y)
df['Predicted_Gls'] = model.predict(X)

# Plot Actual vs Predicted Goals
st.write("### Predicted Goals vs Actual Goals")
fig, ax = plt.subplots()
ax.scatter(df['xG_y'], df['Gls'], color='blue', label='Actual')
ax.plot(df['xG_y'], df['Predicted_Gls'], color='red', label='Predicted', linestyle='--')
ax.set_xlabel('xG')
ax.set_ylabel('Goals')
ax.legend()
st.pyplot(fig)
