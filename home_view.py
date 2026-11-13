import streamlit as st
import pandas as pd
from database import get_all_diagnostics

st.set_page_config(page_title="Sante AI | المنصة الطبية المتكاملة", page_icon="🏥", layout="wide")

st.markdown("""
<style>
.portal-header {
    text-align: center;
    padding: 25px 10px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 18px;
    border: 1px solid rgba(56, 189, 248, 0.25);
    margin-bottom: 30px;
}
.portal-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #38bdf8;
    margin-bottom: 8px;
}
.portal-sub {
    color: #cbd5e1;
    font-size: 1.05rem;
}
.module-card {
    background: #1e293b;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.module-icon { font-size: 2.8rem; margin-bottom: 10px; }
.module-name { font-size: 1.3rem; font-weight: 700; color: #f8fafc; margin-bottom: 6px; }
.module-desc { font-size: 0.9rem; color: #94a3b8; min-height: 45px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="portal-header">
    <div class="portal-title">🏥 منصة Sante AI للتشخيص الطبي الذكي</div>
    <div class="portal-sub">اختر التخصص الطبي للانتقال مباشرة إلى لوحة التنبؤ الذكي وحفظ السجلات</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🫀</div>
        <div class="module-name">أمراض القلب</div>
        <div class="module-desc">تقييم مخاطر القلب والأوعية الدموية وتحليل المؤشرات السريرية</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("الدخول لقسم القلب ⬅️", key="btn_heart", use_container_width=True):
        st.switch_page("app.py")

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🩺</div>
        <div class="module-name">ضغط الدم</div>
        <div class="module-desc">التنبؤ بمخاطر ارتفاع ضغط الدم (Hypertension) وتحليل العوامل</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("الدخول لقسم ضغط الدم ⬅️", key="btn_hyper", use_container_width=True):
        st.switch_page("hypertension-prediction/streamlit_app.py")

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🩸</div>
        <div class="module-name">داء السكري</div>
        <div class="module-desc">الكشف المبكر عن السكري وتقييم مستويات الجلوكوز وكتلة الجسم</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("الدخول لقسم السكري ⬅️", key="btn_diab", use_container_width=True):
        st.switch_page("app/dashboard.py")

with col4:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">🦋</div>
        <div class="module-name">الغدة الدرقية</div>
        <div class="module-desc">تشخيص اضطرابات الغدة الدرقية وتحليل هرمونات TSH و T3 و T4</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("الدخول لقسم الغدة ⬅️", key="btn_thyroid", use_container_width=True):
        st.switch_page("thyroid/app.py")

st.markdown("---")
st.subheader("📊 آخر الفحوصات المسجلة في جميع الأقسام")
try:
    all_records = get_all_diagnostics()
    if all_records:
        st.dataframe(pd.DataFrame(all_records), use_container_width=True)
    else:
        st.info("لا توجد فحوصات مسجلة في المنصة بعد.")
except Exception as e:
    st.warning(f"تعذر تحميل السجل العام: {e}")