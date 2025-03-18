import streamlit as st
import time
from utils import generate_questions
from data_handler import save_personal_info, save_technical_responses, load_personal_info, load_technical_responses
import re

st.title("TalentScout Hiring Assistant 🤖")
st.caption("Let's begin your initial screening!")

# Information gathering steps
steps = [
    ("name", "May I have your full name?"),
    ("email", "What's your email address?"),
    ("phone", "Could you share your phone number?"),
    ("experience", "How many years of professional experience do you have?"),
    ("position", "What position are you applying for?"),
    ("location", "Where are you currently located?"),
    ("tech_stack", "Please list your technical skills (comma-separated):\nExample: Python, React, AWS")
]

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hey! I will assist you in applying for jobs."}]
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "current_step" not in st.session_state:
    st.session_state.current_step = -1
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "question_index" not in st.session_state:
    st.session_state.question_index = 0


def validate_input(key, value):
    if key == "name":
        return bool(re.match(r"^[a-zA-Z\s]+$", value))  # Only alphabets and spaces
    elif key == "email":
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value))  # Email regex
    elif key == "phone":
        return bool(re.match(r"^\d{10}$", value))  # 10-digit phone number
    elif key == "experience":
        try:
            return float(value) >= 0  # Positive number
        except ValueError:
            return False
    elif key == "tech_stack":
        return len(value.split(",")) > 0  # At least one skill listed
    return True  # Default to valid for other fields

def append_message(role, content):
    if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["content"] != content:
        st.session_state.messages.append({"role": role, "content": content})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gather personal information
if st.session_state.current_step < len(steps):
    key, question = steps[st.session_state.current_step]
    prompt = st.chat_input("Type your responses here...")

    if prompt:
        if validate_input(key, prompt):
            st.session_state.user_info[key] = prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.current_step += 1
        else:
            # st.session_state.messages.append({"role": "assistant", "content": f"Invalid input for {key}. Please try again."})
            append_message("assistant", f"Invalid input for {key}. Please try again.")
        if st.session_state.current_step < len(steps):
            next_question = steps[st.session_state.current_step][1]
            # st.session_state.messages.append({"role": "assistant", "content": next_question})
            append_message("assistant", next_question)
        else:
            # st.session_state.messages.append({"role": "assistant", "content": "Thank you! Generating technical questions..."})
            append_message("assistant", "Thank you! Generating technical questions...")
            st.session_state.current_step = len(steps)  # Mark completion

        st.rerun()


# Generate and ask technical questions
if st.session_state.current_step == len(steps):
    save_personal_info(st.session_state.user_info)
    tech_stack = [t.strip() for t in st.session_state.user_info.get("tech_stack", "").split(",") if t.strip()]
    experience = st.session_state.user_info.get("experience", "N/A")

    if not st.session_state.tech_questions:
        for tech in tech_stack:
            questions = generate_questions(tech, experience)
            st.session_state.tech_questions.extend([(tech, q) for q in questions.split("|||")])

    if st.session_state.question_index < len(st.session_state.tech_questions):
        tech, question = st.session_state.tech_questions[st.session_state.question_index]
        with st.chat_message("assistant"):
            st.markdown(f"**{tech}**: {question}")

        response = st.chat_input("Your response:")

        if response:
            st.session_state.responses[question] = response
            st.session_state.messages.append({"role":"assistant", "content":question})
            st.session_state.messages.append({"role": "user", "content": response})

            st.session_state.question_index += 1
            if st.session_state.question_index == len(st.session_state.tech_questions):
                save_technical_responses(st.session_state.responses)
                st.session_state.messages.append({"role": "assistant", "content": "Thank you for completing the technical round! Our team will review your responses."})

            st.rerun()
