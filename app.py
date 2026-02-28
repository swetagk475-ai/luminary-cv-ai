import streamlit as st
from jinja2 import Environment, FileSystemLoader
from tone_engine import AIEngine
from jd_matcher import match_job_description 
from resume_classic import generate_classic
from resume_modern import generate_modern
from resume_professional import generate_professional

# Initialize AI Engine
ai = AIEngine()
# --- UPDATED AGENT FUNCTIONS ---

import re 

def agent_analyze_jd(jd_text):
    prompt = f"""
    [INST] Act as a Technical Recruiter. 
    TASK: Extract only the technical skills and tools from the JD below.
    JD: {jd_text}
    
    FORMAT: Return ONLY a comma-separated list of keywords. 
    Example: Python, AWS, Docker, React.
    Do not write sentences. [/INST]
    """
    return ai.process_text(prompt, task="summary") 

def agent_semantic_match(resume_text, extracted_keywords):
    prompt = f"""
    [INST] Compare Resume to Keywords.
    KEYWORDS: {extracted_keywords}
    RESUME: {resume_text}
    TASK: Provide a compatibility score between 0 and 100.
    FORMAT: Your response MUST include the score as 'MATCH_SCORE: X' where X is the number. [/INST]
    """
    return ai.process_text(prompt, task="summary")
st.set_page_config(page_title="Luminary CV", layout="wide", page_icon="✨")

# --- 1. INITIALIZE SESSION STATE ---
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {
        "name": "", "email": "", "summary": "", 
        "skills": "", "exp": "", "edu": "", "projects": ""
    }

if 'template_choice' not in st.session_state:
    st.session_state.template_choice = "Modern"

# --- 2. SIDEBAR NAVIGATION & THEME LOGIC ---
with st.sidebar:
    # 2.1 The Toggle
    is_dark = st.toggle("🌙 Deep Space Mode", value=True)
    
    # 2.2 Define Theme Variables based on Toggle
    if is_dark:
        primary = "#00f2fe"    # Cyan
        text_main = "#FFFFFF"  # White
        sidebar_bg = "#0a0f1e" # Dark Space
    else:
        primary = "#0072ff"    # IBM Blue
        text_main = "#1f2937"  # Dark Grey
        sidebar_bg = "#f0f2f6" # Light Grey

    # 2.3 Dynamic Sidebar Title
    st.markdown(f"""
        <h1 style='color: {primary}; font-size: 2.2rem; font-weight: 800; margin-bottom: 0; text-shadow: 0 0 10px {primary}33;'>
            LUMINARY CV
        </h1>
    """, unsafe_allow_html=True)
    
    st.divider()
    mode = st.radio("SELECT TOOL", ["✨ Resume Designer", "📈 JD Matcher", "🌐 Web Portfolio"])
    st.divider()
    
    # Dynamic Caption
    st.markdown(f"<p style='color: {primary}; opacity: 0.7; font-size: 0.8rem;'>v2.2.0 - Premium Edition</p>", unsafe_allow_html=True)

# --- 3. CUSTOM CSS ---
st.markdown(f"""
    <style>
    /* Hide Default Streamlit Header */
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0) !important;
        color: transparent !important;
    }}

    /* Global App Background */
    .stApp {{
        background: {sidebar_bg} !important;
        color: {text_main};
    }}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {primary}33;
    }}
    
    /* Sidebar Text & Labels */
    [data-testid="stSidebar"] .stText, 
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .st-bd {{
        color: {primary} !important;
    }}

    /* Glowing Button */
    .stButton > button {{
        --glow-color: {primary};
        --glow-size: 12px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border-radius: 8px;
        border: none;
        color: #fff !important;
        background: linear-gradient(90deg, #111827, #374151) !important;
        cursor: pointer;
        position: relative;
        box-shadow: 0 0 var(--glow-size) {primary}55;
        transition: transform 200ms ease, box-shadow 200ms ease;
        width: 100%;
    }}

    .stButton > button:hover {{
        transform: translateY(-3px) !important;
        box-shadow: 0 0 calc(var(--glow-size) * 1.6) {primary} !important;
        color: {primary} !important;
    }}

    /* Floating Cards Animation */
    .bg-animation {{
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; pointer-events: none;
    }}
    .floating-card {{
        position: absolute; width: 150px; height: 200px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid {primary}33; border-radius: 10px;
        animation: float 20s infinite linear;
    }}
    @keyframes float {{
        0% {{ transform: translateY(110vh) rotate(0deg); opacity: 0; }}
        10% {{ opacity: 0.3; }}
        100% {{ transform: translateY(-20vh) rotate(360deg); opacity: 0; }}
    }}

    /* Inputs & Typography */
    h1 {{ font-size: 3.5rem !important; font-weight: 800; color: {text_main}; }}
    h2 {{ font-size: 2.2rem !important; color: {primary}; border-bottom: 2px solid {primary}33; }}
    label p {{ font-size: 1.1rem !important; font-weight: 700; color: {primary} !important; }}
    
    .stTextInput>div>div, .stTextArea>div>textarea {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: {text_main} !important;
        border: 1px solid {primary}44 !important;
        border-radius: 12px !important;
    }}
    </style>
    
    <div class="bg-animation">
        <div class="floating-card" style="left: 10%; animation-delay: 0s;"></div>
        <div class="floating-card" style="left: 80%; animation-delay: 5s;"></div>
        <div class="floating-card" style="left: 45%; animation-delay: 12s;"></div>
    </div>
""", unsafe_allow_html=True)

# --- 4. APP LOGIC ---

