Thyroid Care 🦋

Thyroid Care is an educational web application designed to provide information about the thyroid gland, its functions, common disorders, and medical tests.

The application also includes an AI-powered assistant that answers general educational questions about thyroid health.

Features

- Home: Introduction to the application.
- About: Information about the thyroid gland.
- Thyroid Diseases: Educational information about hypothyroidism and hyperthyroidism.
- Thyroid Tests: Information about TSH, T3, T4, and thyroid antibodies.
- AI Assistant: An AI assistant powered by Llama 3.2 (1B) through Ollama.

Technologies Used

- HTML, CSS, JavaScript
- Node.js
- Express.js
- Ollama
- Llama 3.2 (1B)
- Docker and Docker Compose

Project Structure

thyroid-app/
├── frontend/
├── backend/
├── ai/
├── Dockerfile
├── docker-compose.yml
└── package.json

Requirements

- Docker Desktop
- Internet connection for the initial AI model download

How to Run the Project

1. Clone the repository

git clone https://github.com/ferial04/thyroid-care.git

2. Open the project folder

cd thyroid-care

3. Create the Ollama Docker volume

docker volume create ollama

4. Build and start the containers

docker compose up --build -d

5. Download the AI model

docker exec -it ollama ollama pull llama3.2:1b

Wait until the download finishes.

6. Open the application

Visit:

http://localhost:3000

AI Assistant

The AI assistant uses the locally running Ollama service with the Llama 3.2 (1B) model.

No external AI API key is required.

Important Note

This application is for educational purposes only. It does not provide medical diagnoses or replace professional medical advice.

Author

Thyroid Care Module — University Group Project
# نظام الذكاء الاصطناعي للتنبؤ بأمراض القلب (sante_ai)

تطبيق ويب طبي تفاعلي مبني باستخدام Streamlit ومغلف بالكامل داخل حاوية Docker.

## الملفات الأساسية
- app.py: كود الواجهة التفاعلية والمنطق الطبي.
- Dockerfile: تعليمات بناء وتجهيز الحاوية.
- requirements.txt: المكتبات اللازمة لتشغيل التطبيق.

## طريقة التشغيل عبر Docker

1. بناء الصورة (Build Image):
`bash
docker build -t sante-ai-image .
