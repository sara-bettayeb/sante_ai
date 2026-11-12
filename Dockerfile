# استخدام صورة بايثون الرسمية الخفيفة
FROM python:3.10-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع (الكود، مجلد archive للصورة وللبيانات)
COPY . .

# فتح منفذ ستريمليت الافتراضي
EXPOSE 8501


# أمر تشغيل التطبيق
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]