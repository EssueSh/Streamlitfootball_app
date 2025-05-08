import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="La Liga Player Stats", layout="centered")

@st.cache_data
def load_data():
    return pd.read_excel("players.xlsx")  # Make sure this file is uploaded on Streamlit Cloud

df = load_data()

st.title("⚽ La Liga 2021–2022 Player Stats Viewer")

# Clean column names (remove spaces, handle duplicates)
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Let user select one or more players
players = df['Player'].unique()
selected_players = st.multiselect("Select Players", players, default=players[:2])

# Filter data
filtered_df = df[df["Player"].isin(selected_players)]

if not filtered_df.empty:
    st.subheader("📊 Basic Stats Comparison")
    stats_to_plot = ['Min', 'Gls', 'Ast', 'xG_y', 'npxG', 'xAG', 'SCA', 'GCA']
    df_plot = filtered_df[['Player'] + stats_to_plot].set_index('Player')
    st.bar_chart(df_plot)

    st.subheader("🧾 Player Summary Table")
    st.dataframe(filtered_df[['Player', 'Team', 'Pos', 'Age', 'Min', 'Gls', 'Ast', 'xG_y', 'npxG', 'xAG', 'SCA', 'GCA']])
else:
    st.info("Please select at least one player to view stats.")

st.caption("Made with ❤️ using Streamlit")
