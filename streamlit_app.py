import streamlit as st
import os

# 🔑 API CONFIGURATION - Use environment variables or secrets
try:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
except:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("🔑 Configure OPENAI_API_KEY in secrets or environment")
    st.stop()

def call_real_agent(content, target_agent, lang_code):
    try:
        import openai
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a {target_agent} specialist for Green Hill Canarias cannabis operations."},
                {"role": "user", "content": content}
            ],
            max_tokens=1000
        )
        
        return {"response": response.choices[0].message.content}, f"✅ {target_agent}"
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

st.title("🌿 Green Hill Executive Cockpit")

agents = ["Strategy", "Finance", "Operations", "Market", "Risk", "Compliance", "Innovation"]
selected_agent = st.selectbox("Select Agent:", agents)
user_query = st.text_area("Your query:", height=100)

if st.button("🚀 Execute"):
    if user_query.strip():
        result, status = call_real_agent(user_query, selected_agent, "en")
        if result:
            st.success(status)
            st.write(result["response"])
        else:
            st.error(status)
