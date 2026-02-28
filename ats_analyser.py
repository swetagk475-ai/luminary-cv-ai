import re

def calculate_ats_score(resume_data):
    """
    Evaluates the resume based on structure, completeness, and formatting.
    Returns a score (0-100) and list of improvement suggestions.
    """
    score = 0
    feedback = []
    
    # 1. Check for Essential Sections (25 Points)
    sections = {
        "summary": "Professional Summary",
        "exp": "Work Experience",
        "edu": "Education",
        "skills": "Skills Section"
    }
    for key, label in sections.items():
        if len(resume_data.get(key, "")) > 20:
            score += 6.25
        else:
            feedback.append(f"⚠️ Missing or too short: {label}")

    # 2. Contact Information Check (15 Points)
    if "@" in resume_data.get("email", ""):
        score += 7.5
    else:
        feedback.append("❌ Valid Email address is required.")
    
    if len(resume_data.get("name", "")) > 3:
        score += 7.5
    else:
        feedback.append("❌ Full Name is missing.")

    # 3. Readability & Length (20 Points)
    word_count = len(resume_data.get("exp", "").split()) + len(resume_data.get("summary", "").split())
    if 200 <= word_count <= 600:
        score += 20
    elif word_count < 200:
        score += 10
        feedback.append("💡 Your resume is a bit thin. Try adding more detail to your experience.")
    else:
        score += 15
        feedback.append("📏 Your resume is very long. Recruiters prefer concise descriptions.")

    # 4. Keyword Density (40 Points)
    # Common industry standard keywords
    industry_keywords = ["leadership", "management", "developed", "strategy", "project", "data", "analysis", "team"]
    found_keywords = [w for w in industry_keywords if w in resume_data.get("exp", "").lower()]
    
    keyword_score = (len(found_keywords) / len(industry_keywords)) * 40
    score += keyword_score
    
    if len(found_keywords) < 3:
        feedback.append("🔑 Action verbs missing: Use words like 'Managed', 'Developed', or 'Spearheaded'.")

    return round(score), feedback