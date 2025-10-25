import streamlit as st
from dotenv import load_dotenv
import os
import json
from utils.gemini_chat import ask_nova

# Load Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Apply custom styling
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 🦉 Nova greets the user
st.image("assets/nova_owl.png", width=100)
st.title("🦉 Hi, I’m Nova!")
st.markdown("I'm here to guide you through stories, games, and reflections. Choose a mode and let's begin!")

# Initialize session state
if "mode" not in st.session_state:
    st.session_state.mode = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "learn_history" not in st.session_state:
    st.session_state.learn_history = []
if "play_history" not in st.session_state:
    st.session_state.play_history = []

# 🎯 Mode selection
if not st.session_state.mode:
    st.markdown("""
    ### What would you like to do today?
    1️⃣ **Play a decision game**  
    2️⃣ **Chat with Nova**  
    3️⃣ **Learn something new**  
    4️⃣ **Write a letter to your future self**
    """)
    choice = st.text_input("Enter a number (1–4):")
    if choice in ["1", "2", "3", "4"]:
        st.session_state.mode = choice
        st.rerun()

# 🎮 Mode 1: Play
if st.session_state.mode == "1":
    st.subheader("🎮 Decision Game")
    with st.spinner("🦉 Nova is thinking of a scenario..."):
        scenario = ask_nova("Give a short decision-based scenario for a teen facing peer pressure.", api_key)
    st.session_state.play_history.append(scenario)
    st.write("🦉 Nova says:", scenario)
    decision = st.radio("What would you do?", ["Say no", "Go along", "Talk to a friend", "Leave the situation"], key=len(st.session_state.play_history))
    if decision:
        st.success("🦉 Nova: Great choice! Let's talk about why that matters...")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎮 Play another"):
            st.rerun()
    with col2:
        if st.button("🔙 Exit game"):
            st.session_state.mode = None
            st.rerun()

# 💬 Mode 2: Chat
elif st.session_state.mode == "2":
    st.subheader("💬 Chat with Nova")
    for msg in st.session_state.chat_history:
        st.write(f"🧑 You: {msg['user']}")
        st.write(f"🦉 Nova: {msg['nova']}")
    prompt = st.text_input("Ask Nova anything:", key="chat")
    if prompt:
        with st.spinner("🦉 Nova is thinking..."):
            response = ask_nova(prompt, api_key)
        st.session_state.chat_history.append({"user": prompt, "nova": response})
        st.rerun()
    if st.button("🔙 Exit chat"):
        st.session_state.mode = None
        st.rerun()

# 📚 Mode 3: Learn
elif st.session_state.mode == "3":
    st.subheader("📚 Learn Something New")
    with st.spinner("🦉 Nova is fetching something insightful..."):
        fact = ask_nova("Share a short fact or insight about substance abuse prevention for teens.", api_key)
    st.session_state.learn_history.append(fact)
    st.info(f"🧠 Nova says: {fact}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Learn another"):
            st.rerun()
    with col2:
        if st.button("🔙 Exit learning"):
            st.session_state.mode = None
            st.rerun()

# 💌 Mode 4: Letter
elif st.session_state.mode == "4":
    st.subheader("💌 Letter to Future Me")
    with st.spinner("🦉 Nova is thinking..."):
        encouragement = ask_nova("Motivate a teen to write a heartfelt letter to their future self.", api_key)
    st.write("🦉 Nova:", encouragement)
    letter = st.text_area("Write your letter here:")
    if letter:
        with st.spinner("🦉 Saving your letter..."):
            with open("data/letters.json", "a") as f:
                json.dump({"letter": letter}, f)
        st.success("💌 Saved! You're building your story, one word at a time.")
    if st.button("🔙 Exit letter mode"):
        st.session_state.mode = None
        st.rerun()

# 🦉 Nova sign-off
st.markdown("---")
st.write("🦉 Nova is always here when you need a guide.")
st.image("assets/nova_owl.png", width=100)
