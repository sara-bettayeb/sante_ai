import os
import warnings
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

try:
    from database import get_all_diagnostics, save_diagnostic
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

st.set_page_config(
    page_title="المنصة الذكية للتنبؤ بمخاطر السكري",
    page_icon="🩺",
    layout="wide",
)

st.markdown("""
    <style>
    .stApp {
        background-color: #e0f7fa !important;
    }
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    h1, h2, h3, p, label, .stMarkdown, .stText {
        color: #0d47a1 !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #1565c0;
        color: white;
        padding: 12px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0d47a1;
        color: white;
        box-shadow: 0 0 10px #1565c0;
    }
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] li {
        color: #000000 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

BRFSS_FEATURES = [
    "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
    "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
    "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
    "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income",
]


def yes_no_to_int(label: str) -> int:
    return 1 if label.startswith("نعم") else 0


@st.cache_resource
def load_brfss_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(base_dir, "extracted_model", "model.joblib"),
        os.path.join(base_dir, "model.joblib"),
        os.path.join(base_dir, "PIRFECT.joblib"),
        os.path.join(base_dir, "models", "model.joblib"),
        os.path.join(base_dir, "PIRFECT"),
    ]
    for path in candidates:
        if os.path.exists(path) and os.path.isfile(path):
            return joblib.load(path), path
    return None, None


model, loaded_path = load_brfss_model()

st.markdown("<h1 style='text-align: center; color: #0d47a1;'>🩺 المنصة الذكية للتنبؤ بمخاطر السكري</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1565c0; font-size: 18px;'>تقييم وقائي مبني على 21 مؤشراً سلوكياً ونمط الحياة (BRFSS) دون تحاليل مخبرية</p>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 الفحص والتنبؤ الفوري", "📚 دليل مؤشرات نمط الحياة"])

with tab1:
    patient_name = st.text_input("اسم المستفيد (Patient Name)", placeholder="أدخل الاسم لحفظ الفحص في السجل...")
    col_input, col_result = st.columns([1, 1.2], gap="large")

    with col_input:
        st.markdown("### 📋 1. مؤشر كتلة الجسم (BMI) والنشاط والعادات اليومية")
        col_w, col_h = st.columns(2)
        weight = col_w.number_input("الوزن (كجم)", 30.0, 220.0, 72.0)
        height_cm = col_h.number_input("الطول (سم)", 100.0, 230.0, 170.0)
        calculated_bmi = float(weight / ((height_cm / 100.0) ** 2))
        st.info(f"مؤشر BMI المحسوب: {calculated_bmi:.1f}")

        phys_activity = yes_no_to_int(st.selectbox("ممارسة نشاط بدني خلال آخر 30 يوماً (PhysActivity)", ["نعم (1)", "لا (0)"]))
        fruits = yes_no_to_int(st.selectbox("تناول الفاكهة يومياً مرة واحدة على الأقل (Fruits)", ["نعم (1)", "لا (0)"]))
        veggies = yes_no_to_int(st.selectbox("تناول الخضروات يومياً مرة واحدة على الأقل (Veggies)", ["نعم (1)", "لا (0)"]))
        smoker = yes_no_to_int(st.selectbox("التدخين - 100 سيجارة أو أكثر في الحياة (Smoker)", ["لا (0)", "نعم (1)"]))
        hvy_alcohol = yes_no_to_int(st.selectbox("استهلاك مرتفع للكحول (HvyAlcoholConsump)", ["لا (0)", "نعم (1)"]))

        st.markdown("---")
        st.markdown("### 🩺 2. التاريخ الصحي والوضع العام")
        high_bp = yes_no_to_int(st.selectbox("ارتفاع ضغط الدم (HighBP)", ["لا (0)", "نعم (1)"]))
        high_chol = yes_no_to_int(st.selectbox("ارتفاع الكوليسترول (HighChol)", ["لا (0)", "نعم (1)"]))
        chol_check = yes_no_to_int(st.selectbox("فحص الكوليسترول خلال 5 سنوات (CholCheck)", ["نعم (1)", "لا (0)"]))
        stroke = yes_no_to_int(st.selectbox("سجل سكتة دماغية (Stroke)", ["لا (0)", "نعم (1)"]))
        heart_disease = yes_no_to_int(st.selectbox("أمراض القلب أو نوبة قلبية (HeartDiseaseorAttack)", ["لا (0)", "نعم (1)"]))
        diff_walk = yes_no_to_int(st.selectbox("صعوبة شديدة في المشي أو صعود الدرج (DiffWalk)", ["لا (0)", "نعم (1)"]))
        any_healthcare = yes_no_to_int(st.selectbox("توفر تغطية صحية (AnyHealthcare)", ["نعم (1)", "لا (0)"]))
        no_doc_cost = yes_no_to_int(st.selectbox("تعذر زيارة الطبيب بسبب التكلفة خلال سنة (NoDocbcCost)", ["لا (0)", "نعم (1)"]))

        gen_hlth = st.slider("الحالة الصحية العامة (GenHlth: 1 ممتاز - 5 ضعيف جداً)", 1, 5, 2)
        ment_hlth = st.slider("أيام الصحة النفسية غير الجيدة خلال 30 يوماً (MentHlth)", 0, 30, 0)
        phys_hlth = st.slider("أيام الصحة البدنية غير الجيدة خلال 30 يوماً (PhysHlth)", 0, 30, 0)

        st.markdown("---")
        st.markdown("### 👤 3. البيانات الديموغرافية (ترميز BRFSS)")
        sex = 0 if st.selectbox("الجنس (Sex)", ["أنثى (0)", "ذكر (1)"]).startswith("أنثى") else 1
        age_map = {
            "18–24": 1, "25–29": 2, "30–34": 3, "35–39": 4, "40–44": 5,
            "45–49": 6, "50–54": 7, "55–59": 8, "60–64": 9, "65–69": 10,
            "70–74": 11, "75–79": 12, "80+": 13,
        }
        age_label = st.selectbox("الفئة العمرية (Age)", list(age_map.keys()), index=4)
        age_code = age_map[age_label]

        education = st.slider("المستوى التعليمي (Education: 1 أدنى - 6 جامعي/أعلى)", 1, 6, 4)
        income = st.slider("مستوى الدخل (Income: 1 الأقل - 8 الأعلى)", 1, 8, 5)

    with col_result:
        st.markdown("### 🔬 نتيجة التنبؤ والتحليل")
        if model is None:
            st.error("⚠️ لم يتم العثور على ملف النموذج PIRFECT داخل مجلد diabetes.malak!")
        else:
            st.caption(f"النموذج المحمّل: `{os.path.basename(loaded_path)}`")
            if st.button("🔍 إجراء التقييم وحفظ النتيجة"):
                input_dict = {
                    "HighBP": high_bp,
                    "HighChol": high_chol,
                    "CholCheck": chol_check,
                    "BMI": calculated_bmi,
                    "Smoker": smoker,
                    "Stroke": stroke,
                    "HeartDiseaseorAttack": heart_disease,
                    "PhysActivity": phys_activity,
                    "Fruits": fruits,
                    "Veggies": veggies,
                    "HvyAlcoholConsump": hvy_alcohol,
                    "AnyHealthcare": any_healthcare,
                    "NoDocbcCost": no_doc_cost,
                    "GenHlth": gen_hlth,
                    "MentHlth": ment_hlth,
                    "PhysHlth": phys_hlth,
                    "DiffWalk": diff_walk,
                    "Sex": sex,
                    "Age": age_code,
                    "Education": education,
                    "Income": income,
                }

                ordered_cols = list(model.feature_names_in_) if hasattr(model, "feature_names_in_") else BRFSS_FEATURES
                features_df = pd.DataFrame([[input_dict[c] for c in ordered_cols]], columns=ordered_cols)
                prediction = int(model.predict(features_df)[0])

                if hasattr(model, "predict_proba"):
                    probability = float(model.predict_proba(features_df)[0][1] * 100.0)
                else:
                    probability = 75.0 if prediction == 1 else 20.0

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability,
                    number={"suffix": "%", "font": {"size": 36, "color": "#0d47a1"}},
                    title={"text": "مؤشر خطورة السكري المحتملة (وقائي)", "font": {"size": 18, "color": "#0d47a1"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#0d47a1"},
                        "bar": {"color": "#1565c0"},
                        "bgcolor": "#ffffff",
                        "steps": [
                            {"range": [0, 35], "color": "#bbdefb"},
                            {"range": [35, 70], "color": "#64b5f6"},
                            {"range": [70, 100], "color": "#1e88e5"},
                        ],
                    },
                ))
                fig_gauge.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig_gauge, use_container_width=True)

                if prediction == 1:
                    result_label = f"احتمال مرتفع لمخاطر السكري ({probability:.1f}%)"
                    st.error(f"⚠️ النتيجة: {result_label}")
                    st.warning("💡 توصية وقائية: يُنصح بتحسين نمط الحياة والنشاط البدني ومراجعة مختص للفحص الوقائي.")
                else:
                    result_label = f"احتمال منخفض لمخاطر السكري ({probability:.1f}%)"
                    st.success(f"✅ النتيجة: {result_label}")
                    st.info("💡 نصيحة: الاستمرار على العادات الصحية والنشاط البدني المنتظم.")

                if DB_AVAILABLE:
                    inputs_summary = (
                        f"BMI: {calculated_bmi:.1f}, PhysActivity: {phys_activity}, "
                        f"Smoker: {smoker}, GenHlth: {gen_hlth}, AgeCode: {age_code}"
                    )
                    final_patient = patient_name.strip() if patient_name.strip() else "مريض غير مسمى"
                    save_diagnostic(final_patient, "Diabetology (Diabetes)", inputs_summary, result_label)
                    st.toast("✅ تم حفظ التقييم في قاعدة البيانات بنجاح!")

                estimator = model.steps[-1][1] if hasattr(model, "steps") else model
                if hasattr(estimator, "feature_importances_") and len(estimator.feature_importances_) == len(ordered_cols):
                    df_imp = pd.DataFrame({
                        "العامل": ordered_cols,
                        "الأهمية": estimator.feature_importances_,
                    }).sort_values("الأهمية", ascending=True).tail(10)
                    fig_imp = px.bar(
                        df_imp, x="الأهمية", y="العامل", orientation="h",
                        color="الأهمية", color_continuous_scale=["#bbdefb", "#1565c0"],
                    )
                    fig_imp.update_layout(height=280, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
                    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🗂️ سجل فحوصات السكري المحفوظة (Diabetes)")
    if DB_AVAILABLE:
        try:
            records = get_all_diagnostics("Diabetology (Diabetes)")
            if records:
                st.dataframe(pd.DataFrame(records), use_container_width=True)
            else:
                st.info("لا توجد فحوصات محفوظة بعد.")
        except Exception as e:
            st.warning(f"تعذر تحميل السجل: {e}")
    else:
        st.info("سيتم تفعيل سجل قاعدة البيانات تلقائياً عند ربط ملف database.py بنفس الأسماء.")

with tab2:
    st.header("📚 دليل مؤشرات نمط الحياة والوقاية")
    st.markdown("""
- **النشاط البدني والتغذية:** الحركة المنتظمة وتناول الخضروات والفاكهة من أهم العوامل الوقائية في بيانات BRFSS.
- **مؤشر كتلة الجسم (BMI):** يُحسب تلقائياً من الوزن والطول دون الحاجة لأي تحاليل مخبرية.
- **تنبيه أكاديمي ووقائي:** يعتمد هذا النموذج على مؤشرات سلوكية وإحصائية للفحص الأولي وليس للتشخيص الطبي السريري.
    """)