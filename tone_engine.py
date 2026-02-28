import streamlit as st
from huggingface_hub import InferenceClient

class AIEngine:
    def __init__(self):
        self.client = None 
        try:
            self.token = st.secrets["HUGGINGFACE_API_KEY"] 
            self.repo_id = "meta-llama/Llama-3.2-3B-Instruct" 
            self.client = InferenceClient(model=self.repo_id, token=self.token)
        except Exception as e:
            st.error(f"Secret Key Error: {e}")

    def process_text(self, text, task="summary"):
        if self.client is None:
            return "AI Error: AI Engine not initialized."
            
        if not text.strip():
            return "Please provide some text to enhance."

        # --- DYNAMIC PROMPTING BASED ON TASK ---
        if task == "experience":
            system_content = (
                "You are an expert Resume Writer. Rewrite the input into high-impact, "
                "ATS-friendly bullet points. Use strong action verbs (e.g., Spearheaded, "
                "Architected, Optimized). Focus on measurable achievements. "
                "Return ONLY the bullet points."
            )
        else:
            system_content = (
                "You are a professional Resume Writer. Rewrite the input into a "
                "powerful, 3-4 sentence professional summary paragraph. Focus on "
                "years of experience and core value proposition. "
                "Return ONLY the rewritten text."
            )

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Enhance this {task}: {text}"}
        ]

        try:
            response = self.client.chat_completion(
                messages=messages,
                max_tokens=400, # Increased tokens for longer experience sections
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"AI Error during processing: {e}"