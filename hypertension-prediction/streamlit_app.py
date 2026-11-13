import os
import sys
import joblib
import pandas as pd
import streamlit as st

# ربط المسار بقاعدة البيانات الرئيسية في الجذر
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from database import save_diagnostic, get_all_diagnostics
from model.features import FEATURE_COLUMNS

st.set_page_config(
    page_title="Hypertension AI | التنبؤ بضغط الدم",
    page_icon="🩺",
    layout="wide"
)

@st.cache_resource
def load_hypertension_model():
    model_path = os.path.join(BASE_DIR, "model", "model.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"الموديل غير موجود في المسار: {model_path}")
    bundle = joblib.load(model_path)
    return bundle["pipeline"] if isinstance(bundle, dict) and "pipeline" in bundle else bundle

try:
    pipeline = load_hypertension_model()
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل نموذج ضغط الدم: {e}")
    st.stop()

st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🩺 نظام التنبؤ بمخاطر ارتفاع ضغط الدم (Hypertension)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>أداة ذكاء اصطناعي تعليمية لتقييم عوامل خطر ضغط الدم وحفظ السجلات الطبية</p>", unsafe_allow_html=True)
st.markdown("---")

patient_name = st.text_input("👤 اسم المريض (Patient Name)", placeholder="أدخل الاسم الكامل للمريض...")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.number_input("العمر (Age)", min_value=18, max_value=100, value=45)
    gender = st.selectbox("الجنس (Gender)", options=[0, 1], format_func=lambda x: "أنثى (Female)" if x == 0 else "ذكر (Male)")
    bmi = st.number_input("مؤشر كتلة الجسم (BMI)", min_value=14.0, max_value=55.0, value=25.5, step=0.1)
    family_history = st.selectbox("تاريخ عائلي مع الضغط (Family History)", options=[0, 1], format_func=lambda x: "لا (No)" if x == 0 else "نعم (Yes)")

with c2:
    systolic = st.number_input("الضغط الانقباضي (Systolic - mmHg)", min_value=80, max_value=240, value=125)
    diastolic = st.number_input("الضغط الانبساطي (Diastolic - mmHg)", min_value=50, max_value=150, value=82)
    heart_rate = st.number_input("معدل ضربات القلب (Heart Rate - bpm)", min_value=45, max_value=180, value=75)
    salt = st.number_input("استهلاك الملح اليومي (Salt - g/day)", min_value=0.5, max_value=20.0, value=5.0, step=0.5)

with c3:
    smoking = st.selectbox("التدخين (Smoking)", options=[0, 1], format_func=lambda x: "غير مدخن (No)" if x == 0 else "مدخن (Yes)")
    physical_activity = st.selectbox("النشاط البدني (Physical Activity)", options=[0, 1], format_func=lambda x: "خامل (Sedentary)" if x == 0 else "نشيط (Active)")
    stress = st.selectbox("مستوى التوتر (Stress)", options=[0, 1], format_func=lambda x: "منخفض (Low)" if x == 0 else "مرتفع (High)")
    sleep = st.number_input("ساعات النوم (Sleep - hours/night)", min_value=2.0, max_value=14.0, value=7.0, step=0.5)
    diabetes = st.selectbox("إصابة بالسكري (Diabetes)", options=[0, 1], format_func=lambda x: "لا (No)" if x == 0 else "نعم (Yes)")
    thyroid = st.selectbox("اضطراب الغدة الدرقية (Thyroid)", options=[0, 1], format_func=lambda x: "لا (No)" if x == 0 else "نعم (Yes)")

st.write("")

if st.button("⚡ إجراء الفحص الطبي وحفظ النتيجة", use_container_width=True):
    final_patient = patient_name.strip() if patient_name.strip() else "مريض غير مسمى"
    
    input_data = {
        "age": age,
        "gender": gender,
        "bmi": bmi,
        "systolic": systolic,
        "diastolic": diastolic,
        "heartRate": heart_rate,
        "familyHistory": family_history,
        "smoking": smoking,
        "physicalActivity": physical_activity,
        "salt": salt,
        "stress": stress,
        "sleep": sleep,
        "diabetes": diabetes,
        "thyroid": thyroid,
    }
    
    # ترتيب الأعمدة بدقة حسب FEATURE_COLUMNS
    row = pd.DataFrame([[input_data[col] for col in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
    
    try:
        prob = float(pipeline.predict_proba(row)[0, 1])
        pred = int(prob >= 0.5)
        risk_pct = round(prob * 100, 1)
        
        if pred == 1:
            result_label = f"إيجابي (خطر ارتفاع ضغط الدم - {risk_pct}%)"
            st.error(f"⚠️ النتيجة: {result_label}")
        else:
            result_label = f"سلبي (مستوى ضغط مستقر - {risk_pct}%)"
            st.success(f"✅ النتيجة: {result_label}")
            
        inputs_summary = f"Age:{age}, Sys/Dia:{systolic}/{diastolic}, HR:{heart_rate}, BMI:{bmi}"
        save_diagnostic(final_patient, "Cardiology (Hypertension)", inputs_summary, result_label)
        st.toast("تم حفظ نتيجة الفحص في قاعدة البيانات بنجاح!")
    except Exception as err:
        st.error(f"حدث خطأ أثناء الحساب أو الحفظ: {err}")

st.markdown("---")
st.subheader("📂 سجل فحوصات ضغط الدم المحفوظة (Hypertension)")
try:
    records = get_all_diagnostics("Cardiology (Hypertension)")
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
    else:
        st.info("لا توجد فحوصات محفوظة بعد. قم بإجراء أول فحص ليظهر هنا!")
except Exception as e:
    st.warning(f"تعذر تحميل السجل: {e}")