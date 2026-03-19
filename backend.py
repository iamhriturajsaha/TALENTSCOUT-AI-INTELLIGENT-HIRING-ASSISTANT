import os
import re
import json
from groq import Groq
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)
analyzer = SentimentIntensityAnalyzer()

# DATABASE (SQLite)
Base = declarative_base()
class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    experience = Column(String)
    position = Column(String)
    location = Column(String)
    tech_stack = Column(Text)
    sentiment = Column(String)
engine = create_engine("sqlite:///candidates.db", echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# VALIDATION
def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 10
def validate_experience(exp):
    try:
        return float(exp) >= 0
    except:
        return False

# TECH NORMALIZATION
TECH_MAP = {
    "py": "Python",
    "python3": "Python",
    "js": "JavaScript",
    "reactjs": "React",
    "nodejs": "Node.js",
    "sql": "SQL",
    "mysql": "MySQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL"
}
def normalize_tech_stack(stack):
    items = [s.strip().lower() for s in stack.split(",") if s.strip()]
    normalized = [TECH_MAP.get(i, i.capitalize()) for i in items]
    seen = set()
    result = []
    for t in normalized:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result

# SENTIMENT
def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)
    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    return "Neutral"

# DATABASE SAVE
def save_candidate(data, sentiment):
    session = Session()
    candidate = Candidate(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        experience=data.get("experience"),
        position=data.get("position"),
        location=data.get("location"),
        tech_stack=", ".join(data.get("tech_stack", [])),
        sentiment=sentiment
    )
    session.add(candidate)
    session.commit()
    session.close()

# JSON EXPORT
def export_to_json(data, path="candidate_data.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# LLM CALL 
def llm_call(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ latest working model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ DEBUG ERROR:", str(e))
        return f"❌ ERROR: {str(e)}"

# QUESTION GENERATION
def generate_questions(tech_stack, experience, history):
    prompt = f"""
You are a technical interviewer.

Conversation:
{history}

Candidate Experience: {experience}
Tech Stack: {tech_stack}

Generate 3-5 practical, scenario-based interview questions per technology.
Group questions by technology.
"""
    return llm_call(prompt)

# CONTEXTUAL RESPONSE
def contextual_response(user_input, history):
    prompt = f"""
Conversation:
{history}

User input:
{user_input}

Respond professionally and keep the conversation within hiring context.
"""
    return llm_call(prompt)
