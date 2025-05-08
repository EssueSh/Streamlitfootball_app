import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("La-Liga Merged.csv")
    return df[df['Squad'] == 'Valencia']  # Only Valencia FC

df = load_data()

st.title("Valencia FC - Player Stats (2021-22)")

# Player selection
player = st.selectbox("Select Player", df['Player'].unique())
st.write(df[df['Player'] == player][['Min', 'Gls', 'Ast', 'xG_y']])

# Compare players (simple stats only)
players = st.multiselect("Compare Players", df['Player'].unique())
if players:
    st.dataframe(df[df['Player'].isin(players)][['Player', 'Gls', 'Ast', 'xG_y']])

# Top performers (precomputed)
st.subheader("Top Performers")
st.write("Top Scorer:", df.loc[df['Gls'].idxmax(), 'Player'])
st.write("Top Assister:", df.loc[df['Ast'].idxmax(), 'Player'])
