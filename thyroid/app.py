import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(page_title="Thyroid Care Portal", page_icon="🦋", layout="centered")

# --- Professional Medical Dashboard & Chat CSS ---
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .main-title-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 25px;
    }
    .main-title-box h1 { color: #38bdf8 !important; font-weight: 700; font-size: 2.2rem; margin: 0; }
    
    /* تلوين رسائل المستخدم عبر استهداف الأيقونة المخصصة للمستخدم */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background-color: #1e293b !important;
        border-radius: 12px;
        border: 1px solid #334155;
    }

    .medical-card-hypo {
        background-color: #1e293b; padding: 20px; border-radius: 12px; color: #f1f5f9;
        border-left: 5px solid #38bdf8; border: 1px solid #334155; height: 100%;
    }
    .medical-card-hyper {
        background-color: #1e293b; padding: 20px; border-radius: 12px; color: #f1f5f9;
        border-left: 5px solid #f43f5e; border: 1px solid #334155; height: 100%;
    }
    h2, h3 { color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

# --- Load Dataset ---
@st.cache_data
def load_data():
    file_path = os.path.join("archive", "Thyroid_Diff.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

df = load_data()

# --- Section 1: Header ---
st.markdown("""
    <div class="main-title-box">
        <h1>✚ Thyroid Care Portal</h1>
        <p style="color: #94a3b8; margin-top: 8px; font-size: 1.05rem;">Clinical Education & AI Assistant Module</p>
    </div>
""", unsafe_allow_html=True)

# --- Section 2: Educational Information ---
st.header("Overview: What is the Thyroid Gland?")
st.write("""
The thyroid is a small, butterfly-shaped endocrine gland located at the base of the front of the neck. 
It regulates vital body functions—including heart rate, energy metabolism, and internal temperature—by synthesizing 
and releasing Triiodothyronine (T3) and Thyroxine (T4) under the regulation of Thyroid-Stimulating Hormone (TSH).
""")

# Display image if exists
if os.path.exists("thyroid.png"):
    st.image("thyroid.png", caption="Thyroid Gland Anatomy & Structure", use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Hypothyroidism")
    st.markdown("""
        <div class="medical-card-hypo">
            <strong>Clinical Indicators (Underactive):</strong><br><br>
            • Persistent fatigue & lethargy<br>
            • Unexplained weight gain<br>
            • Cold intolerance<br>
            • Dry skin & hair texture changes
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("📈 Hyperthyroidism")
    st.markdown("""
        <div class="medical-card-hyper">
            <strong>Clinical Indicators (Overactive):</strong><br><br>
            • Tachycardia / palpitations<br>
            • Rapid, unexplained weight loss<br>
            • Anxiety, tremors & sweating<br>
            • Sleep disturbances / insomnia
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# --- Section 3: Interactive AI Chatbot Assistant ---
st.header("🤖 Thyroid AI Assistant")
st.caption("Ask any question regarding thyroid symptoms, lab results, or general medical guidance.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Thyroid Care AI Assistant. How can I help you understand thyroid health today?"}
    ]
    # Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type your question about the thyroid here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate smart AI response with comprehensive keyword matching
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            p = prompt.lower()
            
            if any(w in p for w in ["hi", "hello", "hey", "good morning", "good evening"]):
                reply = "Hello! I am your Thyroid Care Assistant. How can I help you understand thyroid health, symptoms, or lab results today?"
            elif any(w in p for w in ["what is", "define", "meaning", "thyroid gland", "thyroid"]):
                reply = "The thyroid is a small, butterfly-shaped endocrine gland located at the base of the front of the neck. It produces hormones (T3 and T4) controlled by TSH to regulate your metabolism, energy, and heart rate."
            elif any(w in p for w in ["hypo", "skin", "hair", "haire", "gain", "fatigue", "cold", "sluggish", "tired", "dry"]):
                reply = "Hypothyroidism occurs when the thyroid is underactive and doesn't produce enough hormones. Common clinical indicators include persistent fatigue, unexplained weight gain, dry skin, changes in hair texture, and increased sensitivity to cold."
            elif any(w in p for w in ["hyper", "loss", "heart", "sweat", "anxiety", "sleep", "fast", "palpitation"]):
                reply = "Hyperthyroidism happens when the thyroid is overactive, accelerating your metabolism. Common symptoms include rapid or irregular heartbeat (tachycardia), sudden weight loss, anxiety, tremors, sweating, and difficulty sleeping."
            elif any(w in p for w in ["pain", "hurt", "hert", "ache", "sore", "neck"]):
                reply = "Neck discomfort or pain can sometimes be linked to thyroid conditions (such as thyroiditis or nodules), but it can also relate to muscles or lymph nodes. If you have persistent pain, it's best to consult an endocrinologist."
            elif any(w in p for w in ["tsh", "t3", "t4", "hormone", "lab", "test", "blood"]):
                reply = "Thyroid lab tests measure TSH, T3, and T4 levels. High TSH often indicates an underactive thyroid (hypothyroidism), while low TSH suggests an overactive thyroid (hyperthyroidism)."
            elif any(w in p for w in ["dataset", "data", "kaggle", "records", "database"]):
                count = len(df) if df is not None else 0
                reply = f"Yes! Our system is directly integrated with the Kaggle thyroid research repository containing {count} verified clinical records for analysis."
            else:
                reply = f"I understand you're asking about '{prompt}'. Managing thyroid health involves monitoring hormone levels (TSH, T3, T4), watching for symptoms like skin/hair changes or weight fluctuations, and consulting an endocrinologist for a precise diagnosis!"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
