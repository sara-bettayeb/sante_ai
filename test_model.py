import urllib.request
from skops.io import load
import numpy as np

url = "https://huggingface.co/RavshanjonEminov/Diabetes-Risk-Prediction/resolve/main/model.skops"
file_path = "models/model.skops"

print("⏳ جاري تحميل النموذج...")
urllib.request.urlretrieve(url, file_path)
print("✅ تم التحميل بنجاح!")

print("\n🔍 جاري تحميل النموذج للاختبار (مع الوثوق بـ numpy.dtype)...")

try:
    loaded_data = load(file_path, trusted=['numpy.dtype'])
    
    # نستخرجو الـ pipeline من القاموس
    pipeline = loaded_data['pipeline']
    threshold = loaded_data.get('threshold', 0.5) # إذا ما كانش، نستعملو 0.5
    model_type = loaded_data.get('model_type', 'Unknown')
    
    print(f"ℹ️ نوع النموذج: {model_type}")
    print(f"ℹ️ العتبة (Threshold): {threshold}")
    print("🎉 النموذج اشتغل بنجاح وجاهز للاستخدام!")
    
    # نتحققو من عدد المدخلات
    if hasattr(pipeline, "n_features_in_"):
        print(f"🔢 عدد المدخلات المتوقعة: {pipeline.n_features_in_}")
    else:
        print("ℹ️ عدد المدخلات غير متوفر مباشرة.")
        
    # نتحققو من دعم الاحتمالات
    if hasattr(pipeline, "predict_proba"):
        print("✅ النموذج يدعم حساب الاحتمالات (predict_proba).")
    else:
        print("ℹ️ النموذج لا يدعم حساب الاحتمالات المباشرة.")
        
    # --- اختبار سريع بمدخلات وهمية (8 قيم) ---
    print("\n🧪 اختبار سريع بمدخلات وهمية (8 خصائص):")
    # المدخلات: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
    dummy_input = np.array([[2, 120, 70, 20, 80, 25.0, 0.5, 30]])
    
    try:
        prediction = pipeline.predict(dummy_input)
        print(f"🔮 التنبؤ: {prediction[0]} (0 = سليم، 1 = مصاب)")
        
        if hasattr(pipeline, "predict_proba"):
            proba = pipeline.predict_proba(dummy_input)
            print(f"📊 الاحتمالات: {proba}")
    except Exception as e:
        print(f"❌ خطأ أثناء التنبؤ: {e}")

except Exception as e:
    print(f"❌ حدث خطأ أثناء تحميل النموذج: {e}")