from io import BytesIO
import random
from difflib import SequenceMatcher
from gtts import gTTS
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Practice of English Tenses", page_icon="🎧", layout="centered"
)

st.title("🎧 Practice of English Tenses")
st.write(
    "Listen to the generated audio and type exactly the sentence you hear in English."
)

# Vocabulary bank by categories
subjects = [
    "The teacher",
    "A student",
    "My friend",
    "The chef",
    "An artist",
    "Our neighbor",
    "The doctor",
    "A mechanic",
]
verbs_present = [
    ("drinks", "drinks / drinks coffee"),
    ("prepares", "prepares"),
    ("reads", "reads"),
    ("paints", "paints"),
    ("cleans", "cleans"),
]
verbs_future = [
    ("visit", "will visit"),
    ("build", "will build"),
    ("buy", "will buy"),
    ("learn", "will learn"),
    ("organize", "will organize"),
]
objects = [
    ("coffee", "coffee"),
    ("a book", "a book"),
    ("a house", "a house"),
    ("a car", "a car"),
    ("a project", "a project"),
]
locations = [
    ("in the morning", "in the morning"),
    ("at home", "at home"),
    ("in the office", "in the office"),
    ("every day", "every day"),
]


def generate_all_sentences():
    """Generates a complete bank of possible sentences to avoid duplicates."""
    all_sentences = []
    
    # Simple Present
    for subject in subjects:
        for verb_en, verb_es in verbs_present:
            for obj_en, obj_es in objects:
                for loc_en, loc_es in locations:
                    all_sentences.append({
                        "tense": "Simple Present",
                        "en": f"{subject} {verb_en} {obj_en} {loc_en}.",
                        "es": f"{subject} {verb_es} {obj_es} {loc_es}."
                    })

    # Simple Future
    for subject in subjects:
        for verb_en, verb_es in verbs_future:
            for obj_en, obj_es in objects:
                all_sentences.append({
                    "tense": "Simple Future",
                    "en": f"{subject} will {verb_en} {obj_en} tomorrow.",
                    "es": f"{subject} {verb_es} {obj_es} tomorrow."
                })

    # Present Continuous
    for subject in subjects:
        for verb_en, verb_es in [("working on", "is working on"), ("studying", "is studying")]:
            for obj_en, obj_es in objects:
                all_sentences.append({
                    "tense": "Present Continuous",
                    "en": f"{subject} is {verb_en} {obj_en} right now.",
                    "es": f"{subject} {verb_es} {obj_es} right now."
                })
                
    return all_sentences


# Initialize session state
if "configured" not in st.session_state:
    st.session_state.configured = False
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_result = None
    st.session_state.test_questions = []
    st.session_state.chosen_tolerance = 0.85

# Initial configuration screen (before starting)
if not st.session_state.configured:
    st.subheader("⚙️ Test Settings")
    
    # Calculate the maximum number of unique sentences
    temp_bank = generate_all_sentences()
    max_questions = len(temp_bank)
    
    total_chosen = st.slider(
        "How many questions would you like in this test?",
        min_value=3,
        max_value=min(20, max_questions),
        value=5
    )

    # Grading strictness mode selector
    strictness_mode = st.select_slider(
        "Grading strictness level:",
        options=["Very Flexible (70%)", "Flexible (80%)", "Normal (85%)", "Strict (95%)", "Exact (100%)"],
        value="Normal (85%)"
    )

    # Map the selected option to a decimal threshold
    tolerance_map = {
        "Very Flexible (70%)": 0.70,
        "Flexible (80%)": 0.80,
        "Normal (85%)": 0.85,
        "Strict (95%)": 0.95,
        "Exact (100%)": 1.00
    }
    
    if st.button("🚀 Start Test"):
        st.session_state.test_questions = random.sample(temp_bank, total_chosen)
        st.session_state.chosen_tolerance = tolerance_map[strictness_mode]
        st.session_state.configured = True
        st.session_state.step = 0
        st.session_state.score = 0
        st.rerun()

else:
    total_questions = len(st.session_state.test_questions)

    # If the test is ongoing
    if st.session_state.step < total_questions:
        current_item = st.session_state.test_questions[st.session_state.step]
        
        st.subheader(
            f"Question {st.session_state.step + 1} of {total_questions}"
        )
        st.info(f"Verb Tense: **{current_item['tense']}**")

        # Generate or retrieve cached audio in session state
        if "audio_bytes" not in st.session_state or st.session_state.get("audio_step") != st.session_state.step:
            tts = gTTS(text=current_item["en"], lang="en")
            fp = BytesIO()
            tts.write_to_fp(fp)
            st.session_state.audio_bytes = fp.getvalue()
            st.session_state.audio_step = st.session_state.step

        st.audio(st.session_state.audio_bytes, format="audio/mp3")

        # Answer submission form
        with st.form(key=f"form_{st.session_state.step}"):
            user_response = st.text_input(
                "Type what you heard in English:", key=f"input_{st.session_state.step}"
            )
            submit_button = st.form_submit_button(label="Submit Answer")

            if submit_button:
                clean_original = current_item["en"].rstrip("?.!").lower()
                clean_response = user_response.rstrip("?.!").lower()

                # Similarity scoring based on the user's chosen threshold
                similarity = SequenceMatcher(None, clean_response, clean_original).ratio()

                st.session_state.answered = True
                if similarity >= st.session_state.chosen_tolerance:
                    st.session_state.score += 1
                    st.session_state.last_result = "correct"
                else:
                    st.session_state.last_result = "incorrect"
                st.rerun()

        # Display feedback if the answer has been submitted for this step
        if st.session_state.get("answered", False):
            if st.session_state.last_result == "correct":
                st.success("Correct! 🎉")
            else:
                st.error("❌ Not quite right.")
                st.write(f"**Expected answer:** {current_item['en']}")
                st.write(f"**Your answer:** {st.session_state.get('input_' + str(st.session_state.step), '')}")

            if st.button("Next Question ➡️"):
                st.session_state.step += 1
                st.session_state.answered = False
                st.rerun()

    else:
        # Final results screen
        st.balloons()
        st.success("Test Completed!")
        st.write(
            f"Your final score: **{st.session_state.score} out of {total_questions}** correct answers."
        )

        if st.button("🔄 Configure New Test"):
            st.session_state.configured = False
            st.rerun()
