import streamlit as st
import subprocess
import json
import datetime

st.set_page_config(page_title="SAT to JSON - DocMind Light")
st.title("📄 SAT Question Converter with Ollama + Phi-3")

uploaded_file = st.file_uploader("Upload a .txt file with SAT questions", type="txt")

if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")

    st.subheader("📝 Prompt Preview")
    user_prompt = f"""You will be given SAT-style questions inside triple backticks. For each question, return a JSON object with the following fields: 

- difficulty (easy/medium/hard)
- domain (Reading, Math, etc.)
- skill (comprehension, algebra, etc.)
- passage_text
- question
- answers (A, B, C, D)
- correct_answer
- explanation

Wrap all responses in a JSON array. Questions:
{input_text}
```"""

    st.code(user_prompt, language="markdown")

    if st.button("Send to Phi-3 via Ollama"):
        with st.spinner("Thinking..."):
            result = subprocess.run(
                ["ollama", "run", "phi3", user_prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                st.error("Error running Ollama:\n" + result.stderr)
            else:
                st.success("✅ Phi-3 Response")
                try:
                    structured = json.loads(result.stdout)
                    st.json(structured)
                    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                    filename = f"sat_output_{timestamp}.json"
                    st.download_button(
                        label="📥 Download JSON Output",
                        data=json.dumps(structured, indent=2),
                        file_name=filename,
                        mime="application/json"
                    )
                except Exception:
                    st.text(result.stdout)
