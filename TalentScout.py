# Install Dependencies
!pip install -q streamlit pyngrok groq validators vaderSentiment sqlalchemy

# Commented out IPython magic to ensure Python compatibility.
# # Backend
# %%writefile backend.py
# import os
# import re
# import json
# from groq import Groq
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from sqlalchemy import create_engine, Column, String, Integer, Text
# from sqlalchemy.orm import declarative_base, sessionmaker
# GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# if not GROQ_API_KEY:
#     GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)
# analyzer = SentimentIntensityAnalyzer()
# 
# # DATABASE (SQLite)
# Base = declarative_base()
# class Candidate(Base):
#     __tablename__ = "candidates"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)
#     phone = Column(String)
#     experience = Column(String)
#     position = Column(String)
#     location = Column(String)
#     tech_stack = Column(Text)
#     sentiment = Column(String)
# engine = create_engine("sqlite:///candidates.db", echo=False)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# 
# # VALIDATION
# def validate_email(email):
#     return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
# def validate_phone(phone):
#     return phone.isdigit() and len(phone) >= 10
# def validate_experience(exp):
#     try:
#         return float(exp) >= 0
#     except:
#         return False
# 
# # TECH NORMALIZATION
# TECH_MAP = {
#     "py": "Python",
#     "python3": "Python",
#     "js": "JavaScript",
#     "reactjs": "React",
#     "nodejs": "Node.js",
#     "sql": "SQL",
#     "mysql": "MySQL",
#     "postgres": "PostgreSQL",
#     "postgresql": "PostgreSQL"
# }
# def normalize_tech_stack(stack):
#     items = [s.strip().lower() for s in stack.split(",") if s.strip()]
#     normalized = [TECH_MAP.get(i, i.capitalize()) for i in items]
#     seen = set()
#     result = []
#     for t in normalized:
#         if t not in seen:
#             seen.add(t)
#             result.append(t)
#     return result
# 
# # SENTIMENT
# def analyze_sentiment(text):
#     score = analyzer.polarity_scores(text)
#     if score["compound"] >= 0.05:
#         return "Positive"
#     elif score["compound"] <= -0.05:
#         return "Negative"
#     return "Neutral"
# 
# # DATABASE SAVE
# def save_candidate(data, sentiment):
#     session = Session()
#     candidate = Candidate(
#         name=data.get("name"),
#         email=data.get("email"),
#         phone=data.get("phone"),
#         experience=data.get("experience"),
#         position=data.get("position"),
#         location=data.get("location"),
#         tech_stack=", ".join(data.get("tech_stack", [])),
#         sentiment=sentiment
#     )
#     session.add(candidate)
#     session.commit()
#     session.close()
# 
# # JSON EXPORT
# def export_to_json(data, path="candidate_data.json"):
#     with open(path, "w") as f:
#         json.dump(data, f, indent=4)
# 
# # LLM CALL
# def llm_call(prompt):
#     try:
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",  # ✅ latest working model
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print("❌ DEBUG ERROR:", str(e))
#         return f"❌ ERROR: {str(e)}"
# 
# # QUESTION GENERATION
# def generate_questions(tech_stack, experience, history):
#     prompt = f"""
# You are a technical interviewer.
# 
# Conversation:
# {history}
# 
# Candidate Experience: {experience}
# Tech Stack: {tech_stack}
# 
# Generate 3-5 practical, scenario-based interview questions per technology.
# Group questions by technology.
# """
#     return llm_call(prompt)
# 
# # CONTEXTUAL RESPONSE
# def contextual_response(user_input, history):
#     prompt = f"""
# Conversation:
# {history}
# 
# User input:
# {user_input}
# 
# Respond professionally and keep the conversation within hiring context.
# """
#     return llm_call(prompt)

