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

# DATABASE
DB_PATH = os.path.join("/tmp", "candidates.db") 
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
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
    try:
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
    except Exception as e:
        session.rollback()
        print("❌ DB ERROR:", str(e))
    finally:
        session.close()

# JSON EXPORT
def export_to_json(data, path="/tmp/candidate_data.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# 🤖 LLM CALL
def llm_call(prompt):
    models = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]
    for model in models:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Model {model} failed:", str(e))
            continue
    return "⚠️ Unable to generate questions right now. Please try again later."

# QUESTION GENERATION
def generate_questions(tech_stack, experience, history):
    prompt = f"""
You are a professional technical interviewer.

Candidate Experience: {experience} years
Tech Stack: {tech_stack}

Generate technical interview questions in a CLEAN and STRUCTURED format.

STRICT RULES:
1. Group questions by technology
2. Use clear headings (## Technology Name)
3. Generate EXACTLY 3 questions per technology
4. Keep questions concise and professional
5. Do NOT mix languages in same section
6. Format properly with numbering
7. Do NOT include explanations or answers

FORMAT:

## Python
1. Question
2. Question
3. Question

## Java
1. Question
2. Question
3. Question

Now generate the questions.
"""
    return llm_call(prompt)

# CONTEXT RESPONSE
def contextual_response(user_input, history):
    prompt = f"""
Conversation:
{history}

User input:
{user_input}

Respond professionally and keep the conversation within hiring context.
"""
    return llm_call(prompt)
