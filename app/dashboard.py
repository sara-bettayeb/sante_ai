import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from skops.io import load
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# إعداد الصفحة
st.set_page_config(
    page_title="المنصة الذكية للتنبؤ بمخاطر السكري",
    page_icon="🩺",
    layout="wide"
)

# تنسيق CSS (خلفية زرقاء فاتحة + كلمات زرقاء غامقة)
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
    .stTabs [data-baseweb="tab-list"] {
        direction: rtl;
        justify-content: center;
        gap: 20px;
        border-bottom: 2px solid #0d47a1;
    }
    .stTabs [data-baseweb="tab"] {
        color: #0d47a1 !important;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        border-bottom: 3px solid #0d47a1 !important;
        color: #0d47a1 !important;
    }

    /* هاد الجزء هو اللي راح يصلح مشكل الخانات الصفراء والخضراء */
    div[data-testid="stAlert"] {
        border-radius: 8px;
    }
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] li {
        color: #000000 !important; /* نص أسود باش يبان على الخلفية الصفراء والخضراء */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model_path = "models/model.skops"
    if os.path.exists(model_path):
        loaded_data = load(model_path, trusted=['numpy.dtype'])
        return loaded_data['pipeline']
    return None

model = load_model()

st.markdown("<h1 style='text-align: center; color: #0d47a1;'>🩺 المنصة الذكية للتقييم المبكر لمخاطر السكري</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1565c0; font-size: 18px;'>تطبيق طبي ذكي يعتمد على خوارزميات تعلم الآلة لتحليل المؤشرات الحيوية بدقة علمية.</p>", unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 الفحص والتنبؤ الفوري", "📚 دليل توعوي مبسط"])

# ==================== التبويب الأول ====================
with tab1:
    col_input, col_result = st.columns([1, 1.2], gap="large")

    with col_input:
        st.markdown("### 📋 البيانات الفسيولوجية والسريرية")
        
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
        
        st.info(f"مؤشر الـ BMI المحسوب: **{calculated_bmi:.1f}** ({bmi_status})")

        st.markdown("---")
        st.markdown("**2. المؤشرات الحيوية والمخْبَرية:**")
        
        glucose = st.slider("مستوى الجلوكوز الصائم (Fasting Glucose mg/dL)", 50, 250, 110)
        if glucose > 126:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ هذا المؤشر في المنطقة الحمراء (خطر مرتفع)</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: green; font-weight: bold;'>✅ هذا المؤشر في المعدل الطبيعي</p>", unsafe_allow_html=True)

        bp = st.slider("ضغط الدم الانقبائي (Blood Pressure mm Hg)", 40, 140, 72)
        if bp > 90:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ هذا المؤشر في المنطقة الحمراء (خطر مرتفع)</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: green; font-weight: bold;'>✅ هذا المؤشر في المعدل الطبيعي</p>", unsafe_allow_html=True)

        insulin = st.slider("مستوى الأنسولين (Insulin mu U/ml)", 0, 840, 80)
        if insulin > 166:
            st.markdown("<p style='color: red; font-weight: bold;'>⚠️ هذا المؤشر في المنطقة الحمراء (خطر مرتفع)</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='color: green; font-weight: bold;'>✅ هذا المؤشر في المعدل الطبيعي</p>", unsafe_allow_html=True)

        skin_thickness = st.slider("سمك ثنية الجلد (Skin Thickness mm)", 0, 99, 20)
        dpf = st.slider("مؤشر التاريخ الوراثي (Diabetes Pedigree)", 0.08, 2.42, 0.47, step=0.01)
        age = st.number_input("العمر (بالسنوات)", 1, 120, 33)
        pregnancies = st.number_input("عدد الحمول (Pregnancies)", 0, 20, 1)

    with col_result:
        st.markdown("### 🎯 نتيجة التنبؤ والتحليل الذكي")

        if model is None:
            st.error("⚠️ لم يتم العثور على النموذج! يرجى التأكد من وجود ملف `models/model.skops`.")
        else:
            if st.button("إجراء الفحص الطبي الذكي 🔍"):
                feature_names_en = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
                features = pd.DataFrame([[pregnancies, glucose, bp, skin_thickness, insulin, calculated_bmi, dpf, age]], 
                                        columns=feature_names_en)
                
                prediction = model.predict(features)[0]
                probability = model.predict_proba(features)[0][1] * 100

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=probability,
                    number={'suffix': "%", 'font': {'size': 36, 'color': '#0d47a1'}},
                    title={'text': "نسبة خطورة الإصابة المحتملة", 'font': {'size': 18, 'color': '#1565c0'}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#0d47a1'},
                        'bar': {'color': "#1565c0"},
                        'bgcolor': "#ffffff",
                        'steps': [
                            {'range': [0, 35], 'color': "#bbdefb"},
                            {'range': [35, 70], 'color': "#64b5f6"},
                            {'range': [70, 100], 'color': "#1e88e5"}
                        ]
                    }
                ))
                fig_gauge.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': '#0d47a1'})
                st.plotly_chart(fig_gauge, use_container_width=True)

                if prediction == 1:
                    st.error(f"⚠️ **النتيجة:** احتمال مرتفع للإصابة بمرض السكري ({probability:.1f}%)")
                    st.warning("""
                    **💡 التوصيات الطبية الوقائية:**
                    * مراجعة الطبيب المختص لإجراء فحص السكر التراكمي (HbA1c).
                    * الالتزام بنسق غذائي صحي وتقليل السكريات.
                    * ممارسة النشاط البدني بانتظام.
                    """)
                else:
                    st.success(f"✅ **النتيجة:** احتمال منخفض للإصابة (حالة مستقرة) ({probability:.1f}%)")
                    st.info("""
                    **💡 نصائح للحفاظ على الصحة:**
                    * الاستمرار في اتباع نمط حياة صحي ومتوازن.
                    * إجراء الفحوصات الدورية للاطمئنان المستمر.
                    """)

                st.markdown("---")
                st.markdown("#### 🔍 تحليل تأثير العوامل السريرية على النتيجة:")
                feature_names_ar = ['الحمل', 'الجلوكوز', 'ضغط الدم', 'سمك الجلد', 'الأنسولين', 'BMI', 'الوراثة', 'العمر']
                
                last_step = model.steps[-1][1] 
                if hasattr(last_step, 'coef_'):
                    importances = np.abs(last_step.coef_[0])
                else:
                    importances = np.zeros(len(feature_names_ar)) 
                    
                df_imp = pd.DataFrame({'العامل': feature_names_ar, 'الأهمية': importances}).sort_values('الأهمية', ascending=True)
                
                fig_imp = px.bar(df_imp, x='الأهمية', y='العامل', orientation='h', color='الأهمية',
                                 color_continuous_scale=['#bbdefb', '#1565c0'])
                fig_imp.update_layout(
                    height=280, margin=dict(l=10, r=10, t=10, b=10), 
                    showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#0d47a1', 'size': 14}
                )
                fig_imp.update_xaxes(title_font=dict(size=14, color='#0d47a1'), tickfont=dict(size=12, color='#0d47a1'))
                fig_imp.update_yaxes(title_font=dict(size=14, color='#0d47a1'), tickfont=dict(size=12, color='#0d47a1'))
                
                st.plotly_chart(fig_imp, use_container_width=True)

