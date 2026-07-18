import streamlit as st
import re
from huggingface_hub import InferenceClient
import os

st.set_page_config(page_title="Auto-CAD Generator", page_icon="🚗")
st.title("🚗 Automotive CATIA Macro Generator")

# Check for token in Hugging Face Space secrets
api_token = os.environ.get("HF_TOKEN")

user_input = st.text_area("Describe your component:", placeholder="e.g., Mounting bracket 120x60mm")

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
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]
                )
                
                raw_code = response.choices[0].message.content
                clean_code = re.sub(r"```[a-zA-Z]*\n|```", "", raw_code)
                
                st.code(clean_code, language="vbscript")
                st.download_button("Download .txt Macro", clean_code, "catia_macro.txt")
            except Exception as e:
                st.error(f"Error: {e}")