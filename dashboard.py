import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px

# إعداد الصفحة وتنسيق الاتجاه من اليمين لليسار (RTL)
st.set_page_config(
    page_title="المنصة الذكية للتنبؤ بمخاطر السكري",
    page_icon="🩺",
    layout="wide"
)

# حقن كود CSS لتنظيم العرض والخطوط والاتجاهات بشكل احترافي
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
        justify-content: center;
    }
    h1, h2, h3, p, label, .stMarkdown {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        background-color: #2e7d32;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# تحميل النموذج
@st.cache_resource
def load_model():
    model_path = "models/diabetes_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

# رأس الصفحة الاحترافي
st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🩺 المنصة الذكية للتقييم المبكر لمخاطر مرض السكري</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 18px;'>تطبيق طبي ذكي يعتمد على خوارزميات تعلم الآلة لتحليل المؤشرات الحيوية بدقة علمية.</p>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 الفحص والتنبؤ الفوري", "📚 معلومات وإرشادات علمية"])

# ==================== التبويب الأول ====================
with tab1:
    col_input, col_result = st.columns([1, 1.2], gap="large")

    with col_input:
        st.markdown("### 📋 البيانات الفسيولوجية والسريرية")

        with st.container():
            st.markdown("**1. حاسبة مؤشر كتلة الجسم (BMI):**")
            col_w, col_h = st.columns(2)
            weight = col_w.number_input("الوزن (كجم)", 30.0, 200.0, 70.0)
            height_cm = col_h.number_input("الطول (سم)", 100.0, 220.0, 170.0)
            
            calculated_bmi = weight / ((height_cm / 100) ** 2)
            
            if calculated_bmi < 18.5:
                bmi_status = "وزن منخفض 🟡"
            elif 18.5 <= calculated_bmi < 25:
                bmi_status = "وزن مثالي 🟢"
            elif 25 <= calculated_bmi < 30:
                bmi_status = "وزن زائد 🟡"
            else:
                bmi_status = "سمنة 🔴"
            
            st.success(f"مؤشر الـ BMI المحسوب: **{calculated_bmi:.1f}** ({bmi_status})")

        st.markdown("---")
        st.markdown("**2. المؤشرات الحيوية والمخْبَرية:**")
        glucose = st.slider("مستوى الجلوكوز الصائم (Fasting Glucose mg/dL)", 50, 250, 110)
        bp = st.slider("ضغط الدم الانقبائي (Blood Pressure mm Hg)", 40, 140, 72)
        insulin = st.slider("مستوى الأنسولين (Insulin mu U/ml)", 0, 840, 80)
        skin_thickness = st.slider("سمك ثنية الجلد (Skin Thickness mm)", 0, 99, 20)
        dpf = st.slider("مؤشر التاريخ الوراثي (Diabetes Pedigree)", 0.08, 2.42, 0.47, step=0.01)
        age = st.number_input("العمر (بالسنوات)", 1, 120, 33)
        pregnancies = st.number_input("عدد الحمول (Pregnancies)", 0, 20, 1)

    with col_result:
        st.markdown("### 🎯 نتيجة التنبؤ والتحليل الذكي")

        if model is None:
            st.error("⚠️ لم يتم العثور على النموذج! يرجى التأكد من تشغيل ملف `train.py`.")
        else:
            if st.button("إجراء الفحص الطبي الذكي 🔍"):
                features = np.array([[pregnancies, glucose, bp, skin_thickness, insulin, calculated_bmi, dpf, age]])
                prediction = model.predict(features)[0]
                probability = model.predict_proba(features)[0][1] * 100

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability,
                    number={'suffix': "%", 'font': {'size': 26}},
                    title={'text': "نسبة خطورة الإصابة المحتملة", 'font': {'size': 16}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1},
                        'bar': {'color': "#1b5e20"},
                        'steps': [
                            {'range': [0, 35], 'color': "#c8e6c9"},
                            {'range': [35, 70], 'color': "#ffe0b2"},
                            {'range': [70, 100], 'color': "#ffcdd2"}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=260, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig_gauge, use_container_width=True)

                if prediction == 1:
                    status_text = "احتمال مرتفع للإصابة بمرض السكري"
                    st.error(f"⚠️ **النتيجة:** {status_text} ({probability:.1f}%)")
                    st.warning("""
                    **💡 التوصيات الطبية الوقائية:**
                    * مراجعة الطبيب المختص لإجراء فحص السكر التراكمي (HbA1c).
                    * الالتزام بنسق غذائي صحي وتقليل السكريات.
                    * ممارسة النشاط البدني بانتظام.
                    """)
                else:
                    status_text = "احتمال منخفض للإصابة (حالة مستقرة)"
                    st.success(f"✅ **النتيجة:** {status_text} ({probability:.1f}%)")
                    st.info("""
                    **💡 نصائح للحفاظ على الصحة:**
                    * الاستمرار في اتباع نمط حياة صحي ومتوازن.
                    * إجراء الفحوصات الدورية للاطمئنان المستمر.
                    """)

                st.markdown("---")
                st.markdown("#### 🔍 تحليل تأثير العوامل السريرية على النتيجة:")
                feature_names = ['الحمل', 'الجلوكوز', 'ضغط الدم', 'سمك الجلد', 'الأنسولين', 'BMI', 'الوراثة', 'العمر']
                importances = model.feature_importances_
                df_imp = pd.DataFrame({'العامل': feature_names, 'الأهمية': importances}).sort_values('الأهمية', ascending=True)
                
                fig_imp = px.bar(df_imp, x='الأهمية', y='العامل', orientation='h', color='الأهمية',
                                 color_continuous_scale='Greens')
                fig_imp.update_layout(height=240, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
                st.plotly_chart(fig_imp, use_container_width=True)

# ==================== التبويب الثاني ====================
with tab2:
    st.header("📚 دليل توعوي حول المؤشرات الطبية")
    st.markdown("""
    * **مستوى الجلوكوز الصائم:** يعتبر المعيار الأساسي لتشخيص حالة السكر في الدم.
    * **مؤشر كتلة الجسم (BMI):** يقيس التناسب بين الوزن والطول، والزيادة المفرطة تسبب مقاومة الإنسولين.
    * **مؤشر التاريخ الوراثي:** يقيس احتمالية انتقال المرض وراثياً بناءً على السجل العائلي.
    * **مستوى الأنسولين:** يوضح كفاءة البنكرياس في إفراز الهرمون المسؤول عن تنظيم السكر.
    """)