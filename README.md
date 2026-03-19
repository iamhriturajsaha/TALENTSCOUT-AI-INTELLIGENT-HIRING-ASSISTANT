# TalentScout AI – Intelligent Hiring Assistant

## 📌 Project Overview

TalentScout AI – Intelligent Hiring Assistant is an AI-powered conversational system designed to automate the initial screening process of candidates for technical roles. The system leverages Large Language Models (LLMs) to intelligently collect candidate information, analyze sentiment and dynamically generate technical interview questions based on the candidate’s declared tech stack. This project demonstrates the integration of LLMs, prompt engineering, conversational AI and full-stack development to build a real-world recruitment automation tool.

## 🚀 Key Features

### 🤖 AI-Powered Conversational Interface
* Interactive chatbot built using Streamlit.
* Multi-turn conversation with context awareness.
* Structured step-by-step candidate data collection.

### 🧠 Dynamic Technical Question Generation
* Generates 3–5 tailored questions per technology.
* Adapts difficulty based on candidate experience.
* Covers real-world and scenario-based questions.

### 🔄 Context-Aware Interaction
* Maintains full conversation history.
* Ensures coherent and relevant responses.

### 📊 Sentiment Analysis
* Uses VADER sentiment analysis.
* Classifies candidate responses as -
  * Positive.
  * Neutral.
  * Negative.

### 🧩 Tech Stack Normalization
* Converts informal inputs -
  * `py → Python`
  * `reactjs → React`
* Ensures consistency in question generation.

### 💾 Data Persistence
* Stores candidate data in -
  * SQLite database.
  * JSON file export.

### 🎨 Enhanced UI/UX
* Clean chat interface.
* Progress tracking bar.
* Loading spinner for AI responses.
* Sidebar with feature overview.

## 🏗️ System Architecture

User → Streamlit UI → Session State Manager → Prompt Engine → Groq LLM → Response Generator → UI Display → Database Storage

## 🛠️ Tech Stack

| Component     | Technology               |
| ------------- | ------------------------ |
| Frontend      | Streamlit                |
| Backend       | Python                   |
| LLM           | Groq (LLaMA 3.1 Models)  |
| NLP           | VADER Sentiment Analysis |
| Database      | SQLite                   |
| Deployment    | ngrok                    |
| Data Handling | JSON                     |


## 🧠 Prompt Engineering Strategy

The system uses multiple structured prompts -

### 1. Information Gathering Prompt

Guides the chatbot to collect -

* Name.
* Email.
* Phone.
* Experience.
* Role.
* Location.
* Tech Stack.

### 2. Question Generation Prompt

* Generates technical questions based on tech stack.
* Adapts to experience level.
* Focuses on practical scenarios.

### 3. Contextual Prompt

* Maintains conversation continuity.
* Uses full chat history.

### 4. Fallback Prompt

* Handles unexpected or irrelevant inputs.
* Redirects conversation to hiring flow.

## 🔄 Workflow

1. User starts conversation.
2. Chatbot collects candidate details step-by-step.
3. User provides tech stack.
4. System -
   * Normalizes technologies.
   * Generates tailored technical questions.
5. User responds.
6. System performs sentiment analysis.
7. Data is stored in -
   * SQLite database.
   * JSON file.
8. Conversation ends with summary.

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/TALENTSCOUT-AI-INTELLIGENT-HIRING-ASSISTANT.git
cd TALENTSCOUT-AI-INTELLIGENT-HIRING-ASSISTANT
```

### 2. Set API Key

```python
import os
os.environ["GROQ_API_KEY"] = "your_api_key_here"
```

### 3. Run Application

```bash
streamlit run app.py
```

## 🔐 Data Privacy & Security

* No permanent storage of sensitive data.
* Uses local SQLite database for demo purposes.
* Follows basic GDPR-aware design principles.
* No external data sharing.

## ⚡ Challenges & Solutions

### 🔹 Challenge - API Cost Constraints

**Solution -** Used Groq API with free-tier LLaMA models.

### 🔹 Challenge - Context Management

**Solution -** Maintained full conversation history using session state.

### 🔹 Challenge - Model Deprecation

**Solution -** Implemented dynamic model selection and fallback handling.

### 🔹 Challenge - Streamlit + Environment Variables

**Solution -** Added fallback key handling for Colab environment.

## 🚀 Future Enhancements

* Resume upload & parsing (RAG pipeline).
* Admin dashboard for recruiters.
* Multi-language support.
* Voice-based interaction.
* Cloud deployment (AWS/GCP).
* Advanced analytics dashboard.

## 📊 Evaluation Alignment

| Criteria           | Implementation                     |
| ------------------ | ---------------------------------- |
| Functionality      | ✅ Complete chatbot workflow        |
| Prompt Engineering | ✅ Structured and dynamic prompts   |
| UI/UX              | ✅ Interactive and modern interface |
| Data Handling      | ✅ SQLite + JSON                    |
| Advanced Features  | ✅ Sentiment + normalization        |

## 🏆 Conclusion

TalentScout AI demonstrates how modern AI systems can enhance recruitment workflows by combining conversational AI, LLMs and intelligent automation. This project showcases practical applications of AI/ML in solving real-world business problems.
