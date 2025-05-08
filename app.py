import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("La-Liga Merged.csv")

st.title("Valencia FC - La Liga 2021-22 Player Stats")

st.markdown("Explore Valencia FC players' performance in La Liga 2021-22 season.")

# Player details
player = st.selectbox("Choose a Player", df['Player'].unique())
st.subheader(f"{player} - Performance Summary")
st.dataframe(df[df['Player'] == player][['Min', 'Gls', 'Ast', 'xG_y', 'xAG', 'Cmp%_x', 'PrgP', 'PrgC']])

# Compare players
selected = st.multiselect("Compare Players", df['Player'].unique())
if selected:
    st.subheader("Comparison Table")
    st.dataframe(df[df['Player'].isin(selected)][['Player', 'Gls', 'Ast', 'xG_y']])

# Best performers
st.subheader("Top Performers")
st.write(f"**Top Scorer:** {df.loc[df['Gls'].idxmax(), 'Player']} ({df['Gls'].max()} goals)")
st.write(f"**Top Assister:** {df.loc[df['Ast'].idxmax(), 'Player']} ({df['Ast'].max()} assists)")
st.write(f"**Highest xG:** {df.loc[df['xG_y'].idxmax(), 'Player']} ({df['xG_y'].max()} xG)")

# Player ranking
df['Score'] = (
    0.4 * df['Gls'] / df['Gls'].max() +
    0.3 * df['Ast'] / df['Ast'].max() +
    0.3 * df['xG_y'] / df['xG_y'].max()
)
st.subheader("Top Ranked Players")
st.dataframe(df[['Player', 'Score']].sort_values('Score', ascending=False).head(10))

# Prediction
st.subheader("Goals Prediction Based on xG")
model = LinearRegression()
model.fit(df[['xG_y']], df['Gls'])
df['Predicted_Gls'] = model.predict(df[['xG_y']])

fig, ax = plt.subplots()
ax.scatter(df['xG_y'], df['Gls'], color='blue', label='Actual')
ax.plot(df['xG_y'], df['Predicted_Gls'], color='red', linestyle='--', label='Predicted')
ax.set_xlabel("xG")
ax.set_ylabel("Goals")
ax.legend()
st.pyplot(fig)
