import streamlit as st
import pandas as pd
import os
import sys

# ربط مجلد المشروع الرئيسي لاستيراد database.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import save_diagnostic, get_all_diagnostics

# --- Page configuration
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
        background-color: #1e293b; padding: 20px; border-radius: 12px; color: #f8fafc;
        border-left: 5px solid #38bdf8; border: 1px solid #334155; height: 100%;
    }
    .medical-card-hyper {
        background-color: #1e293b; padding: 20px; border-radius: 12px; color: #f8fafc;
        border-left: 5px solid #f43f5e; border: 1px solid #334155; height: 100%;
    }
    h2, h3 { color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

# --- Load Dataset ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "archive", "Thyroid_Diff.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

df = load_data()

# --- Section 1: Header ---
st.markdown("""
    <div class="main-title-box">
        <h1>🦋 Thyroid Care Portal</h1>
        <p style="color: #94a3b8; margin-top: 8px; font-size: 1.05rem;">Clinical Overview & Intelligent Medical Assistant</p>
    </div>
""", unsafe_allow_html=True)

# --- Section 2: Educational Information ---
st.header("Overview: What is the Thyroid Gland?")
st.write("""
The thyroid is a small, butterfly-shaped endocrine gland located at the base of the neck. 
It regulates vital body functions—including heart rate, energy metabolism, and body temperature—by producing 
and releasing Triiodothyronine (T3) and Thyroxine (T4) under the regulation of TSH.
""")

# Display image if exists
img_path = os.path.join(os.path.dirname(__file__), "thyroid.png")
if os.path.exists(img_path):
    st.image(img_path, caption="Thyroid Gland Anatomy & Structure", use_container_width=True)

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
st.caption("Ask any question regarding thyroid symptoms, lab results, or general care.")

patient_name = st.text_input("اسم المريض (Patient Name)", placeholder="أدخل اسم المريض لحفظ الاستشارة في السجل...")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Thyroid Care Assistant. How can I help you today?"}
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
                reply = "Hello! I am your Thyroid Care Assistant. How can I help you today?"
            elif any(w in p for w in ["what is", "define", "meaning", "thyroid gland"]):
                reply = "The thyroid is a small, butterfly-shaped endocrine gland at the base of the neck that regulates metabolism, heart rate, and energy through T3 and T4 hormones."
            elif any(w in p for w in ["hypo", "skin", "hair", "haire", "gain", "tired", "fatigue", "cold", "underactive", "weight"]):
                reply = "Hypothyroidism occurs when the thyroid is underactive and does not produce enough hormones. Common symptoms include fatigue, weight gain, sensitivity to cold, dry skin, and hair thinning."
            elif any(w in p for w in ["hyper", "loss", "heart", "sweat", "anxiety", "overactive", "palpitation", "tremor"]):
                reply = "Hyperthyroidism happens when the thyroid is overactive, producing excessive hormones. Key symptoms include unexplained weight loss, rapid heartbeat, sweating, tremors, and anxiety."
            elif any(w in p for w in ["pain", "hurt", "hert", "ache", "sore", "neck", "swelling", "throat", "nodule"]):
                reply = "Neck discomfort or pain can sometimes be linked to thyroid inflammation (thyroiditis) or nodules. It is important to consult a healthcare professional for a physical exam and ultrasound."
            elif any(w in p for w in ["tsh", "t3", "t4", "hormone", "lab", "test", "blood", "result"]):
                reply = "Thyroid lab tests measure TSH, T3, and T4 levels. High TSH usually points toward hypothyroidism, while low TSH often suggests hyperthyroidism. Please share your specific values with your doctor."
            elif any(w in p for w in ["dataset", "data", "kaggle", "records", "database"]):
                count = len(df) if df is not None else 0
                reply = f"Yes! Our system is directly integrated with the Kaggle Thyroid Dataset ({count} clinical patient records loaded) to support clinical insights."
            else:
                reply = f"I understand you're asking about '{prompt}'. Managing thyroid health relies on monitoring symptoms, regular TSH/T3/T4 blood tests, and consulting an endocrinologist."
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            # حفظ الاستشارة في قاعدة البيانات الموحدة
            save_diagnostic(patient_name, "Endocrinology (Thyroid)", f"Query: {prompt[:80]}", reply[:120])

# --- Section 4: Database Records ---
st.markdown("---")
st.subheader("📋 سجل استشارات الغدة الدرقية المحفوظة (Thyroid)")
records = get_all_diagnostics("Endocrinology (Thyroid)")
if records:
    st.dataframe(pd.DataFrame(records), use_container_width=True)
else:
    st.info("لا توجد استشارات محفوظة بعد. اطرح سؤالاً على المساعد الذكي ليظهر هنا!")