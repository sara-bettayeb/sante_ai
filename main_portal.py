import sys
import types
import streamlit as st
from sklearn.base import BaseEstimator, TransformerMixin

# حقن FrequencyEncoder في main لكي يعمل موديل القلب بدون خطأ
class FrequencyEncoder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X

if 'main' in sys.modules:
    setattr(sys.modules['main'], 'FrequencyEncoder', FrequencyEncoder)
else:
    fake_main = types.ModuleType('main')
    fake_main.FrequencyEncoder = FrequencyEncoder
    sys.modules['main'] = fake_main

p_home = st.Page("home_view.py", title="الرئيسية (بوابة المنصة)", icon="🏥", url_path="home", default=True)
p_heart = st.Page("app.py", title="أمراض القلب (Cardiology)", icon="🫀", url_path="heart")
p_hyper = st.Page("hypertension-prediction/streamlit_app.py", title="ضغط الدم (Hypertension)", icon="🩺", url_path="hypertension")
p_diab = st.Page("app/dashboard.py", title="السكري (Diabetology)", icon="🩸", url_path="diabetes")
p_thyroid = st.Page("thyroid/app.py", title="الغدة الدرقية (Thyroid)", icon="🦋", url_path="thyroid")

pg = st.navigation([p_home, p_heart, p_hyper, p_diab, p_thyroid])
pg.run()