# ==================== التبويب الثاني ====================
with tab2:
    st.header("📚 دليل توعوي مبسط: كيف تتعرف على مخاطر السكري؟")
    st.markdown("<p style='color: #1565c0; font-size: 16px;'>هذا الدليل موجه للأشخاص الذين لا يملكون خلفية طبية، ويشرح المؤشرات الثمانية بلغة مبسطة.</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    with st.expander("🩸 1. مستوى الجلوكوز الصائم (Fasting Glucose)"):
        st.markdown("""
        * **ما هو؟** هو كمية السكر في الدم بعد الامتناع عن الطعام لمدة 8 ساعات.
        * **المعدل الطبيعي:** بين 70 و 99 mg/dL.
        * **متى يجب القلق؟** إذا تجاوز 126 mg/dL، فهذا يشير إلى أن البنكرياس لا يعمل بكفاءة، وهو مؤشر قوي على الإصابة بالسكري.
        * **نصيحة:** الإقلال من السكريات والكربوهيدرات (الخبز الأبيض، المشروبات الغازية).
        """)
        
    with st.expander("⚖️ 2. مؤشر كتلة الجسم (BMI)"):
        st.markdown("""
        * **ما هو؟** هو مقياس للعلاقة بين الوزن والطول.
        * **المعدل الطبيعي:** بين 18.5 و 24.9.
        * **متى يجب القلق؟** إذا كان فوق 25 (وزن زائد) أو فوق 30 (سمنة)، فهذا يزيد من مقاومة الإنسولين وبالتالي خطر السكري.
        * **نصيحة:** ممارسة المشي لمدة 30 دقيقة يومياً، وتقليل الدهون.
        """)
        
    with st.expander("🫀 3. ضغط الدم (Blood Pressure)"):
        st.markdown("""
        * **ما هو؟** القوة التي يضخ بها القلب الدم في الشرايين.
        * **المعدل الطبيعي:** حوالي 120/80 mm Hg.
        * **متى يجب القلق؟** إذا كان فوق 140/90، لأن الضغط العالي يضر بالكلى والأوعية الدموية ويزيد خطر السكري.
        """)

    with st.expander("🧬 4. مؤشر التاريخ الوراثي (Diabetes Pedigree)"):
        st.markdown("""
        * **ما هو؟** هذا الرقم يحسب احتمالية إصابتك بناءً على تاريخ عائلتك.
        * **متى يجب القلق؟** إذا كان الرقم مرتفعاً (فوق 0.8)، فهذا يعني أن العامل الوراثي قوي، ويجب إجراء فحوصات دورية.
        """)

    with st.expander("💉 5. مستوى الأنسولين (Insulin)"):
        st.markdown("""
        * **ما هو؟** الهرمون الذي يفرزه البنكرياس لتنظيم السكر في الدم.
        * **متى يجب القلق؟** إذا كان مرتفعاً جداً، فهذا يعني أن الجسم بدأ يفقد استجابته للأنسولين (مقاومة الإنسولين).
        """)
        
    with st.expander("🧑 6. العمر وعدد الحمول (Age & Pregnancies)"):
        st.markdown("""
        * **العمر:** كلما تقدم الإنسان في العمر (فوق 45 سنة)، زاد خطر الإصابة بالسكري.
        * **الحمل:** النساء اللواتي أنجبن أكثر من 4 مرات لديهن خطر أكبر.
        """)

    st.markdown("---")
    st.info("💡 **الخلاصة:** إذا كانت لديك أكثر من مؤشر في المنطقة الحمراء، يجب عليك مراجعة الطبيب. هذا التطبيق للتنبيه فقط، وليس تشخيصاً طبياً نهائياً.")