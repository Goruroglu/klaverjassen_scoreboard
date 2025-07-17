import streamlit as st

# Reset handling
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

# Initialize session state
default_state = {
    'player1_score': 0,
    'player2_score': 0,
    'history': [],
    'player1_name': '',
    'player2_name': '',
    'names_set': False,
    'round_to_delete': None,
    'reset_mode': None,
    'show_reset_options': False,
    'set_point': 1000,
    'score_entry_player': 'player1',
}
for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Page configuration
st.set_page_config(page_title="Klaverjassen Scoreboard", layout="centered")
st.title("🎯 Klaverjassen Scoreboard")

# Player & target setup
if not st.session_state.names_set:
    st.subheader("🎮 Start New Game")
    with st.form("setup_form"):
        col1, col2 = st.columns(2)
        p1_name = col1.text_input("Player 1 Name")
        p2_name = col2.text_input("Player 2 Name")

        target = st.number_input("Set Point to Win", value=1000, min_value=100, step=100)

        entry_choice = st.radio("Who will enter their score manually?", [p1_name or "Player 1", p2_name or "Player 2"])

        start = st.form_submit_button("Start Game")
        if start:
            if p1_name.strip() and p2_name.strip():
                st.session_state.player1_name = p1_name.strip()
                st.session_state.player2_name = p2_name.strip()
                st.session_state.set_point = target
                st.session_state.score_entry_player = 'player1' if entry_choice == p1_name else 'player2'
                st.session_state.names_set = True
            else:
                st.warning("⚠️ Please enter both player names.")
    st.stop()

player1 = st.session_state.player1_name
player2 = st.session_state.player2_name
target_score = st.session_state.set_point
entry_side = st.session_state.score_entry_player

# Header info
st.markdown(f"🏆 First to reach *{target_score} points* wins!")

# Score input
with st.form("score_form"):
    st.subheader("➕ Add Round Score")

    if entry_side == 'player1':
        score = st.number_input(f"{player1}'s Score", min_value=0, max_value=162, step=1, key="entry1")
        auto_score = 162 - score
        st.number_input(f"{player2}'s Score", value=auto_score, disabled=True, key="auto2")
    else:
        score = st.number_input(f"{player2}'s Score", min_value=0, max_value=162, step=1, key="entry2")
        auto_score = 162 - score
        st.number_input(f"{player1}'s Score", value=auto_score, disabled=True, key="auto1")

    submitted = st.form_submit_button("✅ Submit Round")
    if submitted:
        if entry_side == 'player1':
            st.session_state.player1_score += score
            st.session_state.player2_score += auto_score
            st.session_state.history.append((score, auto_score))
        else:
            st.session_state.player1_score += auto_score
            st.session_state.player2_score += score
            st.session_state.history.append((auto_score, score))

# Current scores
st.subheader("📊 Current Scores")
score_col1, score_col2 = st.columns(2)
score_col1.metric(player1, st.session_state.player1_score)
score_col2.metric(player2, st.session_state.player2_score)

# Winner announcement
if st.session_state.player1_score >= target_score or st.session_state.player2_score >= target_score:
    winner = player1 if st.session_state.player1_score >= target_score else player2
    st.success(f"🎉 *{winner}* has reached {target_score} points and wins the game!")

# History with delete option
with st.expander("🕓 Round History"):
    for i, (p1, p2) in enumerate(st.session_state.history):
        col1, col2, col3 = st.columns([3, 3, 1])
        col1.write(f"Round {i + 1}: {player1} - {p1}")
        col2.write(f"{player2} - {p2}")
        if col3.button("❌", key=f"delete_{i}"):
            st.session_state.round_to_delete = i

# Handle deletion
if st.session_state.round_to_delete is not None:
    idx = st.session_state.round_to_delete
    if 0 <= idx < len(st.session_state.history):
        p1, p2 = st.session_state.history.pop(idx)
        st.session_state.player1_score -= p1
        st.session_state.player2_score -= p2
    st.session_state.round_to_delete = None

# Reset game options
st.markdown("---")
if st.button("🔄 Reset Game"):
    st.session_state.show_reset_options = True

if st.session_state.show_reset_options:
    st.info("Reset game with same or new players?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Same Players"):
            st.session_state.reset_mode = "same"
    with col2:
        if st.button("👥 New Players"):
            st.session_state.reset_mode = "new"

# Footer
st.markdown("— Made with ❤️ using Streamlit")
