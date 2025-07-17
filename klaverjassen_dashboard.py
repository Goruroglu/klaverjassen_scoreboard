import streamlit as st

# Initialize session state
if 'player1_score' not in st.session_state:
    st.session_state.player1_score = 0
if 'player2_score' not in st.session_state:
    st.session_state.player2_score = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'player1_name' not in st.session_state:
    st.session_state.player1_name = ""
if 'player2_name' not in st.session_state:
    st.session_state.player2_name = ""
if 'names_set' not in st.session_state:
    st.session_state.names_set = False

def reset_game():
    st.session_state.player1_score = 0
    st.session_state.player2_score = 0
    st.session_state.history = []
    st.session_state.names_set = False

# App title and layout
st.set_page_config(page_title="Klaverjassen Scoreboard", layout="centered")
st.title("🃏 Klaverjassen Scoreboard")

# Set player names
if not st.session_state.names_set:
    st.subheader("Enter Player Names")
    with st.form("name_form"):
        p1_name = st.text_input("Player 1 Name", key="p1_name")
        p2_name = st.text_input("Player 2 Name", key="p2_name")
        start_game = st.form_submit_button("Start Game")
        if start_game and p1_name.strip() and p2_name.strip():
            st.session_state.player1_name = p1_name.strip()
            st.session_state.player2_name = p2_name.strip()
            st.session_state.names_set = True
        elif start_game:
            st.warning("Please enter both player names.")
    st.stop()

player1 = st.session_state.player1_name
player2 = st.session_state.player2_name

st.markdown(f"Reach **1000 points** to win the game. Enjoy, {player1} and {player2}!")

# Score input form
with st.form("score_form"):
    col1, col2 = st.columns(2)
    with col1:
        p1 = st.number_input(f"{player1} Round Score", min_value=0, max_value=162, step=1, key="p1_input")
    with col2:
        p2 = 162 - p1
        st.number_input(f"{player2} Round Score", value=p2, disabled=True, key="p2_display")

    submitted = st.form_submit_button("Add Round Scores")

    if submitted:
        if p1 > 162:
            st.error("The total round score cannot exceed 162 points.")
        else:
            st.session_state.player1_score += p1
            st.session_state.player2_score += 162 - p1
            st.session_state.history.append((p1, 162 - p1))

# Display current scores
st.subheader("Current Scores")
score_cols = st.columns(2)
score_cols[0].metric(player1, st.session_state.player1_score)
score_cols[1].metric(player2, st.session_state.player2_score)

# Display winner
if st.session_state.player1_score >= 1000 or st.session_state.player2_score >= 1000:
    winner = player1 if st.session_state.player1_score >= 1000 else player2
    st.success(f"🎉 {winner} has won the game!")

# Score history
with st.expander("📜 Round History"):
    for i, (p1, p2) in enumerate(st.session_state.history, 1):
        st.write(f"Round {i}: {player1} - {p1} | {player2} - {p2}")

# Reset button
st.button("🔄 Reset Game", on_click=reset_game)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
