import streamlit as st
import uuid
from utils import call_backend

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="StockSense-Agent", layout="wide")

st.title("📊 StockSense Agent")

# --------------------------
# SESSION STATE
# --------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------
# INPUT BOX
# --------------------------
query = st.text_input("Ask about impact that on real time news on companies or market : just type the company name")

if st.button("Analyze"):

    if not query:
        st.warning("Please enter a query")
    else:
        with st.spinner("Analyzing..."):
            response = call_backend(query, st.session_state.user_id)

            st.session_state.chat_history.append({
                "query": query,
                "response": response
            })
            
# --------------------------
# RESULT FORMATTER
# --------------------------
def display_result(res):

    st.markdown(f"### 🏢 {res.get('company', 'Unknown')}")

    st.markdown("#### 📰 Key News")
    for news in res.get("event_summary", []):
        st.write(f"- {news}")

    st.markdown("#### 🧠 Analysis")
    st.write(f"**Event Type:** {res.get('event_type')}")
    st.write(f"**Impact:** {res.get('impact_direction')}")

    st.markdown("#### 🔗 Reasoning")
    for step in res.get("reasoning_chain", []):
        st.write(f"- {step}")

    st.markdown("#### ⚠️ Risks")
    for risk in res.get("risks", []):
        st.write(f"- {risk}")

    st.markdown(f"#### 📊 Confidence: {res.get('confidence')}")

    # ✅ ADD HERE
    st.markdown("#### 📌 Conclusion")
    st.write(res.get("conclusion", "Not available"))

    st.markdown("#### ⚠️ Disclaimer")
    st.warning(res.get(
        "disclaimer",
        "This is an AI-generated analysis and may not be accurate."
    ))


# --------------------------
# DISPLAY RESULTS
# --------------------------
for chat in reversed(st.session_state.chat_history):

    st.markdown("---")
    st.subheader(f"🧑 Query: {chat['query']}")

    res = chat["response"]

    if "error" in res:
        st.error(res["error"])
        continue
    
    # ✅ NEW FIX
    if isinstance(res, dict) and "message" in res:
        st.warning(res["message"])
        continue

    # Handle multiple companies
    if isinstance(res, list):
        for r in res:
            display_result(r)
    else:
        display_result(res)
    
