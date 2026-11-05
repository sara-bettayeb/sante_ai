import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# التأكد من وجود مجلد models
os.makedirs("models", exist_ok=True)

# 1. تحميل مجموعة البيانات العلمية (Pima Indians Diabetes Dataset)
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']

print("⏳ جاري تحميل البيانات وتدريب النموذج...")
df = pd.read_csv(url, names=columns)

# 2. فصل المتغيرات والهدف
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# 3. تقسيم البيانات وتدريب نموذج Random Forest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. حفظ النموذج المكتمل
joblib.dump(model, 'models/diabetes_model.pkl')
print("✅ تم حفظ نموذج الذكاء الاصطناعي بنجاح داخل: models/diabetes_model.pkl")