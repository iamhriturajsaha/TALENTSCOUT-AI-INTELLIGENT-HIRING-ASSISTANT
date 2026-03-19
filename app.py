import streamlit as st
from backend import *
st.set_page_config(page_title="AI Hiring Assistant", layout="centered")

# 🎨 CUSTOM CSS 
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #f5f7fa, #c3cfe2);
}
h1 {
    text-align: center;
    color: #2c3e50;
}
.chat-message {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1>🤖 TalentScout AI Hiring Assistant</h1>", unsafe_allow_html=True)
st.caption("🚀 Smart Candidate Screening System")

# SIDEBAR
with st.sidebar:
    st.title("📋 About")
    st.write("AI-powered hiring assistant that screens candidates and generates technical questions.")
    st.markdown("---")
    st.subheader("💡 Features")
    st.write("""
    - Context-aware chatbot  
    - Tech-based question generation  
    - Sentiment analysis  
    - Data storage (SQLite + JSON)  
    """)

# SESSION INIT
if "step" not in st.session_state:
    st.session_state.step = "name"
    st.session_state.data = {}
    st.session_state.messages = []
    st.session_state.progress = 0

# GREETING
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your AI Hiring Assistant.\n\nWhat is your full name?"
    })

# PROGRESS BAR
steps = ["name", "email", "phone", "experience", "position", "location", "tech", "questions"]
progress_value = steps.index(st.session_state.step) / len(steps) if st.session_state.step in steps else 1
st.progress(progress_value)

# CHAT DISPLAY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# HELPERS
def add_msg(role, content):
    st.session_state.messages.append({"role": role, "content": content})
def get_history():
    return "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])

# MAIN LOGIC
def process(user_input):
    step = st.session_state.step
    if user_input.lower() in ["exit", "quit", "bye"]:
        st.session_state.step = "end"
        return "👋 Thank you! We will contact you."
    if step == "name":
        st.session_state.data["name"] = user_input
        st.session_state.step = "email"
        return "📧 Enter your email."
    elif step == "email":
        if validate_email(user_input):
            st.session_state.data["email"] = user_input
            st.session_state.step = "phone"
            return "📱 Enter phone number."
        return "❌ Invalid email."
    elif step == "phone":
        if validate_phone(user_input):
            st.session_state.data["phone"] = user_input
            st.session_state.step = "experience"
            return "💼 Years of experience?"
        return "❌ Invalid phone."
    elif step == "experience":
        if validate_experience(user_input):
            st.session_state.data["experience"] = user_input
            st.session_state.step = "position"
            return "🎯 Desired role?"
        return "❌ Invalid input."
    elif step == "position":
        st.session_state.data["position"] = user_input
        st.session_state.step = "location"
        return "📍 Your location?"
    elif step == "location":
        st.session_state.data["location"] = user_input
        st.session_state.step = "tech"
        return "🧠 Enter tech stack (comma separated)."
    elif step == "tech":
        normalized = normalize_tech_stack(user_input)
        st.session_state.data["tech_stack"] = normalized
        st.session_state.step = "questions"
        with st.spinner("⚡ Generating questions..."):
            questions = generate_questions(
                normalized,
                st.session_state.data["experience"],
                get_history()
            )
        if "❌ ERROR" in questions:
            return "⚠️ Failed to generate questions. Try again."
        return f"📝 Technical Questions:\n\n{questions}"
    elif step == "questions":
        sentiment = analyze_sentiment(user_input)
        save_candidate(st.session_state.data, sentiment)
        export_to_json(st.session_state.data)
        st.session_state.step = "end"
        summary = "\n".join([f"**{k.capitalize()}**: {v}" for k, v in st.session_state.data.items()])
        return f"""✅ **Submission Complete!**

📊 **Candidate Summary:**
{summary}

🧠 **Sentiment:** {sentiment}

🎉 We will contact you soon!"""
    else:
        return contextual_response(user_input, get_history())

# INPUT
user_input = st.chat_input("💬 Type your response...")
if user_input and user_input.strip():
    add_msg("user", user_input)
    response = process(user_input)
    add_msg("assistant", response)
    st.rerun()