res = st.session_state.resume_data

if mode == "✨ Resume Designer":
    st.title("Resume Designer ✨")
    
    template = st.selectbox(
        "CHOOSE STYLE", ["Modern", "Classic", "Professional"],
        index=["Modern", "Classic", "Professional"].index(st.session_state.template_choice)
    )
    st.session_state.template_choice = template

    # Generate HTML content
    if template == "Modern":
        html_content = generate_modern(res)
    elif template == "Classic":
        html_content = generate_classic(res)
    else:
        html_content = generate_professional(res)

    col_edit, col_prev = st.columns([1, 1.2], gap="large")

    with col_edit:
        st.header("🛠️ Editor")
        res['name'] = st.text_input("FULL NAME", value=res['name'], key="name_in")
        res['email'] = st.text_input("EMAIL", value=res['email'], key="email_in")
        
        # --- SUMMARY SECTION ---
        summary_raw = st.text_area("SUMMARY", value=res['summary'], height=120, key="sum_in")
        if st.button("🪄 AI ENHANCE SUMMARY"):
            if summary_raw.strip():
                with st.spinner("Polishing summary..."):
                    enhanced = ai.process_text(summary_raw, task="summary")
                    st.session_state.resume_data['summary'] = enhanced
                    st.rerun()

        # --- SKILLS SECTION ---
        res['skills'] = st.text_input("SKILLS (Comma separated)", value=res['skills'], key="skills_input")

        # --- EXPERIENCE SECTION ---
        exp_raw = st.text_area("EXPERIENCE", value=res['exp'], height=200, key="exp_editor")
        
        if st.button("🪄 AI ENHANCE EXPERIENCE", key="ai_exp_btn"):
            if exp_raw.strip():
                with st.spinner("Optimizing bullet points..."):
                    enhanced_exp = ai.process_text(exp_raw, task="experience")
                    st.session_state.resume_data['exp'] = enhanced_exp
                    st.rerun()
        else:
            
            st.session_state.resume_data['exp'] = exp_raw
        
        # --- EDUCATION & PROJECTS ---
        res['edu'] = st.text_area("EDUCATION", value=res['edu'], height=100, key="edu_in")
        res['projects'] = st.text_area("PROJECTS", value=res['projects'], height=100, key="proj_in")

        st.divider()
        st.download_button(
            label="💾 DOWNLOAD HTML",
            data=html_content,
            file_name=f"{res['name']}_Resume.html",
            mime="text/html"
        )

    with col_prev:
        st.header("👀 Preview")
        st.components.v1.html(html_content, height=850, scrolling=True)

elif mode == "📈 JD Matcher":
    st.title("Agentic JD Matcher 📈")
    
    st.markdown("""
        <div style='background: rgba(0, 242, 254, 0.05); border-left: 5px solid #00f2fe; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
            <strong>Agentic Logic:</strong> Multi-agent orchestration for requirement extraction and semantic scoring.
        </div>
    """, unsafe_allow_html=True)

    jd_input = st.text_area("Paste Job Description here...", height=250)

    if st.button("📈 RUN AGENTIC MATCH"):
        if jd_input.strip():
            with st.spinner("🤖 Multi-Agent Analysis in progress..."):
                # 1. Gather Resume Data
                res_text = f"{res['summary']} {res['skills']} {res['exp']}"
                
                # 2. Extract Keywords (Agent 1)
                clean_keywords = agent_analyze_jd(jd_input)
                
                # 3. Get Semantic Score (Agent 2)
                raw_score_response = agent_semantic_match(res_text, clean_keywords)
                
                # --- SMART DATA CLEANING (THE MAX LOGIC) ---
                # Find all numbers between 0 and 100 in the response
                all_numbers = re.findall(r'\b\d{1,3}\b', str(raw_score_response))
                valid_scores = [int(n) for n in all_numbers if 0 <= int(n) <= 100]
                
                # Pick the highest valid number (ignores '5 years' if '85%' exists)
                if valid_scores:
                    score_num = max(valid_scores)
                else:
                    score_num = 0

                # --- DISPLAY RESULTS ---
                st.divider()
                col_score, col_keywords = st.columns([1, 2])
                
                with col_score:
                    st.metric("Compatibility Score", f"{score_num}%")
                    if score_num >= 80:
                        st.success("✅ Strong Match!")
                    elif score_num >= 50:
                        st.warning("⚠️ Average Match")
                    else:
                        st.error("🚨 Low Match")

                with col_keywords:
                    st.subheader("Extracted Requirements")
                    st.info(f"**Keywords:** {clean_keywords}")
                
                st.subheader("Agent's Reasoning")
                st.write(raw_score_response)
        else:
            st.warning("Please provide a Job Description.") 
elif mode == "🌐 Web Portfolio":
    st.title("Digital Portfolio")
    try:
        # 1. Setup Jinja2 Environment
        env = Environment(loader=FileSystemLoader('templates'))
        p_template = env.get_template('portfolio_index.html')
        
        # 2. Clean the skills string into a list of simple strings
        s_list = [s.strip() for s in res['skills'].split(',') if s.strip()]
        
        # 3. Render the template using simple variables
        portfolio_html = p_template.render(
            name=res['name'], 
            email=res['email'], 
            summary=res['summary'],
            experience=res['exp'], 
            skills=s_list, 
            projects=res['projects']
        )
        
        # 4. Display the rendered HTML
        st.components.v1.html(portfolio_html, height=1000, scrolling=True)
        
    except Exception as e:
        st.error(f"Make sure 'templates/portfolio_index.html' exists! Error: {e}")