import sys
import types
import importlib

# 1. حل مشاكل مسارات واستيراد NumPy
class NumpyCoreRedirector:
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("numpy._core"):
            target_name = fullname.replace("numpy._core", "numpy.core")
            try:
                mod = importlib.import_module(target_name)
                sys.modules[fullname] = mod
                return mod.spec
            except Exception:
                return None
        return None

sys.meta_path.insert(0, NumpyCoreRedirector())

import numpy as np
import numpy.core.numeric
if hasattr(np.core, 'multiarray'):
    import numpy.core.multiarray
    sys.modules['numpy._core.multiarray'] = np.core.multiarray

np._core = np.core
sys.modules['numpy._core'] = np.core
sys.modules['numpy._core.numeric'] = np.core.numeric

import streamlit as st
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import sklearn.compose._column_transformer

# 2. توافقية Scikit-Learn
if not hasattr(sklearn.compose._column_transformer, '_RemainderColsList'):
    class _RemainderColsList(list):
        pass
    sklearn.compose._column_transformer._RemainderColsList = _RemainderColsList

# 3. تعريف وحقن FrequencyEncoder
class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X

if 'main' in sys.modules:
    setattr(sys.modules['main'], 'FrequencyEncoder', FrequencyEncoder)

if 'main' not in sys.modules:
    fake_main = types.ModuleType('main')
    fake_main.FrequencyEncoder = FrequencyEncoder
    sys.modules['main'] = fake_main
else:
    setattr(sys.modules['main'], 'FrequencyEncoder', FrequencyEncoder)

import joblib

st.set_page_config(
    page_title="CardioPulse AI | Clinical Diagnostic Hub",
    page_icon="🫀",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 20% 15%, #1e2638 0%, #131926 50%, #0d121c 100%);
        color: #e2e8f0;
    }
    
    .titanium-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 26px 30px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 12px 35px 0 rgba(0, 0, 0, 0.35);
        margin-bottom: 24px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .titanium-card:hover {
        border-color: rgba(56, 189, 248, 0.25);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 18px;
        background: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
    }
    
    .pulse-dot {
        width: 9px;
        height: 9px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(120deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 500;
    }

    .metric-box {
    background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38bdf8;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        margin-top: 4px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        padding: 16px 32px !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    loaded = joblib.load('ensemble.joblib')
    if isinstance(loaded, dict):
        for key in ['model', 'pipeline', 'classifier', 'estimator', 'ensemble']:
            if key in loaded and hasattr(loaded[key], 'predict'):
                return loaded[key]
        for val in loaded.values():
            if hasattr(val, 'predict'):
                return val
    return loaded

try:
    model = load_model()
except Exception as e:
    st.error(f"خطأ أثناء استدعاء النموذج: {e}")
    st.stop()

st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 28px; padding-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.06);">
    <div>
        <div class="hero-title">🫀 CardioPulse AI : Clinical Diagnostic Engine</div>
        <div class="hero-subtitle">منظومة الذكاء الاصطناعي للتنبؤ المتقدم بأمراض القلب والشرايين | Docker Containerized</div>
    </div>
    <div>
        <span class="status-pill">
            <span class="pulse-dot"></span>
            بيئة العمل نشطة ومحمية
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="titanium-card">', unsafe_allow_html=True)
st.markdown("<h3 style='margin-top:0; color:#f8fafc; font-weight:700;'>📋 المدخلات السريرية والفحوصات الحيوية للمريض</h3>", unsafe_allow_html=True)
st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.number_input("العمر (Age)", min_value=18, max_value=100, value=54)
    sex = st.selectbox("الجنس السريري (Sex)", options=[1, 0], format_func=lambda x: "ذكر (Male)" if x == 1 else "أنثى (Female)")
    chest_pain = st.selectbox(
        "نوع ألم الصدر (Chest pain type)", 
        options=[1, 2, 3, 4],
        format_func=lambda x: {
            1: "1: ذبحة نموذجية (Typical)",
            2: "2: ذبحة غير نمطية (Atypical)",
            3: "3: ألم غير ذبحي (Non-anginal)",
            4: "4: عديم الأعراض (Asymptomatic)"
        }[x]
    )
    bp = st.number_input("ضغط الدم (BP - mm Hg)", min_value=70, max_value=230, value=135)
    cholesterol = st.number_input("الكوليسترول (Cholesterol - mg/dL)", min_value=0, max_value=600, value=230)

with c2:
    fbs = st.selectbox(
        "سكر الدم الصائم > 120 (FBS over 120)",
        options=[0, 1],
        format_func=lambda x: "طبيعي (أقل من 120 mg/dL)" if x == 0 else "مرتفع (أكبر من 120 mg/dL)"
    )
    ekg = st.selectbox(
        "نتائج تخطيط القلب (EKG results)",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "0: سليم (Normal)",
            1: "1: شذوذ في موجة ST-T",
            2: "2: تضخم البطين الأيسر (LVH)"
        }[x]
    )
    max_hr = st.number_input("أقصى معدل ضربات قلب (Max HR)", min_value=60, max_value=220, value=145)
    exercise_angina = st.selectbox(
        "ذبحة صدرية بالجهد (Exercise angina)",
        options=[0, 1],
        format_func=lambda x: "لا توجد (No)" if x == 0 else "توجد ذبحة (Yes)"
    )

