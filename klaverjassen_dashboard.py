
import streamlit as st

# Reset logic
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

# Layout
st.set_page_config(page_title="Klaverjassen", layout="centered")
st.markdown("<h1 style='text-align: center;'>🃏 Klaverjassen Scoreboard</h1>", unsafe_allow_html=True)

# Player names
if not st.session_state.names_set:
    with st.form("name_form"):
        p1 = st.text_input("Player 1 Name")
        p2 = st.text_input("Player 2 Name")
        if st.form_submit_button("Start"):
            if p1.strip() and p2.strip():
                st.session_state.player1_name = p1.strip()
                st.session_state.player2_name = p2.strip()
                st.session_state.player1_score = 0
                st.session_state.player2_score = 0
                st.session_state.history = []
                st.session_state.names_set = True
            else:
                st.warning("Enter both names.")
    st.stop()

player1 = st.session_state.player1_name
player2 = st.session_state.player2_name

st.markdown(f"<p style='text-align: center;'>First to <strong>1000 points</strong> wins. Good luck, <strong>{player1}</strong> and <strong>{player2}</strong>!</p>", unsafe_allow_html=True)

# Score input
with st.form("score_form"):
    scorer = st.radio("Select player to enter score:", [player1, player2], horizontal=True)

    col = st.columns([1, 2, 1])[1]  # Centered column
    with col:
        score = st.number_input(
            f"{scorer}'s Score", min_value=0, max_value=162, step=1
        )

    if scorer == player1:
        p1_score = score
        p2_score = 162 - score
    else:
        p2_score = score
        p1_score = 162 - score

    st.markdown(
        f"<div style='text-align:center; font-size:16px;'>"
        f"<strong>{player1}:</strong> {p1_score} &nbsp;&nbsp;&nbsp; "
        f"<strong>{player2}:</strong> {p2_score}</div>",
        unsafe_allow_html=True
    )

    if st.form_submit_button("✅ Add Round"):
        if p1_score + p2_score != 162:
            st.error("Total must be exactly 162.")
        else:
            st.session_state.player1_score += p1_score
            st.session_state.player2_score += p2_score
            st.session_state.history.append((p1_score, p2_score))

# Scores
st.subheader("📊 Current Scores")
cols = st.columns(2)
cols[0].metric(player1, st.session_state.player1_score)
cols[1].metric(player2, st.session_state.player2_score)

# Winner
if st.session_state.player1_score >= 1000 or st.session_state.player2_score >= 1000:
    winner = player1 if st.session_state.player1_score >= 1000 else player2
    st.success(f"🎉 {winner} has won the game!")

# History
st.subheader("📜 Round History")
if not st.session_state.history:
    st.info("No rounds yet.")
else:
    for i, (p1, p2) in enumerate(st.session_state.history):
        col1, col2, col3 = st.columns([3, 3, 1])
        col1.write(f"{player1}: {p1}")
        col2.write(f"{player2}: {p2}")
        if col3.button("❌", key=f"del_{i}"):
            st.session_state.player1_score -= p1
            st.session_state.player2_score -= p2
            st.session_state.history.pop(i)
            st.experimental_rerun()

# Reset options
st.markdown("---")
if st.button("🔄 Reset Game"):
    st.session_state.show_reset_options = True

if st.session_state.show_reset_options:
    st.info("Reset with same players or start fresh?")
    col1, col2 = st.columns(2)
    if col1.button("🔁 Same Players"):
        st.session_state.reset_mode = "same"
    if col2.button("👥 New Players"):
        st.session_state.reset_mode = "new"

# Footer
st.markdown("<hr><p style='text-align: center;'>Made with ❤️ using Streamlit</p>", unsafe_allow_html=True)
