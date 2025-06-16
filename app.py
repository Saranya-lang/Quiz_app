import streamlit as st
import re
import time
from dotenv import load_dotenv

from quiz_logic import generate_quiz
from audio_utils import generate_audio
from email_utils import send_result

load_dotenv()

st.set_page_config("AI Quiz Generator", layout="wide")
st.title("🧠 AI-Powered Quiz Generator")

# Step 1: User input
with st.form("quiz_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Email")
    topic = st.text_input("Quiz Topic (e.g. Solar System, Python, World War 2)")
    submitted = st.form_submit_button("Generate Quiz")

if submitted:
    st.session_state["quiz_started"] = True
    raw_quiz = generate_quiz(topic)

    # Parse questions and answers
    questions = re.findall(
        r"Q\d+\.(.*?)\na\)(.*?)\nb\)(.*?)\nc\)(.*?)\nd\)(.*?)\nAnswer: ([a-d])",
        raw_quiz, re.DOTALL
    )

    st.session_state["questions"] = questions
    st.session_state["user_answers"] = {}
    st.session_state["name"] = name
    st.session_state["email"] = email
    st.session_state["start_time"] = time.time()  # Store start time as timestamp

# Step 2: Display quiz with timer
if st.session_state.get("quiz_started") and "completed" not in st.session_state:
    st.subheader("📋 Your Quiz - 5 Minutes Timer")
    QUIZ_DURATION = 5 * 60  # seconds

    elapsed = time.time() - st.session_state["start_time"]
    remaining = max(QUIZ_DURATION - int(elapsed), 0)

    minutes, seconds = divmod(remaining, 60)
    st.warning(f"⏱️ Time Left: {minutes:02}:{seconds:02}")

    # Auto-submit if time is up
    if elapsed >= QUIZ_DURATION:
        st.session_state["auto_submitted"] = True
        st.session_state["completed"] = True
        st.rerun()

    # Show questions only if not auto-submitted
    if not st.session_state.get("auto_submitted"):
        questions = st.session_state["questions"]
        for idx, q in enumerate(questions):
            question_text, *options, correct = q
            st.markdown(f"**Q{idx+1}. {question_text.strip()}**")

            # Generate and play audio
            audio_path = generate_audio(question_text.strip(), [o.strip() for o in options])
            with open(audio_path, "rb") as f:
                st.audio(f.read(), format="audio/mp3")

            # Display options with no default selection
            if len(options) == 4:
                key = f"q{idx}"
                st.radio(
                    label="Choose an answer:",
                    options=[
                        f"a) {options[0].strip()}",
                        f"b) {options[1].strip()}",
                        f"c) {options[2].strip()}",
                        f"d) {options[3].strip()}"
                    ],
                    key=key,
                    index=None,
                    label_visibility="collapsed"
                )
            else:
                st.error(f"Invalid number of options for question {idx+1}. Expected 4 but got {len(options)}.")
    else:
        st.info("⛔ Time's up! Quiz questions are now hidden.")

    # Disable the Submit button after timeout
    submit_disabled = (time.time() - st.session_state["start_time"]) >= QUIZ_DURATION
    if st.button("Submit Quiz", disabled=submit_disabled):
        st.session_state["completed"] = True
        st.rerun()

    if submit_disabled:
        st.info("🕔 Submission disabled: time is up and quiz was auto-submitted.")

# Step 3: Scoring and Email
if st.session_state.get("completed"):
    questions = st.session_state["questions"]
    score = 0
    total = len(questions)

    for idx, q in enumerate(questions):
        key = f"q{idx}"
        selected = (st.session_state.get(key) or "").lower()[:1]
        correct = q[-1]
        if selected == correct:
            score += 1

    if st.session_state.get("auto_submitted"):
        st.error("⏰ Time's up! Your quiz was auto-submitted.")

    st.success(f"✅ You scored {score}/{total}")
    send_result(st.session_state["email"], st.session_state["name"], score, total)
    st.balloons()
    st.write("Your results have been emailed to you.")
    st.session_state.clear()
