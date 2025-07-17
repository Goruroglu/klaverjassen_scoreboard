
import streamlit as st

# Handle reset mode
if 'reset_mode' in st.session_state:
    if st.session_state.reset_mode == "same":
        st.session_state.player1_score = 0
        st.session_state.player2_score = 0
        st.session_state.history = []
        st.session_state.round_to_delete = None
        st.session_state.reset_mode = None
        st.session_state.show_reset_options = False
    elif st.session_state.reset_mode == "new":
        st.session_state.clear()

# Initialize session state variables
for key, default in {
    'player1_score': 0,
    'player2_score': 0,
    'history': [],
    'player1_name': "",
    'player2_name': "",
    'names_set': False,
    'round_to_delete': None,
    'reset_mode': None,
    'show_reset_options': False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# App title and layout
st.set_page_config(page_title="Klaverjassen Scoreboard", layout="centered")
st.title("🃏 Klaverjassen Scoreboard")

# Player names input form
if not st.session_state.names_set:
    st.subheader("Enter Player Names")
    with st.form("name_form"):
        p1_name = st.text_input("Player 1 Name")
        p2_name = st.text_input("Player 2 Name")
        start_game = st.form_submit_button("Start Game")
        if start_game:
            if p1_name.strip() and p2_name.strip():
                st.session_state.player1_name = p1_name.strip()
                st.session_state.player2_name = p2_name.strip()
                st.session_state.names_set = True
            else:
                st.warning("Please enter both player names.")
    st.stop()

player1 = st.session_state.player1_name
player2 = st.session_state.player2_name

st.markdown(f"Reach **1000 points** to win the game. Good luck, {player1} and {player2}!")

# Score input form
st.markdown("### Enter Round Score")
with st.form("score_form"):
    scorer = st.radio("Who is entering the score?", [player1, player2], horizontal=True)

    if scorer == player1:
        p1_score = st.number_input(f"{player1}'s Score", min_value=0, max_value=162, step=1, key="input_p1")
        p2_score = 162 - p1_score
        st.markdown(f"**{player2}'s Score:** {p2_score}")
    else:
        p2_score = st.number_input(f"{player2}'s Score", min_value=0, max_value=162, step=1, key="input_p2")
        p1_score = 162 - p2_score
        st.markdown(f"**{player1}'s Score:** {p1_score}")

    submitted = st.form_submit_button("Add Round Scores")

    if submitted:
        if p1_score + p2_score != 162:
            st.warning("Invalid round. The total score must be exactly 162.")
        else:
            st.session_state.player1_score += p1_score
            st.session_state.player2_score += p2_score
            st.session_state.history.append((p1_score, p2_score))

# Show current scores
st.subheader("Current Scores")
score_cols = st.columns(2)
score_cols[0].metric(player1, st.session_state.player1_score)
score_cols[1].metric(player2, st.session_state.player2_score)

# Show winner if any
if st.session_state.player1_score >= 1000 or st.session_state.player2_score >= 1000:
    winner = player1 if st.session_state.player1_score >= 1000 else player2
    st.success(f"🎉 {winner} has won the game!")

# Round history with delete buttons (expanded by default)
with st.expander("📜 Round History", expanded=True):
    if not st.session_state.history:
        st.info("No rounds added yet.")
    for i, (p1, p2) in enumerate(st.session_state.history):
        col1, col2, col3 = st.columns([3, 3, 1])
        col1.write(f"Round {i + 1}: {player1} - {p1}")
        col2.write(f"{player2} - {p2}")
        if col3.button("❌", key=f"delete_{i}"):
            st.session_state.round_to_delete = i

# Handle round deletion
if st.session_state.round_to_delete is not None:
    i = st.session_state.round_to_delete
    if 0 <= i < len(st.session_state.history):
        p1, p2 = st.session_state.history.pop(i)
        st.session_state.player1_score -= p1
        st.session_state.player2_score -= p2
    st.session_state.round_to_delete = None

# Reset game button
st.markdown("---")
if st.button("🔄 Reset Whole Game"):
    st.session_state.show_reset_options = True

if st.session_state.show_reset_options:
    st.info("Do you want to reset the game with the same players or enter new players?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Same Players"):
            st.session_state.reset_mode = "same"
    with col2:
        if st.button("👥 New Players"):
            st.session_state.reset_mode = "new"

# Footer
st.markdown("Made with ❤️ using Streamlit")
