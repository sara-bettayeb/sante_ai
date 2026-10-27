import streamlit as st

# إعداد الصفحة وتحديد الأيقونة
st.set_page_config(
    page_title="نظام التنبؤ بأمراض القلب",
    page_icon="❤️",
    layout="centered"
)

# تخصيص المظهر بالـ CSS ودعم اتجاه اليمين (RTL)
st.markdown("""
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .main-title {
        text-align: center;
        color: #b7094c;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #555555;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    div.stButton > button:first-child {
        background-color: #b7094c;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 8px;
        width: 100%;
        padding: 0.6rem;
        border: none;
    }
    div.stButton > button:first-child:hover {
        background-color: #890838;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان والوصف
st.markdown("<h1 class='main-title'>❤️ نظام الذكاء الاصطناعي للتنبؤ بأمراض القلب</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>أدخل القياسات السريرية للمريض للحصول على التقييم الأولي</p>", unsafe_allow_html=True)

# حقول الإدخال
age = st.number_input("العمر (Age)", value=45, min_value=1, max_value=120)
bp = st.number_input("ضغط الدم (Blood Pressure)", value=120, min_value=50, max_value=250)
chol = st.number_input("الكوليسترول (Cholesterol)", value=200, min_value=100, max_value=600)

# زر التحليل وكود التنبؤ
if st.button("تحليل الحالة الطبية"):
    # إذا كانت لديك شروط معينة أو استدعاء للنموذج:
    if chol < 240 and bp < 140:
        st.success("المؤشرات مستقرة وطبيعية ✅")
    else:
        st.warning("يُرجى استشارة الطبيب لإجراء فحوصات إضافية ⚠️")