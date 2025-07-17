
import streamlit as st

# Setup
st.set_page_config(page_title="Klaverjassen", layout="centered")

# Player names
if 'names_set' not in st.session_state:
    st.session_state.names_set = False
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

# Score input
with st.form("score_form"):
    scorer = st.radio("Select player:", [player1, player2], horizontal=True)

    col = st.columns([1, 2, 1])[1]  # Centered column
    with col:
        score = st.number_input(
            f"Enter score for {scorer}", min_value=0, max_value=162, step=1, key="score_input"
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
        st.session_state.player1_score += p1_score
        st.session_state.player2_score += p2_score
        st.session_state.history.append((p1_score, p2_score))
        st.session_state.score_input = 0  # Reset input

# Scores
st.subheader("📊 Current Scores")
cols = st.columns(2)
cols[0].metric(player1, st.session_state.player1_score)
cols[1].metric(player2, st.session_state.player2_score)

# History
st.subheader("📜 Round History")
for i, (p1, p2) in enumerate(st.session_state.history):
    col1, col2, col3 = st.columns([3, 3, 1])
    col1.write(f"{player1}: {p1}")
    col2.write(f"{player2}: {p2}")
    if col3.button("❌", key=f"del_{i}"):
        st.session_state.player1_score -= p1
        st.session_state.player2_score -= p2
        st.session_state.history.pop(i)
        st.experimental_rerun()