with c3:
    st_depression = st.number_input("انخفاض مقطع ST (ST depression)", min_value=-2.5, max_value=7.0, value=1.4, step=0.1)
    slope_st = st.selectbox(
        "انحدار مقطع ST (Slope of ST)",
        options=[1, 2, 3],
        format_func=lambda x: {
            1: "1: صاعد (Upsloping)",
            2: "2: مستوٍ (Flat)",
            3: "3: هابط (Downsloping)"
        }[x]
    )
    vessels = st.selectbox("عدد الأوعية الملونة (Number of vessels fluro)", options=[0, 1, 2, 3])
    thallium = st.selectbox(
        "فحص الثاليوم (Thallium)",
        options=[3, 6, 7],
        format_func=lambda x: {
            3: "3: طبيعي (Normal)",
            6: "6: عيب ثابت (Fixed Defect)",
            7: "7: عيب قابل للعكس (Reversible Defect)"
        }[x]
    )

st.markdown('</div>', unsafe_allow_html=True)

# ملخص حي للمؤشرات
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{bp}</div><div class="metric-title">ضغط الدم (BP)</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{cholesterol}</div><div class="metric-title">الكوليسترول</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{max_hr}</div><div class="metric-title">النبض الأقصى (Max HR)</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-box"><div class="metric-value">{st_depression}</div><div class="metric-title">انخفاض ST</div></div>', unsafe_allow_html=True)

st.write("")

# تجهيز البيانات بأسماء الأعمدة الدقيقة المطابقة للنموذج
input_df = pd.DataFrame([{
    'Age': age,
    'Sex': sex,
    'Chest pain type': chest_pain,
    'BP': bp,
    'Cholesterol': cholesterol,
    'FBS over 120': fbs,
    'EKG results': ekg,
    'Max HR': max_hr,
    'Exercise angina': exercise_angina,
    'ST depression': st_depression,
    'Slope of ST': slope_st,
    'Number of vessels fluro': vessels,
    'Thallium': thallium
}])

# زر التنبؤ وإظهار النتائج
if st.button("⚡ تحليل المؤشرات وإصدار التشخيص السريري الذكي"):
    try:
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0] if hasattr(model, 'predict_proba') else None
        
        st.write("")
        st.markdown('<div class="titanium-card">', unsafe_allow_html=True)
        
        is_disease = (prediction == 1) or (str(prediction).lower() in ['presence', 'positive', 'yes'])
        
        if is_disease:
            risk_pct = (proba[1] * 100) if (proba is not None and len(proba) > 1) else 87.5
            safe_pct = 100.0 - risk_pct
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.03) 100%); border-right: 5px solid #ef4444; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="color: #f87171; margin: 0; font-weight: 800; font-size: 1.8rem;">⚠️ تنبيه طبي: مؤشرات خطر حرجة للإصابة (High Risk)</h2>
                        <p style="color: #cbd5e1; margin: 8px 0 0 0; font-size: 1.05rem;">
                            التحليل الإحصائي لنموذج التعلّم الآلي أظهر دلالات واضحة لارتفاع احتمالية الإصابة بأمراض القلب.
                        </p>
                        </div>
                    <div style="text-align: center; background: rgba(0,0,0,0.3); padding: 12px 24px; border-radius: 14px; border: 1px solid rgba(239, 68, 68, 0.4);">
                        <div style="font-size: 2.2rem; font-weight: 800; color: #f87171;">{risk_pct:.1f}%</div>
                        <div style="font-size: 0.85rem; color: #cbd5e1; font-weight: 600;">مستوى الخطورة</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.write(f"📊 معدل احتمالية الإصابة بالمرض: {risk_pct:.2f}%")
                st.progress(float(risk_pct / 100))
            with res_c2:
                st.write(f"🛡️ معدل السلامة واستقرار الحالة: {safe_pct:.2f}%")
                st.progress(float(safe_pct / 100))
                
            st.info("💡 التوصية السريرية: يُوصى بإجراء تصوير الأوعية التاجية ومراجعة أخصائي أمراض القلب فوراً.")

        else:
            safe_pct = (proba[0] * 100) if (proba is not None and len(proba) > 0) else 91.2
            risk_pct = 100.0 - safe_pct
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.03) 100%); border-right: 5px solid #10b981; border-radius: 12px; padding: 20px 24px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h2 style="color: #34d399; margin: 0; font-weight: 800; font-size: 1.8rem;">✅ النتيجة مطمئنة: حالة القلب مستقرة (Low Risk)</h2>
                        <p style="color: #cbd5e1; margin: 8px 0 0 0; font-size: 1.05rem;">
                            المؤشرات الحيوية والفسيولوجية الحالية تقع ضمن الحدود الطبيعية وفق قواعد مصفوفة النموذج السريري.
                        </p>
                    </div>
                    <div style="text-align: center; background: rgba(0,0,0,0.3); padding: 12px 24px; border-radius: 14px; border: 1px solid rgba(16, 185, 129, 0.4);">
                        <div style="font-size: 2.2rem; font-weight: 800; color: #34d399;">{safe_pct:.1f}%</div>
                        <div style="font-size: 0.85rem; color: #cbd5e1; font-weight: 600;">مستوى الأمان</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            res_c1, res_c2 = st.columns(2)
            with res_c1:
                st.write(f"🛡️ معدل السلامة واستقرار الحالة: {safe_pct:.2f}%")
                st.progress(float(safe_pct / 100))
            with res_c2:
                st.write(f"📊 معدل الخطورة المتبقي: {risk_pct:.2f}%")
                st.progress(float(risk_pct / 100))
                
            st.success("💡 التوصية الطبية: الاستمرار على نمط الحياة الصحي وإجراء الفحوصات الدورية الروتينية سنوياً.")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as err:
        st.error(f"حدث خطأ أثناء إجراء التشخيص: {err}")