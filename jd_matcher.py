import re

def match_job_description(resume_text, jd_text):
    stop_words = {
        "with", "the", "and", "for", "join", "role", "like", "from", "that", 
        "this", "plus", "our", "strong", "requirements", "frontend", "backend"
    }
    extra_noise = {"are", "looking", "team", "core", "deep", "familiarity", "optimization", "experience"}
    stop_words.update(extra_noise)
    filler_words = {
        'must', 'will', 'you', 'seeking', 'looking', 'plus', 'preferred', 
        'required', 'join', 'team', 'expert', 'experience', 'knowledge', 
        'work', 'years', 'working', 'responsibilities', 'duties'
    }
    stop_words.update(filler_words)   
    if not resume_text.strip() or not jd_text.strip():
        return 0, ["Provide data to analyze."], set() # Return empty set for matches
    
    def get_clean_words(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text) 
        return set(text.split())

    resume_words = get_clean_words(resume_text)
    jd_words = get_clean_words(jd_text)
    
    important_jd_keywords = {word for word in jd_words if word not in stop_words and len(word) > 2}
    matches = resume_words.intersection(important_jd_keywords)
    
    if not important_jd_keywords:
        return 0, ["No keywords found."], set()
        
    score = int((len(matches) / len(important_jd_keywords)) * 100)
    missing = list(important_jd_keywords - resume_words)[:8]
    
    feedback = [f"✅ Matches found: {', '.join(list(matches)[:5])}..."]
    if score < 50:
        feedback.append("🚨 Low Match: Add more technical keywords.")
    else:
        feedback.append("✅ Strong Match!")
        
    if missing:
        feedback.append(f"💡 Missing: {', '.join(missing)}")
    
    # Return score, feedback list, and the set of matched words
    return score, feedback, matches