# Commented out IPython magic to ensure Python compatibility.
# # Streamlit App
# %%writefile app.py
# import streamlit as st
# from backend import *
# st.set_page_config(page_title="AI Hiring Assistant", layout="centered")
# 
# # 🎨 CUSTOM CSS
# st.markdown("""
# <style>
# .main {
#     background: linear-gradient(to right, #f5f7fa, #c3cfe2);
# }
# h1 {
#     text-align: center;
#     color: #2c3e50;
# }
# .chat-message {
#     padding: 10px;
#     border-radius: 10px;
#     margin-bottom: 10px;
# }
# </style>
# """, unsafe_allow_html=True)
# 
# # HEADER
# st.markdown("<h1>🤖 TalentScout AI Hiring Assistant</h1>", unsafe_allow_html=True)
# st.caption("🚀 Smart Candidate Screening System")
# 
# # SIDEBAR
# with st.sidebar:
#     st.title("📋 About")
#     st.write("AI-powered hiring assistant that screens candidates and generates technical questions.")
#     st.markdown("---")
#     st.subheader("💡 Features")
#     st.write("""
#     - Context-aware chatbot
#     - Tech-based question generation
#     - Sentiment analysis
#     - Data storage (SQLite + JSON)
#     """)
# 
# # SESSION INIT
# if "step" not in st.session_state:
#     st.session_state.step = "name"
#     st.session_state.data = {}
#     st.session_state.messages = []
#     st.session_state.progress = 0
# 
# # GREETING
# if "initialized" not in st.session_state:
#     st.session_state.initialized = True
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": "Hello! I'm your AI Hiring Assistant.\n\nWhat is your full name?"
#     })
# 
# # PROGRESS BAR
# steps = ["name", "email", "phone", "experience", "position", "location", "tech", "questions"]
# progress_value = steps.index(st.session_state.step) / len(steps) if st.session_state.step in steps else 1
# st.progress(progress_value)
# 
# # CHAT DISPLAY
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])
# 
# # HELPERS
# def add_msg(role, content):
#     st.session_state.messages.append({"role": role, "content": content})
# def get_history():
#     return "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
# 
# # MAIN LOGIC
# def process(user_input):
#     step = st.session_state.step
#     if user_input.lower() in ["exit", "quit", "bye"]:
#         st.session_state.step = "end"
#         return "👋 Thank you! We will contact you."
#     if step == "name":
#         st.session_state.data["name"] = user_input
#         st.session_state.step = "email"
#         return "📧 Enter your email."
#     elif step == "email":
#         if validate_email(user_input):
#             st.session_state.data["email"] = user_input
#             st.session_state.step = "phone"
#             return "📱 Enter phone number."
#         return "❌ Invalid email."
#     elif step == "phone":
#         if validate_phone(user_input):
#             st.session_state.data["phone"] = user_input
#             st.session_state.step = "experience"
#             return "💼 Years of experience?"
#         return "❌ Invalid phone."
#     elif step == "experience":
#         if validate_experience(user_input):
#             st.session_state.data["experience"] = user_input
#             st.session_state.step = "position"
#             return "🎯 Desired role?"
#         return "❌ Invalid input."
#     elif step == "position":
#         st.session_state.data["position"] = user_input
#         st.session_state.step = "location"
#         return "📍 Your location?"
#     elif step == "location":
#         st.session_state.data["location"] = user_input
#         st.session_state.step = "tech"
#         return "🧠 Enter tech stack (comma separated)."
#     elif step == "tech":
#         normalized = normalize_tech_stack(user_input)
#         st.session_state.data["tech_stack"] = normalized
#         st.session_state.step = "questions"
#         with st.spinner("⚡ Generating questions..."):
#             questions = generate_questions(
#                 normalized,
#                 st.session_state.data["experience"],
#                 get_history()
#             )
#         if "❌ ERROR" in questions:
#             return "⚠️ Failed to generate questions. Try again."
#         return f"📝 Technical Questions:\n\n{questions}"
#     elif step == "questions":
#         sentiment = analyze_sentiment(user_input)
#         save_candidate(st.session_state.data, sentiment)
#         export_to_json(st.session_state.data)
#         st.session_state.step = "end"
#         summary = "\n".join([f"**{k.capitalize()}**: {v}" for k, v in st.session_state.data.items()])
#         return f"""✅ **Submission Complete!**
# 
# 📊 **Candidate Summary:**
# {summary}
# 
# 🧠 **Sentiment:** {sentiment}
# 
# 🎉 We will contact you soon!"""
#     else:
#         return contextual_response(user_input, get_history())
# 
# # INPUT
# user_input = st.chat_input("💬 Type your response...")
# if user_input and user_input.strip():
#     add_msg("user", user_input)
#     response = process(user_input)
#     add_msg("assistant", response)
#     st.rerun()

# Run Streamlit App
from pyngrok import ngrok
ngrok.kill()
get_ipython().system_raw('streamlit run app.py --server.port 8501 &')
public_url = ngrok.connect(8501)
print("🚀 Your App URL:", public_url)
