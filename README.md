# ✨ Luminary CV: Agentic Resume & Portfolio Builder

Luminary CV is a high-performance AI-driven platform that transforms raw career data into professional resumes and digital portfolios. It uses a **Multi-Agent Orchestration** system to analyze job descriptions and provide semantic matching scores.



---

## 🚀 Key Features

* **✨ AI Resume Designer:** Generate Modern, Classic, or Professional resumes using dynamic Jinja2 templates.
* **📈 Agentic JD Matcher:** * **Agent 1 (Analyzer):** Extracts technical keywords and requirements from any Job Description.
    * **Agent 2 (Matcher):** Performs semantic analysis between your resume and the JD to provide a compatibility score.
* **🌙 Deep Space Mode:** A premium, high-contrast dark UI for a modern developer experience.
* **🌐 Web Portfolio:** Instantly render a hosted digital portfolio based on your resume data.

---

## 🛠️ Technical Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Engine:** HuggingFace / Groq (via custom `AIEngine` class)
* **Templating:** [Jinja2](https://palletsprojects.com/p/jinja/) for HTML/CSS generation
* **Logic:** Multi-agent prompt engineering and Regex-based data cleaning.

---

## 📦 Installation & Local Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/swetagk475-ai/luminary-cv-ai.git](https://github.com/swetagk475-ai/luminary-cv-ai.git)
   cd luminary-cv-ai
