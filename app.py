import streamlit as st
import re
from huggingface_hub import InferenceClient
import os

# Page configuration
st.set_page_config(
    page_title="Auto-CAD Generator",
    layout="wide"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
        body {
            background-image: url('https://images.unsplash.com/photo-1502877338535-766e1452684a');
            background-size: cover;
            background-attachment: fixed;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 10px;
        }
        h1 {
            font-family: 'Trebuchet MS', sans-serif;
            color: #003366;
            text-align: center;
            font-size: 2.8em;
        }
        textarea {
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
        }
        .footer {
            text-align: center;
            font-size: 0.9em;
            color: #333333;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Automotive component Prompt to VBA Macro Generator By Ibraheem")

# Hugging Face API token
api_token = os.environ.get("HF_TOKEN")

# User input
user_input = st.text_area("Describe your component:", placeholder="e.g., Mounting bracket 120x60mm")

# Generate Macro button
if st.button("Generate Macro"):
    if not api_token:
        st.error("HF_TOKEN not found in Space Secrets.")
    elif user_input:
        with st.spinner("Generating code..."):
            try:
                client = InferenceClient(api_key=api_token)
                system_prompt = "You are a CATIA V5 expert. Output ONLY valid VBScript. Min thickness 2mm, 2mm fillets."
                
                response = client.chat_completion(
                    model="Qwen/Qwen2.5-7B-Instruct",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                
                raw_code = response.choices[0].message.content
                clean_code = re.sub(r"```[a-zA-Z]*\n|```", "", raw_code)
                
                st.code(clean_code, language="vbscript")
                st.download_button("Download .txt Macro", clean_code, "catia_macro.txt")
            except Exception as e:
                st.error(f"Error: {e}")

# Footer credit
st.markdown('<div class="footer">App made by <b>Ibraheem</b></div>', unsafe_allow_html=True)
