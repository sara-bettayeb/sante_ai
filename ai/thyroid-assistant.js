async function askThyroidAssistant(message) {
    const ollamaUrl =
        process.env.OLLAMA_URL ||
        "http://localhost:11434/api/generate";

    const response = await fetch(ollamaUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model: "llama3.2:1b",
            prompt:` 
You are a thyroid health educational assistant.

Answer questions about the thyroid gland,
its hormones, diseases, and medical tests.

Use simple and clear language.
Do not diagnose diseases or prescribe medication.
Remind users to consult a healthcare professional
for personal medical concerns.

User question: ${message}
           ` ,
            stream: false
        })
    });

    if (!response.ok) {
        throw new Error("AI model connection failed");
    }

    const data = await response.json();

    return data.response;
}

module.exports = askThyroidAssistant;