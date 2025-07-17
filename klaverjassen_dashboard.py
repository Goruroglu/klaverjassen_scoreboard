import streamlit as st

# Initialize session state
if 'player1_score' not in st.session_state:
    st.session_state.player1_score = 0
if 'player2_score' not in st.session_state:
    st.session_state.player2_score = 0
if 'history' not in st.session_state:
    st.session_state.history = []

def reset_game():
    st.session_state.player1_score = 0
    st.session_state.player2_score = 0
    st.session_state.history = []

# App title and layout
st.set_page_config(page_title="Klaverjassen Scoreboard", layout="centered")
st.title("🃏 Klaverjassen Scoreboard")

st.markdown("Reach **1000 points** to win the game. Enjoy!")

# Score input form
with st.form("score_form"):
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.number_input("Player 1 Round Score", min_value=0, max_value=1000, step=1, key="p1_input")
    with col2:
        p2 = st.number_input("Player 2 Round Score", min_value=0, max_value=1000, step=1, key="p2_input")
    submitted = st.form_submit_button("Add Round Scores")

    if submitted:
        st.session_state.player1_score += p1
        st.session_state.player2_score += p2
        st.session_state.history.append((p1, p2))

# Display current scores
st.subheader("Current Scores")
score_cols = st.columns(2)
score_cols[0].metric("Player 1", st.session_state.player1_score)
score_cols[1].metric("Player 2", st.session_state.player2_score)

# Display winner
if st.session_state.player1_score >= 1000 or st.session_state.player2_score >= 1000:
    winner = "Player 1" if st.session_state.player1_score >= 1000 else "Player 2"
    st.success(f"🎉 {winner} has won the game!")

# Score history
with st.expander("📜 Round History"):
    for i, (p1, p2) in enumerate(st.session_state.history, 1):
        st.write(f"Round {i}: Player 1 - {p1} | Player 2 - {p2}")

# Reset button
st.button("🔄 Reset Game", on_click=reset_game)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
